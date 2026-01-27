"""
EEX Commitment of Traders Report Parser

This module parses Excel files from the European Energy Exchange (EEX)
containing MiFID II RTS 21 weekly reports (Commitment of Traders data).
"""
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional
import re


class EEXCoTParser:
    """Parser for EEX Commitment of Traders Excel reports."""

    # Category mappings
    CATEGORIES = {
        'investment_firms': 'Investment Firms or credit institutions',
        'investment_funds': 'Investment Funds',
        'other_financial': 'Other Financial Institutions',
        'commercial': 'Commercial Undertakings',
        'compliance_operators': 'Operators with compliance obligations under Directive 2003/87/EC'
    }

    def __init__(self, file_path: str):
        """
        Initialize parser with file path.

        Args:
            file_path: Path to the Excel file
        """
        self.file_path = file_path
        self.xl_file = pd.ExcelFile(file_path)

    def extract_metadata(self, sheet_name: str = 'Weekly_Report') -> Dict[str, str]:
        """
        Extract metadata from the report header.

        Args:
            sheet_name: Name of the sheet to parse (default: 'Weekly_Report')

        Returns:
            Dictionary containing metadata fields
        """
        df = pd.read_excel(self.file_path, sheet_name=sheet_name, header=None)

        metadata = {}
        # Extract metadata from first 8 rows
        metadata['trading_venue'] = df.iloc[0, 1]
        metadata['venue_identifier'] = df.iloc[1, 1]
        metadata['report_date'] = pd.to_datetime(df.iloc[2, 1]).strftime('%Y-%m-%d')
        metadata['publication_datetime'] = df.iloc[3, 1]
        metadata['contract_name'] = df.iloc[4, 1]
        metadata['contract_code'] = df.iloc[5, 1]
        metadata['report_status'] = df.iloc[6, 1]
        metadata['report_type'] = df.iloc[7, 1]

        return metadata

    def parse_positions(self, sheet_name: str = 'Weekly_Report') -> pd.DataFrame:
        """
        Parse position data from the report.

        Args:
            sheet_name: Name of the sheet to parse (default: 'Weekly_Report')

        Returns:
            DataFrame with structured position data
        """
        df = pd.read_excel(self.file_path, sheet_name=sheet_name, header=None)

        # Extract metadata first
        metadata = self.extract_metadata(sheet_name)

        # Parse positions data (rows 11-13: Number of positions)
        # Row structure: [Label, Type, Description, IF_Long, IF_Short, IFund_Long, IFund_Short, ...]
        positions = []

        # Categories start at column 3
        categories = [
            ('investment_firms', 3, 4),
            ('investment_funds', 5, 6),
            ('other_financial', 7, 8),
            ('commercial', 9, 10),
            ('compliance_operators', 11, 12)
        ]

        # Row 11: Risk reducing positions
        # Row 12: Other positions
        # Row 13: Total positions
        position_types = {
            11: 'risk_reducing',
            12: 'other',
            13: 'total'
        }

        for row_idx, pos_type in position_types.items():
            for cat_name, long_col, short_col in categories:
                long_val = df.iloc[row_idx, long_col]
                short_val = df.iloc[row_idx, short_col]

                positions.append({
                    'report_date': metadata['report_date'],
                    'contract_code': metadata['contract_code'],
                    'category': cat_name,
                    'position_type': pos_type,
                    'long': self._clean_number(long_val),
                    'short': self._clean_number(short_val),
                    'net': self._clean_number(long_val) - self._clean_number(short_val)
                })

        # Parse changes (rows 14-16)
        changes = []
        change_types = {
            14: 'risk_reducing',
            15: 'other',
            16: 'total'
        }

        for row_idx, pos_type in change_types.items():
            for cat_name, long_col, short_col in categories:
                long_val = df.iloc[row_idx, long_col]
                short_val = df.iloc[row_idx, short_col]

                changes.append({
                    'report_date': metadata['report_date'],
                    'contract_code': metadata['contract_code'],
                    'category': cat_name,
                    'position_type': pos_type,
                    'long_change': self._clean_number(long_val),
                    'short_change': self._clean_number(short_val),
                    'net_change': self._clean_number(long_val) - self._clean_number(short_val)
                })

        # Parse percentages (rows 17-19)
        percentages = []
        pct_types = {
            17: 'risk_reducing',
            18: 'other',
            19: 'total'
        }

        for row_idx, pos_type in pct_types.items():
            for cat_name, long_col, short_col in categories:
                long_val = df.iloc[row_idx, long_col]
                short_val = df.iloc[row_idx, short_col]

                percentages.append({
                    'report_date': metadata['report_date'],
                    'contract_code': metadata['contract_code'],
                    'category': cat_name,
                    'position_type': pos_type,
                    'long_pct': self._clean_number(long_val),
                    'short_pct': self._clean_number(short_val)
                })

        positions_df = pd.DataFrame(positions)
        changes_df = pd.DataFrame(changes)
        percentages_df = pd.DataFrame(percentages)

        # Merge all data
        result_df = positions_df.merge(
            changes_df,
            on=['report_date', 'contract_code', 'category', 'position_type'],
            how='left'
        ).merge(
            percentages_df,
            on=['report_date', 'contract_code', 'category', 'position_type'],
            how='left'
        )

        return result_df

    def parse_all_sheets(self) -> pd.DataFrame:
        """
        Parse all sheets in the Excel file (current week and historical data).

        Returns:
            DataFrame with data from all sheets
        """
        all_data = []

        for sheet_name in self.xl_file.sheet_names:
            try:
                df = self.parse_positions(sheet_name)
                all_data.append(df)
            except Exception as e:
                print(f"Warning: Could not parse sheet {sheet_name}: {e}")

        if all_data:
            return pd.concat(all_data, ignore_index=True)
        else:
            return pd.DataFrame()

    def _clean_number(self, value) -> float:
        """Convert value to float, handling NaN and formatting."""
        if pd.isna(value):
            return 0.0
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    def get_latest_report(self) -> Dict:
        """
        Get the latest report summary.

        Returns:
            Dictionary with latest report data
        """
        metadata = self.extract_metadata('Weekly_Report')
        positions_df = self.parse_positions('Weekly_Report')

        # Focus on total positions (not split by risk_reducing/other)
        total_positions = positions_df[positions_df['position_type'] == 'total'].copy()

        return {
            'metadata': metadata,
            'positions': total_positions
        }


def parse_file(file_path: str) -> pd.DataFrame:
    """
    Convenience function to parse an EEX CoT file.

    Args:
        file_path: Path to the Excel file

    Returns:
        DataFrame with position data
    """
    parser = EEXCoTParser(file_path)
    return parser.parse_all_sheets()


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python eex_parser.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    parser = EEXCoTParser(file_path)

    # Print metadata
    print("\n=== METADATA ===")
    metadata = parser.extract_metadata()
    for key, value in metadata.items():
        print(f"{key}: {value}")

    # Print latest report
    print("\n=== LATEST POSITIONS (Total) ===")
    latest = parser.get_latest_report()
    print(latest['positions'].to_string())

    # Parse all sheets
    print("\n=== ALL HISTORICAL DATA ===")
    all_data = parser.parse_all_sheets()
    print(f"\nTotal records: {len(all_data)}")
    print(f"Date range: {all_data['report_date'].min()} to {all_data['report_date'].max()}")
    print("\nSample data:")
    print(all_data.head(20))
