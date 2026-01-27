# HTML Report Guide

## Overview

The EEX CoT workflow now automatically generates a beautiful HTML report that includes:

- **Summary Cards**: Total long, short, and net positions at a glance
- **Position Tables**: Current positions for each trader category
- **Weekly Change Tables**: See how positions changed from last week
- **Interactive Charts**: All generated visualizations embedded in the report

## Automatic Generation

The HTML report is **automatically generated** when you run the full workflow:

```bash
python eex_workflow.py DEBM DEPM
```

After completion, the report location will be shown:
```
HTML report: c:\Users\Henning\claudecode\eex-cot\reports\cot_report_20260123.html
Open in browser: file:///c:\Users\Henning\claudecode\eex-cot\reports\cot_report_20260123.html
```

## Manual Report Generation

You can generate the HTML report at any time from stored data without re-downloading or reprocessing:

```bash
# Generate report for one or more contracts
python generate_report.py DEBM DEPM

# Generate and automatically open in browser
python generate_report.py DEBM DEPM --open
```

This is useful when:
- You want to regenerate the report with the same data
- You want a different format or subset of contracts
- You're reviewing historical data

## Opening the Report

### Option 1: Copy the URL
Copy the `file:///` URL from the console output and paste it into your browser

### Option 2: Double-click
Navigate to the `reports/` folder and double-click the HTML file

### Option 3: Use --open flag
```bash
python generate_report.py DEBM DEPM --open
```

## Report Contents

### For Each Contract

**1. Summary Cards (Top)**
- Total Long Positions (in MW)
- Total Short Positions (in MW)
- Net Market Position (in MW)

**2. Current Positions Table**
Shows for each trader category:
- Long positions (MW)
- Short positions (MW)
- Net position (MW)
- Percentage of total open interest

**3. Weekly Changes Table**
Shows the change from previous week:
- Long change (MW)
- Short change (MW)
- Net change (MW)

Positive changes are shown in **green**, negative in **red**

**4. Charts Section**
All visualizations are embedded:
- Net Positions by Category (line chart)
- Long/Short Breakdown (stacked area chart)
- Detailed views for Investment Funds, Commercial, and Investment Firms

## Report Features

### Visual Design
- Professional gradient header
- Color-coded changes (green for positive, red for negative)
- Responsive layout that works on mobile
- Print-friendly CSS for generating PDFs

### Data Formatting
- Numbers formatted with thousands separators (e.g., 311,333,244)
- Percentages shown to 2 decimal places
- Sign indicators for changes (+/-)

### Multi-Contract Support
When you generate a report for multiple contracts (e.g., DEBM and DEPM), they're combined into a single HTML file with sections for each contract.

## File Naming

Reports are named with the date:
```
cot_report_YYYYMMDD.html
```

For example:
- `cot_report_20260123.html` - Report for January 23, 2026

## Location

Reports are saved to the `reports/` directory in your project folder:
```
eex-cot/
├── reports/
│   ├── cot_report_20260123.html
│   ├── cot_report_20260116.html
│   └── ...
```

## Sharing Reports

The HTML report is **self-contained** with embedded images, making it easy to:

- Email to colleagues
- Save to a shared drive
- Archive for historical reference
- Print to PDF (use your browser's print function)

**Note**: Chart images are referenced by file path, so for portability, share the entire folder structure or use absolute paths.

## Tips

### Tip 1: Create a Desktop Shortcut
Create a shortcut to quickly open the latest report:
1. Right-click on the HTML file
2. Create shortcut
3. Move to desktop or pin to taskbar

### Tip 2: Automatic Weekly Archive
The scheduler saves reports with dates, so each week's report is preserved:
- `cot_report_20260123.html`
- `cot_report_20260130.html`
- `cot_report_20260206.html`

### Tip 3: Comparing Weeks
Open multiple report HTML files in different browser tabs to compare positioning changes across weeks.

### Tip 4: Generate Report with Different Time Periods
If you want to see more weeks in the charts:
```bash
# First regenerate plots with more weeks
python eex_visualizer.py DEBM 26

# Then generate report
python generate_report.py DEBM
```

## Troubleshooting

**Charts not showing?**
- Make sure the `plots/` folder exists and contains PNG files
- The report references charts by relative path from the reports/ folder

**No data in tables?**
- Run the workflow first: `python eex_workflow.py DEBM DEPM`
- Check that CSV files exist in `data/` folder

**Report looks broken?**
- Make sure you're opening in a modern browser (Chrome, Firefox, Edge, Safari)
- Try refreshing the page (F5)

## Example Output

### Summary Cards
```
┌─────────────────────────┐  ┌─────────────────────────┐  ┌─────────────────────────┐
│ Total Long Positions    │  │ Total Short Positions   │  │ Net Market Position     │
│                         │  │                         │  │                         │
│  311,333,244 MW        │  │  311,333,244 MW        │  │          0 MW          │
└─────────────────────────┘  └─────────────────────────┘  └─────────────────────────┘
```

### Position Table
```
Category            Long (MW)      Short (MW)     Net (MW)        Long %   Short %
Commercial       257,331,824    235,468,105    21,863,719      82.65%    75.63%
Investment Firms  15,700,551     15,358,353       342,198       5.04%     4.93%
Investment Funds  37,555,302     59,283,269   -21,727,967      12.06%    19.04%
...
```

### Weekly Changes
```
Category            Long Change    Short Change   Net Change
Commercial              +876,814      +9,494,562   -8,617,748
Investment Firms      +1,091,233        +198,699     +892,534
Investment Funds      +6,058,639      -1,832,026   +7,890,665
...
```

---

**Happy reporting!** 📊📈

For questions or issues, refer to the main [README.md](README.md)
