"""
EEX CoT HTML Report Generator

This module generates an HTML report with positioning tables and charts.
"""
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import base64


class EEXHTMLReport:
    """Generate HTML reports for EEX CoT data."""

    CATEGORY_NAMES = {
        'investment_firms': 'Investment Firms',
        'investment_funds': 'Investment Funds',
        'other_financial': 'Other Financial',
        'commercial': 'Commercial',
        'compliance_operators': 'Compliance Operators'
    }

    CONTRACT_NAMES = {
        # Power Futures
        'ATBM': 'Austrian Power Baseload',
        'DEBM': 'German Power Baseload',
        'DEPM': 'German Power Peak',
        'F7BM': 'French Power Baseload',
        'F7PM': 'French Power Peakload',
        'F9BM': 'Hungarian Power Baseload',
        'FCBM': 'Swiss Power Baseload',
        'FDBM': 'Italian Power Baseload',
        'FEBM': 'Spanish Power Baseload',
        'FEUA': 'EU Emission Allowances (EUA)',
        'FOBM': 'Japanese Tokyo Power Baseload',
        'FQBM': 'Japanese Kansai Power Baseload',
        'FXBM': 'Czech Power Baseload',
        'Q0BM': 'Dutch Power Baseload',
        'Q0PM': 'Dutch Power Peakload',
        'Q1BM': 'Belgian Power Baseload',
        # Natural Gas Futures
        'G0BM': 'THE Natural Gas (Germany)',
        'G3BM': 'TTF Natural Gas',
        'G5BM': 'PEG Natural Gas',
        'G8BM': 'CEGH VTP Natural Gas',
        'GBBM': 'ZTP Natural Gas',
        'GCBM': 'PSV Natural Gas',
        'GEBM': 'PVB Natural Gas',
        # Dry Bulk Freight Futures
        'CPTM': 'Baltic Capesize 5TC Freight',
        'P5TC': 'Baltic Panamax 5TC Freight',
        'PTCM': 'Baltic Panamax 4TC Freight',
        'SPTM': 'Baltic Supramax 10TC Freight',
    }

    def __init__(self, output_dir: str = "reports"):
        """
        Initialize HTML report generator.

        Args:
            output_dir: Directory to save HTML reports
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _get_html_header(self, title: str) -> str:
        """Generate HTML header with CSS styling."""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}

        .header .subtitle {{
            font-size: 1.2em;
            opacity: 0.95;
        }}

        .content {{
            padding: 30px;
        }}

        .contract-section {{
            margin-bottom: 50px;
            border-bottom: 3px solid #e0e0e0;
            padding-bottom: 30px;
        }}

        .contract-section:last-child {{
            border-bottom: none;
        }}

        .contract-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 25px;
        }}

        .contract-header h2 {{
            font-size: 2em;
            margin-bottom: 8px;
        }}

        .contract-info {{
            font-size: 0.95em;
            opacity: 0.95;
        }}

        .summary-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}

        .card {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}

        .card-title {{
            font-size: 0.9em;
            color: #666;
            margin-bottom: 8px;
            font-weight: 600;
            text-transform: uppercase;
        }}

        .card-value {{
            font-size: 1.8em;
            font-weight: bold;
            color: #333;
        }}

        .card-unit {{
            font-size: 0.8em;
            color: #666;
            margin-left: 5px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 25px 0;
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
        }}

        table caption {{
            font-size: 1.3em;
            font-weight: bold;
            padding: 15px;
            text-align: left;
            background: #f8f9fa;
            color: #333;
        }}

        th {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.85em;
            letter-spacing: 0.5px;
        }}

        th.number {{
            text-align: right;
        }}

        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #e0e0e0;
        }}

        td.number {{
            text-align: right;
            font-family: 'Courier New', monospace;
            font-weight: 500;
        }}

        tr:hover {{
            background-color: #f5f5f5;
        }}

        tr:last-child td {{
            border-bottom: none;
        }}

        .positive {{
            color: #2ecc71;
            font-weight: bold;
        }}

        .negative {{
            color: #e74c3c;
            font-weight: bold;
        }}

        .neutral {{
            color: #95a5a6;
        }}

        .charts {{
            margin-top: 40px;
        }}

        .chart-container {{
            margin: 30px 0;
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}

        .chart-title {{
            font-size: 1.3em;
            font-weight: bold;
            margin-bottom: 15px;
            color: #333;
        }}

        .chart-container img {{
            width: 100%;
            height: auto;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}

        .footer {{
            text-align: center;
            padding: 30px;
            background: #f8f9fa;
            color: #666;
            font-size: 0.9em;
            border-top: 1px solid #e0e0e0;
        }}

        .timestamp {{
            margin-top: 10px;
            font-style: italic;
        }}

        @media print {{
            body {{
                background: white;
                padding: 0;
            }}

            .container {{
                box-shadow: none;
            }}

            .contract-section {{
                page-break-after: always;
            }}
        }}
    </style>
</head>
<body>
"""

    def _get_html_footer(self) -> str:
        """Generate HTML footer."""
        return """
    <div class="footer">
        <p><strong>EEX Commitment of Traders Report</strong></p>
        <p>Data Source: European Energy Exchange (EEX) - MiFID II RTS 21</p>
        <p class="timestamp">Generated: {timestamp}</p>
    </div>
</div>
</body>
</html>
""".format(timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def _format_number(self, value: float) -> str:
        """Format number with thousands separator."""
        if pd.isna(value):
            return "0"
        return f"{value:,.0f}"

    def _format_change(self, value: float) -> str:
        """Format change with sign and color class."""
        if pd.isna(value) or value == 0:
            return '<span class="neutral">0</span>'

        sign = '+' if value > 0 else ''
        css_class = 'positive' if value > 0 else 'negative'
        return f'<span class="{css_class}">{sign}{value:,.0f}</span>'

    def _create_position_table(self, df: pd.DataFrame, report_date: str) -> str:
        """Create HTML table for positions."""
        # Filter for total positions on the latest date
        latest = df[
            (df['report_date'] == pd.to_datetime(report_date)) &
            (df['position_type'] == 'total')
        ].copy()

        # Sort by net position descending
        latest = latest.sort_values('net', ascending=False)

        html = """
        <table>
            <caption>Current Positions by Category</caption>
            <thead>
                <tr>
                    <th>Category</th>
                    <th class="number">Long (MW)</th>
                    <th class="number">Short (MW)</th>
                    <th class="number">Net (MW)</th>
                    <th class="number">Long %</th>
                    <th class="number">Short %</th>
                </tr>
            </thead>
            <tbody>
        """

        for _, row in latest.iterrows():
            cat_name = self.CATEGORY_NAMES.get(row['category'], row['category'])
            html += f"""
                <tr>
                    <td><strong>{cat_name}</strong></td>
                    <td class="number">{self._format_number(row['long'])}</td>
                    <td class="number">{self._format_number(row['short'])}</td>
                    <td class="number">{self._format_change(row['net'])}</td>
                    <td class="number">{row['long_pct']:.2f}%</td>
                    <td class="number">{row['short_pct']:.2f}%</td>
                </tr>
            """

        html += """
            </tbody>
        </table>
        """

        return html

    def _create_change_table(self, df: pd.DataFrame, report_date: str) -> str:
        """Create HTML table for weekly changes."""
        latest = df[
            (df['report_date'] == pd.to_datetime(report_date)) &
            (df['position_type'] == 'total')
        ].copy()

        # Sort by net change descending
        latest = latest.sort_values('net_change', ascending=False)

        html = """
        <table>
            <caption>Weekly Changes</caption>
            <thead>
                <tr>
                    <th>Category</th>
                    <th class="number">Long Change (MW)</th>
                    <th class="number">Short Change (MW)</th>
                    <th class="number">Net Change (MW)</th>
                </tr>
            </thead>
            <tbody>
        """

        for _, row in latest.iterrows():
            cat_name = self.CATEGORY_NAMES.get(row['category'], row['category'])
            html += f"""
                <tr>
                    <td><strong>{cat_name}</strong></td>
                    <td class="number">{self._format_change(row['long_change'])}</td>
                    <td class="number">{self._format_change(row['short_change'])}</td>
                    <td class="number">{self._format_change(row['net_change'])}</td>
                </tr>
            """

        html += """
            </tbody>
        </table>
        """

        return html

    def _create_summary_cards(self, df: pd.DataFrame, report_date: str) -> str:
        """Create summary cards with key metrics."""
        latest = df[
            (df['report_date'] == pd.to_datetime(report_date)) &
            (df['position_type'] == 'total')
        ]

        total_long = latest['long'].sum()
        total_short = latest['short'].sum()
        net_position = latest['net'].sum()

        html = """
        <div class="summary-cards">
            <div class="card">
                <div class="card-title">Total Long Positions</div>
                <div class="card-value">{:,.0f}<span class="card-unit">MW</span></div>
            </div>
            <div class="card">
                <div class="card-title">Total Short Positions</div>
                <div class="card-value">{:,.0f}<span class="card-unit">MW</span></div>
            </div>
            <div class="card">
                <div class="card-title">Net Market Position</div>
                <div class="card-value">{:,.0f}<span class="card-unit">MW</span></div>
            </div>
        </div>
        """.format(total_long, total_short, net_position)

        return html

    def _embed_chart(self, chart_path: Path, title: str) -> str:
        """Embed chart image in HTML."""
        if not chart_path.exists():
            return f'<p>Chart not found: {chart_path}</p>'

        # Use relative path for web deployment
        # Assumes plots are copied to reports/plots/
        relative_path = f"./plots/{chart_path.name}"

        html = f"""
        <div class="chart-container">
            <div class="chart-title">{title}</div>
            <img src="{relative_path}" alt="{title}">
        </div>
        """

        return html

    def generate_report(self, contract: str, df: pd.DataFrame,
                       plots_dir: str = "plots") -> Path:
        """
        Generate HTML report for a contract.

        Args:
            contract: Contract code
            df: DataFrame with CoT data
            plots_dir: Directory containing plot images

        Returns:
            Path to generated HTML report
        """
        plots_path = Path(plots_dir)

        # Get latest report date
        latest_date = df['report_date'].max()
        latest_date_str = latest_date.strftime('%Y-%m-%d')

        # Get contract name from data
        contract_name = df[df['report_date'] == latest_date].iloc[0]['contract_code']

        # Build HTML
        html = self._get_html_header(f"CoT Report - {contract}")

        html += """
<div class="container">
    <div class="header">
        <h1>Commitment of Traders Report</h1>
        <div class="subtitle">European Energy Exchange (EEX)</div>
    </div>

    <div class="content">
"""

        # Contract section
        html += f"""
        <div class="contract-section">
            <div class="contract-header">
                <h2>{contract}</h2>
                <div class="contract-info">Report Date: {latest_date_str}</div>
            </div>
"""

        # Summary cards
        html += self._create_summary_cards(df, latest_date_str)

        # Position table
        html += self._create_position_table(df, latest_date_str)

        # Change table
        html += self._create_change_table(df, latest_date_str)

        # Charts section
        html += '<div class="charts">'

        # Net positions chart
        net_chart = plots_path / f"{contract}_net_positions_13w.png"
        if net_chart.exists():
            html += self._embed_chart(net_chart, "Net Positions by Category")

        # Breakdown chart
        breakdown_chart = plots_path / f"{contract}_breakdown_13w.png"
        if breakdown_chart.exists():
            html += self._embed_chart(breakdown_chart, "Long/Short Breakdown by Category")

        # Individual category charts
        for category in ['investment_funds', 'commercial', 'investment_firms']:
            cat_chart = plots_path / f"{contract}_{category}_13w.png"
            if cat_chart.exists():
                cat_name = self.CATEGORY_NAMES.get(category, category)
                html += self._embed_chart(cat_chart, f"{cat_name} - Detailed Positions")

        html += '</div>'  # Close charts
        html += '</div>'  # Close contract-section
        html += '</div>'  # Close content

        # Footer
        html += self._get_html_footer()

        # Save HTML file
        output_file = self.output_dir / f"{contract}_report_{latest_date_str.replace('-', '')}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"Generated HTML report: {output_file}")
        return output_file

    def generate_multi_contract_report(self, contracts_data: Dict[str, pd.DataFrame],
                                      plots_dir: str = "plots") -> Path:
        """
        Generate a single HTML report for multiple contracts.

        Args:
            contracts_data: Dictionary mapping contract codes to DataFrames
            plots_dir: Directory containing plot images

        Returns:
            Path to generated HTML report
        """
        plots_path = Path(plots_dir)

        # Get latest date from first contract
        first_contract = list(contracts_data.keys())[0]
        latest_date = contracts_data[first_contract]['report_date'].max()
        latest_date_str = latest_date.strftime('%Y-%m-%d')

        # Build HTML
        html = self._get_html_header("CoT Report - Multi-Contract")

        html += f"""
<div class="container">
    <div class="header">
        <h1>Commitment of Traders Report</h1>
        <div class="subtitle">European Energy Exchange (EEX) - Report Date: {latest_date_str}</div>
    </div>

    <div class="content">
"""

        # Generate section for each contract
        for contract, df in contracts_data.items():
            html += f"""
        <div class="contract-section">
            <div class="contract-header">
                <h2>{contract}</h2>
                <div class="contract-info">Report Date: {latest_date_str}</div>
            </div>
"""

            # Summary cards
            html += self._create_summary_cards(df, latest_date_str)

            # Position table
            html += self._create_position_table(df, latest_date_str)

            # Change table
            html += self._create_change_table(df, latest_date_str)

            # Charts section
            html += '<div class="charts">'

            # Net positions chart
            net_chart = plots_path / f"{contract}_net_positions_13w.png"
            if net_chart.exists():
                html += self._embed_chart(net_chart, "Net Positions by Category")

            # Breakdown chart
            breakdown_chart = plots_path / f"{contract}_breakdown_13w.png"
            if breakdown_chart.exists():
                html += self._embed_chart(breakdown_chart, "Long/Short Breakdown by Category")

            # Individual category charts
            for category in ['investment_funds', 'commercial', 'investment_firms']:
                cat_chart = plots_path / f"{contract}_{category}_13w.png"
                if cat_chart.exists():
                    cat_name = self.CATEGORY_NAMES.get(category, category)
                    html += self._embed_chart(cat_chart, f"{cat_name} - Detailed Positions")

            html += '</div>'  # Close charts
            html += '</div>'  # Close contract-section

        html += '</div>'  # Close content

        # Footer
        html += self._get_html_footer()

        # Save HTML file
        output_file = self.output_dir / f"cot_report_{latest_date_str.replace('-', '')}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"\nGenerated multi-contract HTML report: {output_file}")
        return output_file


if __name__ == '__main__':
    import sys
    from eex_storage import EEXDataStorage

    if len(sys.argv) < 2:
        print("Usage: python eex_html_report.py <contract1> [contract2] ...")
        print("\nExample:")
        print("  python eex_html_report.py DEBM DEPM")
        sys.exit(1)

    contracts = sys.argv[1:]

    storage = EEXDataStorage()
    report_gen = EEXHTMLReport()

    if len(contracts) == 1:
        # Single contract report
        contract = contracts[0]
        df = storage.load_history(contract)

        if df is None or len(df) == 0:
            print(f"No data found for contract {contract}")
            sys.exit(1)

        report_path = report_gen.generate_report(contract, df)
        print(f"\nReport saved to: {report_path}")
        print(f"Open in browser: file:///{report_path.absolute()}")

    else:
        # Multi-contract report
        contracts_data = {}
        for contract in contracts:
            df = storage.load_history(contract)
            if df is not None and len(df) > 0:
                contracts_data[contract] = df
            else:
                print(f"Warning: No data found for contract {contract}")

        if contracts_data:
            report_path = report_gen.generate_multi_contract_report(contracts_data)
            print(f"\nReport saved to: {report_path}")
            print(f"Open in browser: file:///{report_path.absolute()}")
        else:
            print("No data found for any contracts")
            sys.exit(1)
