# EEX CoT Analysis - Complete Project Summary

## What This System Does

This project provides a complete, automated workflow for analyzing Commitment of Traders (CoT) reports from the European Energy Exchange (EEX). It's designed to run every Tuesday when new reports are published.

### The Complete Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    TUESDAY MORNING (9:00 AM)                     │
│                                                                   │
│  1. Downloads latest reports from EEX website                    │
│     └─> DEBM (German Base), DEPM (German Peak), etc.            │
│                                                                   │
│  2. Parses complex Excel files                                   │
│     └─> Extracts 13 weeks of historical data per file           │
│                                                                   │
│  3. Stores data in local database (CSV)                          │
│     └─> Appends new data, removes duplicates                    │
│                                                                   │
│  4. Generates detailed analysis                                  │
│     └─> Current positions, weekly changes, percentages          │
│                                                                   │
│  5. Creates visualizations (10 charts)                           │
│     └─> Net positions, breakdowns, category details             │
│                                                                   │
│  6. Generates HTML report                                        │
│     └─> Beautiful report with tables and embedded charts        │
│                                                                   │
│  Result: Complete analysis ready to view!                        │
└─────────────────────────────────────────────────────────────────┘
```

## Key Deliverables

### 1. HTML Report (PRIMARY OUTPUT)
**Location**: `reports/cot_report_YYYYMMDD.html`

**Contains**:
- ✅ Summary cards (total positions)
- ✅ Current positioning table for all categories
- ✅ Weekly changes table (color-coded)
- ✅ 10 embedded charts
- ✅ Professional design
- ✅ Print-ready

**Usage**:
- Open in browser for instant overview
- Email to colleagues
- Save to shared drive
- Archive for historical reference

### 2. Console Analysis
Real-time analysis printed during execution showing:
- Market totals (long/short/net)
- Category breakdown with changes
- Percentage of open interest

### 3. Charts (PNG files)
**Location**: `plots/`

**Generated Charts per Contract**:
1. Net positions (all categories over time)
2. Category breakdown (stacked area charts)
3. Investment Funds detail
4. Commercial detail
5. Investment Firms detail

Total: 5 charts × 2 contracts = 10 charts

### 4. Historical Database
**Location**: `data/`

CSV files with complete history:
- All positions (long/short/net)
- Weekly changes
- Percentages
- Multiple weeks preserved

## Trader Categories Analyzed

Reports show positioning for 5 categories:

1. **Investment Firms** - Banks, brokers, proprietary trading
2. **Investment Funds** - Asset managers, hedge funds, ETFs
3. **Other Financial** - Insurance, pension funds
4. **Commercial** - Energy producers, suppliers, utilities
5. **Compliance Operators** - EU ETS participants

## What You Learn From the Reports

### Market Structure
- Who holds the most positions (usually Commercial)
- How much speculation vs. hedging (Financial vs. Commercial)
- Open interest concentration

### Positioning Changes
- Which categories are adding/reducing positions
- Trend identification (momentum, reversals)
- Sentiment shifts

### Extreme Positioning
- Unusually large net long/short positions
- Historical extremes
- Potential reversal points

## Usage Patterns

### Weekly Routine (Automated)
```
Tuesday 9:00 AM: Scheduler runs workflow
                 ↓
Tuesday 9:05 AM: Check email or shared drive for HTML report
                 ↓
Tuesday 9:10 AM: Review positioning and changes
                 ↓
Weekly Done!
```

### Manual Analysis
```bash
# Quick weekly update
python eex_workflow.py DEBM DEPM

# Look at longer history
python eex_workflow.py DEBM DEPM --weeks 26

# Regenerate report only
python generate_report.py DEBM DEPM --open
```

### Historical Comparison
```bash
# Analyze specific contract
python eex_analyzer.py DEBM

# Generate custom timeframe charts
python eex_visualizer.py DEBM 52  # Full year
```

## File Organization

```
eex-cot/
│
├── 📊 reports/              ← PRIMARY: Open HTML reports here
│   └── cot_report_20260123.html
│
├── 📈 plots/                ← Charts (also in HTML report)
│   ├── DEBM_net_positions_13w.png
│   └── ...
│
├── 💾 data/                 ← Historical database
│   ├── DEBM_history.csv
│   └── DEPM_history.csv
│
├── 📝 logs/                 ← Execution logs
│   └── workflow_20260127_150000.log
│
└── 🐍 Python scripts        ← Source code
    ├── eex_workflow.py
    ├── generate_report.py
    └── ...
```

## Quick Commands Reference

```bash
# Full workflow (recommended)
python eex_workflow.py DEBM DEPM

# Update data only
python eex_workflow.py DEBM DEPM --update-only

# Force redownload
python eex_workflow.py DEBM DEPM --force

# More history in charts
python eex_workflow.py DEBM DEPM --weeks 26

# Generate HTML report from existing data
python generate_report.py DEBM DEPM

# Open report in browser automatically
python generate_report.py DEBM DEPM --open

# Quick analysis
python eex_analyzer.py DEBM

# Custom visualization
python eex_visualizer.py DEBM 20

# Windows quick launcher
run_workflow.bat
```

## Automation Setup

### Windows Task Scheduler
1. Open Task Scheduler
2. Import or create task:
   - Name: "EEX CoT Weekly Update"
   - Trigger: Weekly, Tuesday, 9:00 AM
   - Action: `python schedule_tuesday.py`
   - Start in: Project directory
3. Done - runs automatically every Tuesday

Logs saved to: `logs/workflow_YYYYMMDD_HHMMSS.log`

## System Capabilities

### ✅ What It Does
- Downloads latest reports automatically
- Parses complex Excel formats
- Maintains historical database
- Detects and removes duplicates
- Calculates weekly changes
- Generates professional visualizations
- Creates shareable HTML reports
- Archives weekly reports
- Logs all operations

### ✅ Extensible
- Easy to add more contracts (F7BM, ATBM, etc.)
- Customizable time periods
- Modular design (use components independently)
- Clean, documented code

### ✅ Reliable
- Error handling throughout
- Data validation
- Graceful failures
- Logging for troubleshooting

## Data Source

**Official EEX Publication Site:**
https://public.eex-group.com/eex/mifid2/rts-21/index.html

**Update Schedule:**
- Published weekly (typically Tuesday morning)
- Reports previous Thursday's positions
- 13 weeks of historical data per file

**Data Quality:**
- Official regulatory reporting (MiFID II)
- Verified by EEX
- Comprehensive market coverage

## Use Cases

### 1. Market Monitoring
Track weekly changes in energy market positioning

### 2. Trend Analysis
Identify accumulation/distribution patterns over time

### 3. Sentiment Indicators
Financial vs. Commercial positioning as market signal

### 4. Research & Reporting
Historical database for quantitative analysis

### 5. Portfolio Management
Monitor market participant behavior for timing decisions

### 6. Team Sharing
Distribute weekly HTML reports to stakeholders

## Technical Specifications

**Language**: Python 3.8+

**Key Libraries**:
- pandas (data manipulation)
- matplotlib (visualization)
- openpyxl (Excel reading)
- beautifulsoup4 (web scraping)

**Data Format**:
- Storage: CSV (portable, Excel-compatible)
- Output: HTML5 + embedded PNG charts
- Charts: High-resolution PNG (300 DPI)

**Performance**:
- Download: 2-5 seconds per contract
- Processing: 5-10 seconds per contract
- Chart generation: 10-15 seconds total
- HTML report: 1-2 seconds
- **Total runtime: ~30 seconds for 2 contracts**

## Documentation

- **[README.md](README.md)** - Complete documentation
- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute setup guide
- **[HTML_REPORT_GUIDE.md](HTML_REPORT_GUIDE.md)** - HTML report details
- **This file** - Project overview

## Example Insights

### From Recent Report (Jan 23, 2026)

**DEBM (German Base Power)**:
- Commercial: Net long 21.9M MW (down 8.6M from last week)
- Investment Funds: Net short 21.7M MW (short position increased)
- Investment Firms: Roughly balanced

**Interpretation**:
- Commercial hedgers reducing long exposure
- Financial players increasing short positions
- Potential bearish sentiment or mean reversion

**Action Items**:
- Monitor if trend continues next week
- Compare to price movements
- Check if positions at historical extremes

## Success Metrics

After setup, you should have:
- ✅ Automated Tuesday reports
- ✅ Growing historical database (13+ weeks)
- ✅ Weekly HTML reports for distribution
- ✅ Complete visualization library
- ✅ Console analysis for quick checks
- ✅ Audit trail in logs

## Support

For issues or questions:
1. Check [README.md](README.md) for detailed usage
2. Review error logs in `logs/` directory
3. Verify data files exist in `data/` and `plots/`
4. Ensure Python packages are installed
5. Check EEX website accessibility

## Next Steps

### Immediate
1. ✅ Install dependencies (`pip install -r requirements.txt`)
2. ✅ Run first workflow (`python eex_workflow.py DEBM DEPM`)
3. ✅ Open HTML report in browser
4. ✅ Set up Task Scheduler (optional)

### Ongoing
- Review reports every Tuesday
- Build historical database
- Compare week-over-week changes
- Identify positioning patterns

### Advanced
- Add more contracts (F7BM, ATBM, CPTM)
- Extend time periods (--weeks 26, 52)
- Custom analysis in Python
- Integrate with other data sources

---

**Version**: 1.0
**Date**: January 2026
**Status**: Production Ready
**Platform**: Windows (adaptable to Linux/Mac)

**Happy analyzing!** 📊📈💹
