@echo off
REM Quick launcher for EEX CoT Workflow
REM Double-click this file to run the workflow for DEBM and DEPM

echo ================================================================================
echo EEX COMMITMENT OF TRADERS WORKFLOW
echo ================================================================================
echo.

python eex_workflow.py DEBM DEPM --weeks 13

echo.
echo ================================================================================
echo Press any key to exit...
pause >nul
