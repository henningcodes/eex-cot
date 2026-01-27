# EEX Commitment of Traders (CoT) Analysis Workflow

A comprehensive Python workflow for downloading, analyzing, and visualizing Commitment of Traders reports from the European Energy Exchange (EEX).

## Overview

This project automates the analysis of MiFID II RTS 21 weekly position reports published by EEX. It downloads the latest data, parses Excel files, stores historical data, and generates detailed analysis and visualizations.

## Features

- **Automated Data Download**: Scrapes the EEX public website for the latest CoT reports
- **Excel Parsing**: Extracts position data from complex Excel formats
- **Historical Data Storage**: Maintains a local database of historical positions
- **Comprehensive Analysis**: Calculates current positions, weekly changes, and trends
- **Rich Visualizations**: Generates multiple charts showing positioning over time
- **HTML Reports**: Beautiful, self-contained HTML reports with tables and embedded charts
- **Scheduled Execution**: Can be configured to run automatically every Tuesday

## Supported Contracts

Currently configured for German power contracts:
- **DEBM** - EEX German Power Base Future
- **DEPM** - EEX German Power Peak Future

The system is designed to be easily extended to other EEX contracts (e.g., ATBM, CPTM, F7BM, F7PM).

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone or download this repository

2. Install required packages:
```bash
pip install -r requirements.txt
```

The main dependencies are:
- pandas (data manipulation)
- openpyxl (Excel file reading)
- matplotlib (visualization)
- requests (HTTP requests)
- beautifulsoup4 (HTML parsing)
- lxml (XML/HTML processing)

## Usage

### Quick Start

Run the complete workflow for DEBM and DEPM contracts:

```bash
python eex_workflow.py DEBM DEPM
```

This will:
1. Download the latest reports from EEX
2. Parse the Excel files
3. Store data in the `data/` directory
4. Generate analysis (printed to console)
5. Create visualizations in the `plots/` directory

### Command-Line Options

```bash
# Show 20 weeks of historical data
python eex_workflow.py DEBM DEPM --weeks 20

# Force redownload even if files exist
python eex_workflow.py DEBM --force

# Use custom directories
python eex_workflow.py DEBM --data-dir ./my_data --plots-dir ./my_plots

# Update data only (no analysis/plots)
python eex_workflow.py DEBM DEPM --update-only
```

### Individual Modules

You can also use individual modules independently:

**Download files:**
```bash
python eex_downloader.py DEBM,DEPM
```

**Parse an Excel file:**
```bash
python eex_parser.py WPR_2026-01-23_DEBM_COMB_260127080028.xlsx
```

**Analyze stored data:**
```bash
python eex_analyzer.py DEBM
```

**Generate visualizations:**
```bash
python eex_visualizer.py DEBM 13
```

## Scheduling (Windows)

To run the workflow automatically every Tuesday:

### Using Windows Task Scheduler

1. Open Task Scheduler
2. Create a new task:
   - **Name**: EEX CoT Weekly Update
   - **Trigger**: Weekly, every Tuesday at 9:00 AM
   - **Action**: Start a program
     - Program: `python`
     - Arguments: `"C:\path\to\schedule_tuesday.py"`
     - Start in: `C:\path\to\eex-cot`

The script will log all output to `logs/workflow_YYYYMMDD_HHMMSS.log`

### Manual Tuesday Run

```bash
python schedule_tuesday.py
```

## Output

### Data Storage

Historical data is stored in CSV format in the `data/` directory:
- `data/DEBM_history.csv` - DEBM historical positions
- `data/DEPM_history.csv` - DEPM historical positions

Each file contains:
- Report dates
- Categories (Investment Firms, Investment Funds, Commercial, etc.)
- Long/Short positions
- Net positions
- Weekly changes
- Percentage of open interest

### Analysis Output

The workflow prints detailed analysis to the console including:

1. **Overall Market Summary**
   - Total long/short positions
   - Net position

2. **Category Breakdown**
   - Positions by trader category
   - Weekly changes
   - Percentage of open interest

3. **Trader Categories**
   - Investment Firms or credit institutions
   - Investment Funds
   - Other Financial Institutions
   - Commercial Undertakings
   - Operators with compliance obligations (Directive 2003/87/EC)

### Visualizations

Generated plots are saved to the `plots/` directory:

**For each contract:**

1. **Net Positions Chart** (`{CONTRACT}_net_positions_13w.png`)
   - Shows net positioning for all categories over time
   - Helps identify positioning trends

2. **Category Breakdown** (`{CONTRACT}_breakdown_13w.png`)
   - Stacked area charts showing percentage composition
   - Separate views for long and short positions

3. **Individual Category Charts** (e.g., `{CONTRACT}_investment_funds_13w.png`)
   - Long and short positions for specific category
   - Net position bar chart
   - Generated for major participants (Investment Funds, Commercial, Investment Firms)

### HTML Reports

**Automatically generated** with each workflow run, saved to the `reports/` directory.

The HTML report (`cot_report_YYYYMMDD.html`) contains:

1. **Summary Cards**: Quick overview with total long/short/net positions
2. **Position Tables**: Current positions for each trader category with percentages
3. **Weekly Change Tables**: Color-coded changes (green=positive, red=negative)
4. **Embedded Charts**: All visualizations integrated into the report

**Features:**
- Professional design with gradient styling
- Responsive layout (works on desktop and mobile)
- Self-contained and shareable
- Print-friendly for PDF export
- Numbers formatted with thousands separators

**Viewing the Report:**
- Open the HTML file in any browser
- Or copy the `file:///` URL from console output
- Or use: `python generate_report.py DEBM DEPM --open`

**Generate Reports Manually:**
```bash
# Generate from existing data
python generate_report.py DEBM DEPM

# Generate and open in browser
python generate_report.py DEBM DEPM --open
```

See [HTML_REPORT_GUIDE.md](HTML_REPORT_GUIDE.md) for detailed information.

## Project Structure

```
eex-cot/
├── eex_workflow.py          # Main workflow orchestrator
├── eex_downloader.py         # Web scraper for EEX website
├── eex_parser.py             # Excel file parser
├── eex_storage.py            # Data storage manager
├── eex_analyzer.py           # Analysis functions
├── eex_visualizer.py         # Visualization generator
├── eex_html_report.py        # HTML report generator
├── generate_report.py        # Standalone report generator
├── schedule_tuesday.py       # Scheduled execution script
├── run_workflow.bat          # Quick launcher (Windows)
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── QUICKSTART.md             # Quick start guide
├── HTML_REPORT_GUIDE.md      # HTML report documentation
│
├── data/                     # Historical data storage (CSV)
│   ├── DEBM_history.csv
│   └── DEPM_history.csv
│
├── plots/                    # Generated visualizations
│   ├── DEBM_net_positions_13w.png
│   ├── DEBM_breakdown_13w.png
│   └── ...
│
├── reports/                  # HTML reports
│   ├── cot_report_20260123.html
│   └── ...
│
└── logs/                     # Execution logs (from scheduler)
    └── workflow_YYYYMMDD_HHMMSS.log
```

## Data Source

Data is downloaded from:
https://public.eex-group.com/eex/mifid2/rts-21/index.html

This is the official EEX publication site for MiFID II RTS 21 weekly position reports.

## Understanding the Data

### Position Types

Each report contains three types of positions:
- **Risk Reducing**: Positions directly related to commercial activities
- **Other**: Speculative or non-commercial positions
- **Total**: Sum of risk reducing and other positions

### Trader Categories

The reports classify market participants into five categories based on MiFID II regulations:

1. **Investment Firms or Credit Institutions**: Banks and investment firms
2. **Investment Funds**: Asset managers and funds
3. **Other Financial Institutions**: Insurance companies, pension funds, etc.
4. **Commercial Undertakings**: Energy producers, suppliers, traders
5. **Compliance Operators**: Entities with obligations under EU ETS (Directive 2003/87/EC)

### Interpreting Net Positions

- **Positive Net**: More long than short (bullish positioning)
- **Negative Net**: More short than long (bearish positioning)
- **Weekly Changes**: Indicate shifts in sentiment or positioning

## Extending the System

### Adding More Contracts

To analyze additional contracts (e.g., French power, Austrian power):

1. Edit `schedule_tuesday.py` or your workflow command:
```python
contracts = ['DEBM', 'DEPM', 'F7BM', 'F7PM', 'ATBM']
```

2. Run the workflow - it will automatically download and process the new contracts

### Customizing Analysis

You can modify the analysis modules:
- `eex_analyzer.py` - Add custom metrics or comparisons
- `eex_visualizer.py` - Create new chart types or layouts

## Troubleshooting

### Common Issues

**Missing packages:**
```bash
pip install -r requirements.txt
```

**Download fails:**
- Check internet connection
- Verify the EEX website is accessible
- The website may be temporarily down (try again later)

**Encoding errors:**
- Make sure you're using Python 3.8+
- The code uses UTF-8 encoding for file operations

**No data for a contract:**
- Verify the contract code is correct (4 characters, uppercase)
- Check if the contract is available on the EEX website
- Run with `--force` to redownload files

## License

This project is for personal use and analysis. Please respect the terms of use for the EEX public data.

## Disclaimer

This tool is for informational and analytical purposes only. It does not constitute financial advice. Always verify data and analysis independently before making trading or investment decisions.

## Contact

For issues, improvements, or questions about this workflow, please create an issue or contact the maintainer.

---

**Version**: 1.0
**Last Updated**: January 2026
**Data Source**: European Energy Exchange (EEX) - MiFID II RTS 21 Reports
