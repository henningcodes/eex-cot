@echo off
echo ================================================================
echo Adding All New Contracts with Tabbed Interface
echo ================================================================
echo.

echo Step 1: Pulling latest changes from GitHub...
git pull

echo.
echo Step 2: Adding new files...
git add .github/workflows/weekly_cot_report.yml
git add eex_html_report.py
git add eex_html_report_tabbed.py
git add eex_workflow.py
git add generate_report.py
git add update_for_all_contracts.bat

echo.
echo Step 3: Committing changes...
git commit -m "Add all contracts with tabbed HTML interface"

echo.
echo Step 4: Pushing to GitHub...
git push

echo.
echo ================================================================
echo Done! Changes pushed to GitHub.
echo.
echo Next steps:
echo 1. Go to GitHub Actions
echo 2. Run the workflow manually
echo 3. View your tabbed report at: https://henner247.github.io/eex-cot/
echo ================================================================
pause
