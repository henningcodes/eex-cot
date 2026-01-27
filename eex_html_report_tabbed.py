"""
EEX CoT HTML Report Generator with Tabbed Interface

This module generates an HTML report with tabbed interface for multiple contracts.
"""
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Dict
import sys

# Import the base class
from eex_html_report import EEXHTMLReport


class EEXHTMLReportTabbed(EEXHTMLReport):
    """Generate tabbed HTML reports for multiple EEX CoT contracts."""

    def generate_multi_contract_report(self, contracts_data: Dict[str, pd.DataFrame],
                                      plots_dir: str = "plots") -> Path:
        """
        Generate a tabbed HTML report for multiple contracts.

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

        # Build HTML with tabs
        html = self._get_tabbed_html_header(f"CoT Report - Multi-Contract")

        html += f"""
<div class="container">
    <div class="header">
        <h1>Commitment of Traders Report</h1>
        <div class="subtitle">European Energy Exchange (EEX) - Report Date: {latest_date_str}</div>
    </div>

    <div class="tabs">
"""

        # Generate tab buttons
        for idx, contract in enumerate(contracts_data.keys()):
            contract_name = self.CONTRACT_NAMES.get(contract, contract)
            active_class = ' active' if idx == 0 else ''
            html += f'        <button class="tab-button{active_class}" onclick="openTab(event, \'{contract}\')">{contract} - {contract_name}</button>\n'

        html += '    </div>\n\n'

        # Generate tab content for each contract
        for idx, (contract, df) in enumerate(contracts_data.items()):
            active_style = ' style="display:block"' if idx == 0 else ''
            contract_name = self.CONTRACT_NAMES.get(contract, contract)

            html += f"""
    <div id="{contract}" class="tab-content"{active_style}>
        <div class="content">
            <div class="contract-header-inline">
                <h2>{contract} - {contract_name}</h2>
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
            html += '</div>'  # Close content
            html += '</div>'  # Close tab-content

        html += '</div>'  # Close container

        # Footer
        html += self._get_html_footer()

        # Save HTML file
        output_file = self.output_dir / f"cot_report_{latest_date_str.replace('-', '')}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"\nGenerated multi-contract HTML report: {output_file}")
        return output_file

    def _get_tabbed_html_header(self, title: str) -> str:
        """Generate HTML header with CSS styling for tabs."""
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

        /* Tab Styles */
        .tabs {{
            display: flex;
            flex-wrap: wrap;
            background: #f8f9fa;
            border-bottom: 2px solid #667eea;
            padding: 10px 10px 0 10px;
            gap: 5px;
        }}

        .tab-button {{
            background: #e0e0e0;
            border: none;
            padding: 12px 20px;
            cursor: pointer;
            font-size: 0.95em;
            font-weight: 600;
            color: #555;
            border-radius: 8px 8px 0 0;
            transition: all 0.3s;
            white-space: nowrap;
        }}

        .tab-button:hover {{
            background: #d0d0d0;
            color: #333;
        }}

        .tab-button.active {{
            background: white;
            color: #667eea;
            border-bottom: 3px solid #667eea;
        }}

        .tab-content {{
            display: none;
        }}

        .content {{
            padding: 30px;
        }}

        .contract-header-inline {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 25px;
        }}

        .contract-header-inline h2 {{
            font-size: 1.8em;
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

            .tabs {{
                display: none;
            }}

            .tab-content {{
                display: block !important;
                page-break-after: always;
            }}
        }}

        @media (max-width: 768px) {{
            .tabs {{
                flex-direction: column;
            }}

            .tab-button {{
                border-radius: 4px;
                margin-bottom: 5px;
            }}
        }}
    </style>
    <script>
        function openTab(evt, contractName) {{
            var i, tabcontent, tabbuttons;

            // Hide all tab content
            tabcontent = document.getElementsByClassName("tab-content");
            for (i = 0; i < tabcontent.length; i++) {{
                tabcontent[i].style.display = "none";
            }}

            // Remove active class from all buttons
            tabbuttons = document.getElementsByClassName("tab-button");
            for (i = 0; i < tabbuttons.length; i++) {{
                tabbuttons[i].className = tabbuttons[i].className.replace(" active", "");
            }}

            // Show current tab and mark button as active
            document.getElementById(contractName).style.display = "block";
            evt.currentTarget.className += " active";
        }}
    </script>
</head>
<body>
"""


if __name__ == '__main__':
    # Test with imported base functionality
    print("Tabbed HTML Report Generator ready")
