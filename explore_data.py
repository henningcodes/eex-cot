"""
Script to explore the structure of EEX CoT Excel files
"""
import pandas as pd
import sys

if len(sys.argv) > 1:
    file_path = sys.argv[1]
else:
    file_path = "WPR_2026-01-23_DEBM_COMB_260127080028.xlsx"

print(f"Analyzing file: {file_path}")
print("=" * 80)

# Read the Excel file
try:
    # First, let's see what sheets are available
    xl_file = pd.ExcelFile(file_path)
    print(f"\nAvailable sheets: {xl_file.sheet_names}")

    # Read each sheet
    for sheet_name in xl_file.sheet_names:
        print(f"\n{'=' * 80}")
        print(f"Sheet: {sheet_name}")
        print("=" * 80)

        df = pd.read_excel(file_path, sheet_name=sheet_name)
        print(f"\nShape: {df.shape}")
        print(f"\nColumns: {df.columns.tolist()}")
        print(f"\nFirst few rows:")
        print(df.head(10))
        print(f"\nData types:")
        print(df.dtypes)

except Exception as e:
    print(f"Error reading file: {e}")
    import traceback
    traceback.print_exc()
