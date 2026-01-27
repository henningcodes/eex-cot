"""
Quick script to generate HTML report from existing data
"""
import sys
import webbrowser
from pathlib import Path
from eex_storage import EEXDataStorage
from eex_html_report_tabbed import EEXHTMLReportTabbed


def main():
    """Generate HTML report from stored data."""
    if len(sys.argv) < 2:
        print("Usage: python generate_report.py <contract1> [contract2] ...")
        print("\nExample:")
        print("  python generate_report.py DEBM DEPM")
        print("\nThis will generate an HTML report from existing stored data.")
        sys.exit(1)

    contracts = sys.argv[1:]
    open_browser = '--open' in contracts

    if '--open' in contracts:
        contracts.remove('--open')

    print(f"\nGenerating HTML report for: {', '.join(contracts)}")
    print("=" * 80)

    storage = EEXDataStorage()
    report_gen = EEXHTMLReportTabbed()

    # Collect data
    contracts_data = {}
    for contract in contracts:
        df = storage.load_history(contract)
        if df is not None and len(df) > 0:
            contracts_data[contract] = df
            print(f"Loaded data for {contract}: {len(df)} records")
        else:
            print(f"Warning: No data found for contract {contract}")

    if not contracts_data:
        print("\nError: No data available for any contracts")
        print("Run the workflow first: python eex_workflow.py DEBM DEPM")
        sys.exit(1)

    # Generate report
    print("\nGenerating HTML report...")
    report_path = report_gen.generate_multi_contract_report(contracts_data)

    print("\n" + "=" * 80)
    print("HTML REPORT GENERATED SUCCESSFULLY")
    print("=" * 80)
    print(f"\nReport saved to: {report_path.absolute()}")
    print(f"\nOpen in browser: file:///{report_path.absolute()}")

    # Open in browser if requested
    if open_browser:
        print("\nOpening in default browser...")
        webbrowser.open(f"file:///{report_path.absolute()}")


if __name__ == '__main__':
    main()
