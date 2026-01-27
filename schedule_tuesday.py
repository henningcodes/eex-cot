"""
Tuesday Scheduler for EEX CoT Workflow

This script is designed to be run by Windows Task Scheduler every Tuesday.
It runs the full EEX CoT workflow and logs the output.
"""
import sys
import os
from datetime import datetime
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from eex_workflow import EEXWorkflow


def main():
    """Run the Tuesday workflow with logging."""
    # Configuration
    contracts = ['DEBM', 'DEPM']  # Add more contracts here if needed
    data_dir = 'data'
    plots_dir = 'plots'
    download_dir = '.'
    weeks = 13
    log_dir = Path('logs')

    # Create log directory
    log_dir.mkdir(exist_ok=True)

    # Setup logging
    log_file = log_dir / f"workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    # Redirect stdout and stderr to log file
    class Logger:
        def __init__(self, filename):
            self.terminal = sys.stdout
            self.log = open(filename, 'w', encoding='utf-8')

        def write(self, message):
            self.terminal.write(message)
            self.log.write(message)
            self.log.flush()

        def flush(self):
            self.terminal.flush()
            self.log.flush()

    sys.stdout = Logger(log_file)
    sys.stderr = sys.stdout

    print(f"Log file: {log_file}")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    try:
        # Create and run workflow
        workflow = EEXWorkflow(
            contracts=contracts,
            data_dir=data_dir,
            plots_dir=plots_dir,
            download_dir=download_dir
        )

        success = workflow.run_full_workflow(
            force_download=False,  # Don't redownload if file exists
            weeks=weeks
        )

        if success:
            print(f"\nCompleted successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            return 0
        else:
            print(f"\nWorkflow failed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            return 1

    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
