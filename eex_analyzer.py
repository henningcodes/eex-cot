"""
EEX CoT Data Analyzer

This module provides analysis functions for Commitment of Traders data.
"""
import pandas as pd
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta


class EEXAnalyzer:
    """Analyzer for EEX Commitment of Traders data."""

    CATEGORY_NAMES = {
        'investment_firms': 'Investment Firms',
        'investment_funds': 'Investment Funds',
        'other_financial': 'Other Financial',
        'commercial': 'Commercial',
        'compliance_operators': 'Compliance Operators'
    }

    def __init__(self, df: pd.DataFrame):
        """
        Initialize analyzer with data.

        Args:
            df: DataFrame with CoT data
        """
        self.df = df.copy()
        if 'report_date' in self.df.columns:
            self.df['report_date'] = pd.to_datetime(self.df['report_date'])

    def get_latest_positions(self, position_type: str = 'total') -> pd.DataFrame:
        """
        Get the latest positions for all categories.

        Args:
            position_type: Type of position ('total', 'risk_reducing', or 'other')

        Returns:
            DataFrame with latest positions
        """
        if len(self.df) == 0:
            return pd.DataFrame()

        latest_date = self.df['report_date'].max()
        latest_df = self.df[
            (self.df['report_date'] == latest_date) &
            (self.df['position_type'] == position_type)
        ].copy()

        # Sort by net position (largest net long to largest net short)
        latest_df = latest_df.sort_values('net', ascending=False)

        return latest_df

    def get_weekly_change(self, position_type: str = 'total') -> pd.DataFrame:
        """
        Get the change from the previous week.

        Args:
            position_type: Type of position ('total', 'risk_reducing', or 'other')

        Returns:
            DataFrame with weekly changes
        """
        if len(self.df) == 0:
            return pd.DataFrame()

        latest_date = self.df['report_date'].max()
        latest_df = self.df[
            (self.df['report_date'] == latest_date) &
            (self.df['position_type'] == position_type)
        ].copy()

        # The changes are already in the data
        return latest_df[['category', 'long_change', 'short_change', 'net_change']].sort_values(
            'net_change', ascending=False
        )

    def get_positioning_summary(self) -> Dict:
        """
        Get a comprehensive summary of current positioning.

        Returns:
            Dictionary with summary statistics
        """
        latest_positions = self.get_latest_positions('total')

        if len(latest_positions) == 0:
            return {}

        latest_date = self.df['report_date'].max()

        summary = {
            'report_date': latest_date.strftime('%Y-%m-%d'),
            'contract_code': latest_positions.iloc[0]['contract_code'],
            'total_long': latest_positions['long'].sum(),
            'total_short': latest_positions['short'].sum(),
            'net_position': latest_positions['net'].sum(),
            'categories': {}
        }

        for _, row in latest_positions.iterrows():
            cat_name = self.CATEGORY_NAMES.get(row['category'], row['category'])
            summary['categories'][row['category']] = {
                'name': cat_name,
                'long': row['long'],
                'short': row['short'],
                'net': row['net'],
                'long_change': row['long_change'],
                'short_change': row['short_change'],
                'net_change': row['net_change'],
                'long_pct': row['long_pct'],
                'short_pct': row['short_pct']
            }

        return summary

    def get_historical_series(self, category: str, weeks: int = 13) -> pd.DataFrame:
        """
        Get historical time series for a specific category.

        Args:
            category: Category name (e.g., 'investment_funds')
            weeks: Number of weeks to retrieve

        Returns:
            DataFrame with historical data
        """
        df = self.df[
            (self.df['category'] == category) &
            (self.df['position_type'] == 'total')
        ].copy()

        # Sort by date descending and take last N weeks
        df = df.sort_values('report_date', ascending=False)

        # Get unique dates
        unique_dates = df['report_date'].unique()[:weeks]
        df = df[df['report_date'].isin(unique_dates)]

        # Sort chronologically
        df = df.sort_values('report_date', ascending=True)

        return df[['report_date', 'long', 'short', 'net']]

    def compare_periods(self, weeks_back: int = 4) -> pd.DataFrame:
        """
        Compare current positions with positions from N weeks ago.

        Args:
            weeks_back: Number of weeks to look back

        Returns:
            DataFrame with comparison
        """
        if len(self.df) == 0:
            return pd.DataFrame()

        # Get unique dates
        unique_dates = sorted(self.df['report_date'].unique(), reverse=True)

        if len(unique_dates) < weeks_back + 1:
            print(f"Warning: Only {len(unique_dates)} weeks of data available")
            weeks_back = len(unique_dates) - 1

        current_date = unique_dates[0]
        past_date = unique_dates[min(weeks_back, len(unique_dates) - 1)]

        current = self.df[
            (self.df['report_date'] == current_date) &
            (self.df['position_type'] == 'total')
        ][['category', 'long', 'short', 'net']].set_index('category')

        past = self.df[
            (self.df['report_date'] == past_date) &
            (self.df['position_type'] == 'total')
        ][['category', 'long', 'short', 'net']].set_index('category')

        comparison = pd.DataFrame({
            'current_long': current['long'],
            'current_short': current['short'],
            'current_net': current['net'],
            'past_long': past['long'],
            'past_short': past['short'],
            'past_net': past['net']
        })

        comparison['long_change'] = comparison['current_long'] - comparison['past_long']
        comparison['short_change'] = comparison['current_short'] - comparison['past_short']
        comparison['net_change'] = comparison['current_net'] - comparison['past_net']

        comparison['long_pct_change'] = (comparison['long_change'] / comparison['past_long'] * 100).round(2)
        comparison['short_pct_change'] = (comparison['short_change'] / comparison['past_short'] * 100).round(2)
        comparison['net_pct_change'] = ((comparison['net_change'] / comparison['past_net'].abs()) * 100).round(2)

        return comparison

    def print_summary(self):
        """Print a formatted summary of current positioning."""
        summary = self.get_positioning_summary()

        if not summary:
            print("No data available")
            return

        print(f"\n{'='*80}")
        print(f"COMMITMENT OF TRADERS REPORT - {summary['contract_code']}")
        print(f"Report Date: {summary['report_date']}")
        print(f"{'='*80}\n")

        print(f"OVERALL MARKET:")
        print(f"  Total Long:   {summary['total_long']:>15,.0f} MW")
        print(f"  Total Short:  {summary['total_short']:>15,.0f} MW")
        print(f"  Net Position: {summary['net_position']:>15,.0f} MW")
        print()

        print(f"{'CATEGORY':<25} {'LONG':>15} {'SHORT':>15} {'NET':>15} {'CHG':>12}")
        print("-" * 85)

        for cat_key, cat_data in summary['categories'].items():
            print(f"{cat_data['name']:<25} "
                  f"{cat_data['long']:>15,.0f} "
                  f"{cat_data['short']:>15,.0f} "
                  f"{cat_data['net']:>15,.0f} "
                  f"{cat_data['net_change']:>12,.0f}")

        print()
        print("WEEKLY CHANGES:")
        print(f"{'CATEGORY':<25} {'LONG CHG':>15} {'SHORT CHG':>15} {'NET CHG':>15}")
        print("-" * 73)

        for cat_key, cat_data in summary['categories'].items():
            print(f"{cat_data['name']:<25} "
                  f"{cat_data['long_change']:>15,.0f} "
                  f"{cat_data['short_change']:>15,.0f} "
                  f"{cat_data['net_change']:>15,.0f}")

        print()
        print("PERCENTAGE OF TOTAL OPEN INTEREST:")
        print(f"{'CATEGORY':<25} {'LONG %':>10} {'SHORT %':>10}")
        print("-" * 48)

        for cat_key, cat_data in summary['categories'].items():
            print(f"{cat_data['name']:<25} "
                  f"{cat_data['long_pct']:>9.2f}% "
                  f"{cat_data['short_pct']:>9.2f}%")

        print()


if __name__ == '__main__':
    import sys
    from eex_storage import EEXDataStorage

    if len(sys.argv) < 2:
        print("Usage: python eex_analyzer.py <contract>")
        sys.exit(1)

    contract = sys.argv[1]

    storage = EEXDataStorage()
    df = storage.load_history(contract)

    if df is None or len(df) == 0:
        print(f"No data found for contract {contract}")
        sys.exit(1)

    analyzer = EEXAnalyzer(df)
    analyzer.print_summary()

    print("\n" + "="*80)
    print("4-WEEK COMPARISON")
    print("="*80)
    comparison = analyzer.compare_periods(4)
    if len(comparison) > 0:
        print(comparison.to_string())
