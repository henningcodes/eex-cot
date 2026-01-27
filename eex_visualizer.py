"""
EEX CoT Data Visualizer

This module creates visualizations for Commitment of Traders data.
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path
from typing import List, Optional, Dict
from datetime import datetime


class EEXVisualizer:
    """Visualizer for EEX Commitment of Traders data."""

    CATEGORY_NAMES = {
        'investment_firms': 'Investment Firms',
        'investment_funds': 'Investment Funds',
        'other_financial': 'Other Financial',
        'commercial': 'Commercial',
        'compliance_operators': 'Compliance Operators'
    }

    CATEGORY_COLORS = {
        'investment_firms': '#2E86AB',      # Blue
        'investment_funds': '#A23B72',      # Purple
        'other_financial': '#F18F01',       # Orange
        'commercial': '#C73E1D',            # Red
        'compliance_operators': '#6A994E'   # Green
    }

    def __init__(self, df: pd.DataFrame, output_dir: str = "plots"):
        """
        Initialize visualizer with data.

        Args:
            df: DataFrame with CoT data
            output_dir: Directory to save plot images
        """
        self.df = df.copy()
        if 'report_date' in self.df.columns:
            self.df['report_date'] = pd.to_datetime(self.df['report_date'])

        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def plot_net_positions(self, contract: str, weeks: int = 13,
                          categories: Optional[List[str]] = None,
                          save: bool = True, show: bool = False) -> Optional[Path]:
        """
        Plot net positions over time for different categories.

        Args:
            contract: Contract code
            weeks: Number of weeks to plot
            categories: List of categories to plot (None = all)
            save: Whether to save the plot
            show: Whether to display the plot

        Returns:
            Path to saved plot, or None if not saved
        """
        if categories is None:
            categories = list(self.CATEGORY_NAMES.keys())

        # Filter data
        df = self.df[
            (self.df['position_type'] == 'total') &
            (self.df['category'].isin(categories))
        ].copy()

        # Get last N weeks
        unique_dates = sorted(df['report_date'].unique(), reverse=True)[:weeks]
        df = df[df['report_date'].isin(unique_dates)]
        df = df.sort_values('report_date')

        # Create plot
        fig, ax = plt.subplots(figsize=(14, 8))

        for category in categories:
            cat_df = df[df['category'] == category]
            if len(cat_df) > 0:
                ax.plot(cat_df['report_date'], cat_df['net'],
                       marker='o', linewidth=2, markersize=6,
                       label=self.CATEGORY_NAMES.get(category, category),
                       color=self.CATEGORY_COLORS.get(category, None))

        # Add zero line
        ax.axhline(y=0, color='black', linestyle='--', linewidth=0.8, alpha=0.5)

        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
        plt.xticks(rotation=45, ha='right')

        # Labels and title
        ax.set_xlabel('Report Date', fontsize=12, fontweight='bold')
        ax.set_ylabel('Net Position (MW)', fontsize=12, fontweight='bold')
        ax.set_title(f'{contract} - Net Positions by Category (Last {weeks} Weeks)',
                    fontsize=14, fontweight='bold', pad=20)

        # Grid
        ax.grid(True, alpha=0.3, linestyle='--')

        # Legend
        ax.legend(loc='best', framealpha=0.9, fontsize=10)

        # Format y-axis with thousands separator
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))

        plt.tight_layout()

        # Save or show
        file_path = None
        if save:
            file_path = self.output_dir / f"{contract}_net_positions_{weeks}w.png"
            plt.savefig(file_path, dpi=300, bbox_inches='tight')
            print(f"Saved plot to {file_path}")

        if show:
            plt.show()
        else:
            plt.close()

        return file_path

    def plot_long_short_positions(self, contract: str, category: str, weeks: int = 13,
                                  save: bool = True, show: bool = False) -> Optional[Path]:
        """
        Plot long and short positions for a specific category.

        Args:
            contract: Contract code
            category: Category to plot
            weeks: Number of weeks to plot
            save: Whether to save the plot
            show: Whether to display the plot

        Returns:
            Path to saved plot, or None if not saved
        """
        # Filter data
        df = self.df[
            (self.df['position_type'] == 'total') &
            (self.df['category'] == category)
        ].copy()

        # Get last N weeks
        unique_dates = sorted(df['report_date'].unique(), reverse=True)[:weeks]
        df = df[df['report_date'].isin(unique_dates)]
        df = df.sort_values('report_date')

        if len(df) == 0:
            print(f"No data available for category {category}")
            return None

        # Create plot with two subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

        # Top plot: Long and Short positions
        ax1.plot(df['report_date'], df['long'], marker='o', linewidth=2,
                markersize=6, label='Long', color='#2E86AB')
        ax1.plot(df['report_date'], df['short'], marker='s', linewidth=2,
                markersize=6, label='Short', color='#C73E1D')

        ax1.set_ylabel('Position Size (MW)', fontsize=11, fontweight='bold')
        ax1.set_title(f'{contract} - {self.CATEGORY_NAMES.get(category, category)} Positions',
                     fontsize=14, fontweight='bold', pad=15)
        ax1.grid(True, alpha=0.3, linestyle='--')
        ax1.legend(loc='best', framealpha=0.9, fontsize=10)
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))

        # Bottom plot: Net position
        colors = ['#2E86AB' if x > 0 else '#C73E1D' for x in df['net']]
        ax2.bar(df['report_date'], df['net'], color=colors, alpha=0.7, width=5)
        ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.8)

        ax2.set_xlabel('Report Date', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Net Position (MW)', fontsize=11, fontweight='bold')
        ax2.set_title('Net Position (Long - Short)', fontsize=12, fontweight='bold', pad=10)
        ax2.grid(True, alpha=0.3, linestyle='--', axis='y')
        ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))

        # Format x-axis
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax2.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
        plt.xticks(rotation=45, ha='right')

        plt.tight_layout()

        # Save or show
        file_path = None
        if save:
            file_path = self.output_dir / f"{contract}_{category}_{weeks}w.png"
            plt.savefig(file_path, dpi=300, bbox_inches='tight')
            print(f"Saved plot to {file_path}")

        if show:
            plt.show()
        else:
            plt.close()

        return file_path

    def plot_category_breakdown(self, contract: str, weeks: int = 13,
                               save: bool = True, show: bool = False) -> Optional[Path]:
        """
        Plot stacked area chart showing category breakdown of long/short positions.

        Args:
            contract: Contract code
            weeks: Number of weeks to plot
            save: Whether to save the plot
            show: Whether to display the plot

        Returns:
            Path to saved plot, or None if not saved
        """
        # Filter data
        df = self.df[self.df['position_type'] == 'total'].copy()

        # Get last N weeks
        unique_dates = sorted(df['report_date'].unique(), reverse=True)[:weeks]
        df = df[df['report_date'].isin(unique_dates)]
        df = df.sort_values('report_date')

        if len(df) == 0:
            print("No data available")
            return None

        # Pivot data for stacking
        long_pivot = df.pivot(index='report_date', columns='category', values='long_pct')
        short_pivot = df.pivot(index='report_date', columns='category', values='short_pct')

        # Create plot with two subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

        # Top plot: Long positions
        for category in long_pivot.columns:
            ax1.fill_between(long_pivot.index, 0, long_pivot[category],
                           label=self.CATEGORY_NAMES.get(category, category),
                           color=self.CATEGORY_COLORS.get(category, None),
                           alpha=0.7)

        ax1.set_ylabel('Percentage of Open Interest (%)', fontsize=11, fontweight='bold')
        ax1.set_title(f'{contract} - Long Positions by Category', fontsize=14, fontweight='bold', pad=15)
        ax1.grid(True, alpha=0.3, linestyle='--', axis='y')
        ax1.legend(loc='upper left', framealpha=0.9, fontsize=9)
        ax1.set_ylim(0, 100)

        # Bottom plot: Short positions
        for category in short_pivot.columns:
            ax2.fill_between(short_pivot.index, 0, short_pivot[category],
                           label=self.CATEGORY_NAMES.get(category, category),
                           color=self.CATEGORY_COLORS.get(category, None),
                           alpha=0.7)

        ax2.set_xlabel('Report Date', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Percentage of Open Interest (%)', fontsize=11, fontweight='bold')
        ax2.set_title(f'{contract} - Short Positions by Category', fontsize=14, fontweight='bold', pad=15)
        ax2.grid(True, alpha=0.3, linestyle='--', axis='y')
        ax2.legend(loc='upper left', framealpha=0.9, fontsize=9)
        ax2.set_ylim(0, 100)

        # Format x-axis
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax2.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
        plt.xticks(rotation=45, ha='right')

        plt.tight_layout()

        # Save or show
        file_path = None
        if save:
            file_path = self.output_dir / f"{contract}_breakdown_{weeks}w.png"
            plt.savefig(file_path, dpi=300, bbox_inches='tight')
            print(f"Saved plot to {file_path}")

        if show:
            plt.show()
        else:
            plt.close()

        return file_path

    def create_all_plots(self, contract: str, weeks: int = 13,
                        show: bool = False) -> List[Path]:
        """
        Create all standard plots for a contract.

        Args:
            contract: Contract code
            weeks: Number of weeks to plot
            show: Whether to display plots

        Returns:
            List of paths to saved plots
        """
        print(f"\nGenerating plots for {contract}...")

        plots = []

        # Net positions plot
        plot_path = self.plot_net_positions(contract, weeks, save=True, show=show)
        if plot_path:
            plots.append(plot_path)

        # Category breakdown
        plot_path = self.plot_category_breakdown(contract, weeks, save=True, show=show)
        if plot_path:
            plots.append(plot_path)

        # Individual category plots for major participants
        for category in ['investment_funds', 'commercial', 'investment_firms']:
            plot_path = self.plot_long_short_positions(contract, category, weeks,
                                                      save=True, show=show)
            if plot_path:
                plots.append(plot_path)

        return plots


if __name__ == '__main__':
    import sys
    from eex_storage import EEXDataStorage

    if len(sys.argv) < 2:
        print("Usage: python eex_visualizer.py <contract> [weeks]")
        sys.exit(1)

    contract = sys.argv[1]
    weeks = int(sys.argv[2]) if len(sys.argv) > 2 else 13

    storage = EEXDataStorage()
    df = storage.load_history(contract)

    if df is None or len(df) == 0:
        print(f"No data found for contract {contract}")
        sys.exit(1)

    visualizer = EEXVisualizer(df)
    plots = visualizer.create_all_plots(contract, weeks)

    print(f"\nGenerated {len(plots)} plots:")
    for plot_path in plots:
        print(f"  - {plot_path}")
