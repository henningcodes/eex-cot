# Quick Start Guide - EEX CoT Analysis

## 5-Minute Setup

### Step 1: Install Dependencies (First Time Only)

Open a terminal in this directory and run:

```bash
pip install -r requirements.txt
```

### Step 2: Run the Workflow

**Option A - Double-click (Windows):**
- Double-click `run_workflow.bat`

**Option B - Command line:**
```bash
python eex_workflow.py DEBM DEPM
```

That's it! The workflow will:
1. Download the latest reports from EEX
2. Parse and store the data
3. Generate analysis (shown in console)
4. Create visualizations in the `plots/` folder
5. Generate an HTML report in the `reports/` folder

## What You Get

### Console Output
You'll see a detailed analysis including:
- Current positions for each trader category
- Weekly changes
- Percentage of total open interest

### HTML Report (in reports/ folder)
A beautiful, shareable report with:
- **Summary cards** showing total positions at a glance
- **Position tables** with current data for all categories
- **Weekly change tables** with color-coded changes
- **All charts embedded** in one convenient page

**Open the report:**
- Look for the file path at the end of the workflow output
- Copy the `file:///` URL and paste into your browser
- Or navigate to `reports/` folder and double-click the HTML file

### Visualizations (in plots/ folder)
For each contract:
- **Net Positions Chart** - Historical net positioning trends
- **Category Breakdown** - Long/short composition over time
- **Individual Category Charts** - Detailed views for major traders

### Data Files (in data/ folder)
- Historical position data in CSV format
- Automatically maintained and updated

## Viewing Previous Data

After the first run, you have historical data stored. View it with:

```bash
# Show analysis
python eex_analyzer.py DEBM

# Regenerate plots for different time periods
python eex_visualizer.py DEBM 20  # 20 weeks of history
```

## Setting Up Weekly Automation

To run this automatically every Tuesday:

### Windows Task Scheduler

1. Open **Task Scheduler** (search in Start menu)
2. Click **Create Basic Task**
3. Name: "EEX CoT Weekly Update"
4. Trigger: **Weekly**, select **Tuesday**, choose a time (e.g., 9:00 AM)
5. Action: **Start a program**
   - Program: `python`
   - Add arguments: `"schedule_tuesday.py"`
   - Start in: `C:\Users\Henning\claudecode\eex-cot` (your project path)
6. Click **Finish**

Logs will be saved to the `logs/` folder.

## Common Commands

```bash
# Run for different contracts
python eex_workflow.py DEBM DEPM F7BM ATBM

# Show 26 weeks of data
python eex_workflow.py DEBM --weeks 26

# Force redownload (if data seems stale)
python eex_workflow.py DEBM --force

# Just update data, don't regenerate plots
python eex_workflow.py DEBM --update-only
```

## Example Output

### DEBM Analysis (Sample)
```
COMMITMENT OF TRADERS REPORT - DEBM
Report Date: 2026-01-23

OVERALL MARKET:
  Total Long:       311,333,244 MW
  Total Short:      311,333,244 MW
  Net Position:               0 MW

CATEGORY                             LONG           SHORT             NET          CHG
Commercial                    257,331,824     235,468,105      21,863,719   -8,617,748
Investment Firms               15,700,551      15,358,353         342,198      892,534
Investment Funds               37,555,302      59,283,269     -21,727,967    7,890,665
```

## Understanding the Charts

### Net Positions Chart
- Shows if each category is net long (above 0) or net short (below 0)
- Trends show sentiment changes over time
- Commercial traders typically hedge (variable positioning)
- Financial traders may show momentum trends

### Category Breakdown
- Stacked areas show market composition
- Commercial traders usually dominate (largest share)
- Financial players' share indicates speculative interest

### Individual Category Charts
- Top: Absolute long and short positions
- Bottom: Net position (bars colored by direction)
- Helps identify positioning extremes and reversals

## Key Insights to Look For

1. **Extreme Positioning**: When a category reaches unusually high/low net position
2. **Position Changes**: Large weekly changes may signal sentiment shifts
3. **Commercial vs Financial**: Divergence can indicate market dynamics
4. **Investment Fund Flows**: Often tracks price momentum

## Troubleshooting

**"No module named 'pandas'"**
→ Run: `pip install -r requirements.txt`

**"No data found for contract"**
→ Make sure you ran the workflow first to download data

**No plots appearing**
→ Check the `plots/` folder - files are saved there (not displayed)

**Downloads fail**
→ Check internet connection and try again (EEX site may be temporarily unavailable)

## Next Steps

- Set up weekly automation (see above)
- Add more contracts by editing the command or `schedule_tuesday.py`
- Review the [README.md](README.md) for detailed documentation
- Explore individual modules for custom analysis

## Questions?

Check the [README.md](README.md) for full documentation or review the source code - each module is well-commented and can be run independently.

---

**Happy analyzing!** 📊
