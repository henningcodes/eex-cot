"""
EEX CoT Main Workflow

This is the main script that orchestrates the entire EEX Commitment of Traders workflow:
1. Download latest reports from EEX website
2. Parse Excel files
3. Store data in local database
4. Generate analysis and visualizations
"""
import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import List

from eex_downloader import EEXDownloader
from eex_parser import EEXCoTParser
from eex_storage import EEXDataStorage
from eex_analyzer import EEXAnalyzer
from eex_visualizer import EEXVisualizer
from eex_html_report import EEXHTMLReport


class EEXWorkflow:
    """Main workflow orchestrator for EEX CoT analysis."""

    def __init__(self, contracts: List[str], data_dir: str = "data",
                 plots_dir: str = "plots", download_dir: str = "."):
        """
        Initialize workflow.

        Args:
            contracts: List of contract codes to process
            data_dir: Directory for data storage
            plots_dir: Directory for plot outputs
            download_dir: Directory for downloaded Excel files
        """
        self.contracts = contracts
        self.downloader = EEXDownloader(download_dir)
        self.storage = EEXDataStorage(data_dir)
        self.download_dir = Path(download_dir)
        self.plots_dir = plots_dir

    def run_full_workflow(self, force_download: bool = False, weeks: int = 13):
        """
        Run the complete workflow.

        Args:
            force_download: If True, redownload files even if they exist
            weeks: Number of weeks to include in visualizations
        """
        print("\n" + "="*80)
        print("EEX COMMITMENT OF TRADERS WORKFLOW")
        print(f"Contracts: {', '.join(self.contracts)}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80 + "\n")

        # Step 1: Download latest files
        print("\n[STEP 1/6] Downloading latest reports...")
        print("-" * 80)
        downloaded_files = self.downloader.download_latest(self.contracts, force=force_download)

        if not downloaded_files:
            print("ERROR: No files were downloaded")
            return False

        print(f"[OK] Downloaded {len(downloaded_files)} files")

        # Step 2: Parse and store data
        print("\n[STEP 2/6] Parsing and storing data...")
        print("-" * 80)

        for file_path in downloaded_files:
            # Parse file
            parser = EEXCoTParser(str(file_path))
            metadata = parser.extract_metadata()
            contract = metadata['contract_code']

            print(f"\nProcessing {contract}...")
            print(f"  Report Date: {metadata['report_date']}")
            print(f"  Contract: {metadata['contract_name']}")

            # Parse all sheets (includes historical data)
            df = parser.parse_all_sheets()

            # Store data
            self.storage.append_data(contract, df)

        print(f"\n[OK] Parsed and stored data for {len(downloaded_files)} contracts")

        # Step 3: Generate analysis
        print("\n[STEP 3/6] Generating analysis...")
        print("-" * 80)

        for contract in self.contracts:
            print(f"\n{'='*80}")
            df = self.storage.load_history(contract)

            if df is None or len(df) == 0:
                print(f"No data available for {contract}")
                continue

            analyzer = EEXAnalyzer(df)
            analyzer.print_summary()

        print(f"\n[OK] Generated analysis for {len(self.contracts)} contracts")

        # Step 4: Generate visualizations
        print("\n[STEP 4/6] Generating visualizations...")
        print("-" * 80)

        all_plots = []
        for contract in self.contracts:
            df = self.storage.load_history(contract)

            if df is None or len(df) == 0:
                print(f"Skipping {contract} - no data")
                continue

            visualizer = EEXVisualizer(df, output_dir=self.plots_dir)
            plots = visualizer.create_all_plots(contract, weeks=weeks)
            all_plots.extend(plots)

        print(f"\n[OK] Generated {len(all_plots)} plots")

        # Step 5: Generate HTML report
        print("\n[STEP 5/6] Generating HTML report...")
        print("-" * 80)

        report_gen = EEXHTMLReport()

        # Collect data for all contracts
        contracts_data = {}
        for contract in self.contracts:
            df = self.storage.load_history(contract)
            if df is not None and len(df) > 0:
                contracts_data[contract] = df

        if contracts_data:
            report_path = report_gen.generate_multi_contract_report(
                contracts_data,
                plots_dir=self.plots_dir
            )
            print(f"[OK] HTML report generated")
        else:
            print("Warning: No data available for HTML report")
            report_path = None

        # Step 6: Summary
        print("\n[STEP 6/6] Workflow Summary")
        print("-" * 80)
        print(f"[OK] Downloaded: {len(downloaded_files)} files")
        print(f"[OK] Processed: {len(self.contracts)} contracts")
        print(f"[OK] Generated: {len(all_plots)} plots")
        print(f"\nPlots saved to: {Path(self.plots_dir).absolute()}")
        print(f"Data saved to: {Path(self.storage.data_dir).absolute()}")

        if report_path:
            print(f"HTML report: {report_path.absolute()}")
            print(f"\nOpen in browser: file:///{report_path.absolute()}")

        print("\n" + "="*80)
        print("WORKFLOW COMPLETED SUCCESSFULLY")
        print("="*80 + "\n")

        return True

    def update_only(self):
        """
        Update existing data without regenerating all outputs.
        Downloads latest files and updates storage only.
        """
        print("\n" + "="*80)
        print("EEX COT DATA UPDATE")
        print(f"Contracts: {', '.join(self.contracts)}")
        print("="*80 + "\n")

        # Download
        print("Downloading latest reports...")
        downloaded_files = self.downloader.download_latest(self.contracts, force=False)

        if not downloaded_files:
            print("No new files to download")
            return False

        # Parse and store
        print("\nParsing and storing data...")
        for file_path in downloaded_files:
            parser = EEXCoTParser(str(file_path))
            metadata = parser.extract_metadata()
            contract = metadata['contract_code']

            print(f"  Processing {contract} ({metadata['report_date']})")

            df = parser.parse_all_sheets()
            self.storage.append_data(contract, df)

        print(f"\n[OK] Updated data for {len(self.contracts)} contracts")
        return True


def main():
    """Main entry point for command-line usage."""
    parser = argparse.ArgumentParser(
        description='EEX Commitment of Traders Workflow',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run full workflow for DEBM and DEPM
  python eex_workflow.py DEBM DEPM

  # Update data only (no analysis/plots)
  python eex_workflow.py DEBM DEPM --update-only

  # Force redownload and show 20 weeks of data
  python eex_workflow.py DEBM DEPM --force --weeks 20

  # Specify custom directories
  python eex_workflow.py DEBM --data-dir ./my_data --plots-dir ./my_plots
        """
    )

    parser.add_argument('contracts', nargs='+',
                       help='Contract codes to process (e.g., DEBM DEPM)')
    parser.add_argument('--data-dir', default='data',
                       help='Directory for data storage (default: data)')
    parser.add_argument('--plots-dir', default='plots',
                       help='Directory for plots (default: plots)')
    parser.add_argument('--download-dir', default='.',
                       help='Directory for downloaded files (default: current directory)')
    parser.add_argument('--force', action='store_true',
                       help='Force redownload of files even if they exist')
    parser.add_argument('--weeks', type=int, default=13,
                       help='Number of weeks to include in plots (default: 13)')
    parser.add_argument('--update-only', action='store_true',
                       help='Only update data without generating analysis/plots')

    args = parser.parse_args()

    # Create workflow
    workflow = EEXWorkflow(
        contracts=args.contracts,
        data_dir=args.data_dir,
        plots_dir=args.plots_dir,
        download_dir=args.download_dir
    )

    # Run workflow
    try:
        if args.update_only:
            success = workflow.update_only()
        else:
            success = workflow.run_full_workflow(
                force_download=args.force,
                weeks=args.weeks
            )

        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print("\n\nWorkflow interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
