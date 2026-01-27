"""
Detailed exploration of EEX CoT Excel files
"""
import pandas as pd
import sys

if len(sys.argv) > 1:
    file_path = sys.argv[1]
else:
    file_path = "WPR_2026-01-23_DEBM_COMB_260127080028.xlsx"

print(f"Analyzing file: {file_path}")
print("=" * 80)

# Read the first sheet in detail
df = pd.read_excel(file_path, sheet_name='Weekly_Report', header=None)

print("\nRaw data (all rows):")
print(df.to_string())
