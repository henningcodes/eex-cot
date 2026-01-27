"""
EEX CoT Data Storage

This module manages storage and retrieval of historical CoT data.
"""
import pandas as pd
from pathlib import Path
from typing import List, Optional
from datetime import datetime, timedelta


class EEXDataStorage:
    """Storage manager for EEX Commitment of Traders data."""

    def __init__(self, data_dir: str = "data"):
        """
        Initialize storage manager.

        Args:
            data_dir: Directory to store data files
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def get_storage_file(self, contract: str) -> Path:
        """
        Get the storage file path for a contract.

        Args:
            contract: Contract code (e.g., 'DEBM')

        Returns:
            Path to the CSV file
        """
        return self.data_dir / f"{contract}_history.csv"

    def load_history(self, contract: str) -> Optional[pd.DataFrame]:
        """
        Load historical data for a contract.

        Args:
            contract: Contract code

        Returns:
            DataFrame with historical data, or None if no data exists
        """
        file_path = self.get_storage_file(contract)

        if not file_path.exists():
            print(f"No historical data found for {contract}")
            return None

        df = pd.read_csv(file_path)
        df['report_date'] = pd.to_datetime(df['report_date'])
        return df

    def save_history(self, contract: str, df: pd.DataFrame):
        """
        Save historical data for a contract.

        Args:
            contract: Contract code
            df: DataFrame with data to save
        """
        file_path = self.get_storage_file(contract)
        df.to_csv(file_path, index=False)
        print(f"Saved {len(df)} records to {file_path}")

    def append_data(self, contract: str, new_df: pd.DataFrame, deduplicate: bool = True):
        """
        Append new data to existing history.

        Args:
            contract: Contract code
            new_df: DataFrame with new data
            deduplicate: If True, remove duplicate entries (by report_date, category, position_type)
        """
        # Ensure report_date is datetime in new data
        new_df = new_df.copy()
        if 'report_date' in new_df.columns:
            new_df['report_date'] = pd.to_datetime(new_df['report_date'])

        # Load existing data
        existing_df = self.load_history(contract)

        if existing_df is None:
            # No existing data, just save new data
            self.save_history(contract, new_df)
            return

        # Combine data
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)

        if deduplicate:
            # Remove duplicates, keeping the most recent entry
            combined_df = combined_df.sort_values('report_date', ascending=False)
            combined_df = combined_df.drop_duplicates(
                subset=['report_date', 'category', 'position_type'],
                keep='first'
            )

        # Sort by date descending
        combined_df = combined_df.sort_values('report_date', ascending=False)

        self.save_history(contract, combined_df)

    def get_latest_date(self, contract: str) -> Optional[datetime]:
        """
        Get the date of the most recent report in storage.

        Args:
            contract: Contract code

        Returns:
            Date of latest report, or None if no data exists
        """
        df = self.load_history(contract)
        if df is None or len(df) == 0:
            return None

        return df['report_date'].max()

    def get_date_range(self, contract: str, start_date: Optional[str] = None,
                       end_date: Optional[str] = None) -> Optional[pd.DataFrame]:
        """
        Get data for a specific date range.

        Args:
            contract: Contract code
            start_date: Start date (YYYY-MM-DD), or None for earliest
            end_date: End date (YYYY-MM-DD), or None for latest

        Returns:
            DataFrame with filtered data
        """
        df = self.load_history(contract)
        if df is None:
            return None

        if start_date:
            df = df[df['report_date'] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df['report_date'] <= pd.to_datetime(end_date)]

        return df

    def get_weekly_totals(self, contract: str, weeks: int = 13) -> Optional[pd.DataFrame]:
        """
        Get total positions for the last N weeks.

        Args:
            contract: Contract code
            weeks: Number of weeks to retrieve

        Returns:
            DataFrame with weekly total positions
        """
        df = self.load_history(contract)
        if df is None:
            return None

        # Filter for total positions only
        df = df[df['position_type'] == 'total'].copy()

        # Sort by date descending and take last N weeks
        df = df.sort_values('report_date', ascending=False)

        # Get unique report dates
        unique_dates = df['report_date'].unique()[:weeks]

        # Filter for those dates
        df = df[df['report_date'].isin(unique_dates)]

        # Sort by date ascending for chronological order
        df = df.sort_values('report_date', ascending=True)

        return df

    def get_contracts(self) -> List[str]:
        """
        Get list of contracts with stored data.

        Returns:
            List of contract codes
        """
        contracts = []
        for file_path in self.data_dir.glob("*_history.csv"):
            contract = file_path.stem.replace("_history", "")
            contracts.append(contract)
        return sorted(contracts)


if __name__ == '__main__':
    import sys
    from eex_parser import EEXCoTParser

    if len(sys.argv) < 3:
        print("Usage: python eex_storage.py <command> <contract> [file_path]")
        print("\nCommands:")
        print("  import <contract> <file_path>  - Import data from Excel file")
        print("  show <contract>                - Show latest data")
        print("  list                           - List all contracts in storage")
        sys.exit(1)

    command = sys.argv[1]
    storage = EEXDataStorage()

    if command == "list":
        contracts = storage.get_contracts()
        print(f"Stored contracts: {', '.join(contracts)}")

    elif command == "import" and len(sys.argv) >= 4:
        contract = sys.argv[2]
        file_path = sys.argv[3]

        print(f"Importing {file_path} for contract {contract}")
        parser = EEXCoTParser(file_path)
        df = parser.parse_all_sheets()

        # Filter for this contract
        df = df[df['contract_code'] == contract]

        storage.append_data(contract, df)
        print(f"Import complete. Latest date: {storage.get_latest_date(contract)}")

    elif command == "show" and len(sys.argv) >= 3:
        contract = sys.argv[2]
        df = storage.load_history(contract)

        if df is not None:
            print(f"\n=== {contract} Summary ===")
            print(f"Total records: {len(df)}")
            print(f"Date range: {df['report_date'].min()} to {df['report_date'].max()}")
            print(f"\nLatest report ({df['report_date'].max()}):")

            latest = df[df['report_date'] == df['report_date'].max()]
            latest_total = latest[latest['position_type'] == 'total']
            print(latest_total[['category', 'long', 'short', 'net', 'long_change', 'short_change']].to_string())

    else:
        print("Invalid command or missing arguments")
        sys.exit(1)
