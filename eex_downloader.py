"""
EEX CoT Report Downloader

This module downloads Commitment of Traders reports from the EEX website.
"""
import requests
from bs4 import BeautifulSoup
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import time


class EEXDownloader:
    """Downloader for EEX Commitment of Traders reports."""

    BASE_URL = "https://public.eex-group.com/eex/mifid2/rts-21/"
    INDEX_URL = f"{BASE_URL}index.html"

    def __init__(self, download_dir: str = "."):
        """
        Initialize downloader.

        Args:
            download_dir: Directory to save downloaded files
        """
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(parents=True, exist_ok=True)

    def get_available_files(self) -> List[Dict[str, str]]:
        """
        Scrape the website to get list of available files.

        Returns:
            List of dictionaries with file information
        """
        print(f"Fetching file list from {self.INDEX_URL}")
        response = requests.get(self.INDEX_URL)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all links to .xlsx files
        files = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.endswith('.xlsx') and 'WPR_' in href:
                # Parse filename: WPR_2026-01-23_DEBM_COMB_260127080028.xlsx
                filename = href
                match = re.match(r'WPR_(\d{4}-\d{2}-\d{2})_([A-Z0-9]+)_COMB_(\d+)\.xlsx', filename)

                if match:
                    report_date, contract_code, timestamp = match.groups()
                    files.append({
                        'filename': filename,
                        'url': f"{self.BASE_URL}{filename}",
                        'report_date': report_date,
                        'contract_code': contract_code,
                        'timestamp': timestamp
                    })

        # Sort by report_date descending (newest first)
        files.sort(key=lambda x: (x['report_date'], x['timestamp']), reverse=True)

        return files

    def get_latest_files(self, contracts: Optional[List[str]] = None) -> List[Dict[str, str]]:
        """
        Get the latest files for specified contracts.

        Args:
            contracts: List of contract codes (e.g., ['DEBM', 'DEPM']). If None, returns all.

        Returns:
            List of dictionaries with file information for latest reports
        """
        all_files = self.get_available_files()

        if contracts is None:
            # Group by contract and get latest for each
            contract_files = {}
            for file_info in all_files:
                contract = file_info['contract_code']
                if contract not in contract_files:
                    contract_files[contract] = file_info
            return list(contract_files.values())
        else:
            # Filter for specified contracts and get latest for each
            latest_files = []
            for contract in contracts:
                contract_files = [f for f in all_files if f['contract_code'] == contract]
                if contract_files:
                    latest_files.append(contract_files[0])  # First is latest due to sorting
                else:
                    print(f"Warning: No files found for contract {contract}")

            return latest_files

    def download_file(self, file_info: Dict[str, str], force: bool = False) -> Optional[Path]:
        """
        Download a single file.

        Args:
            file_info: Dictionary with file information (must contain 'url' and 'filename')
            force: If True, download even if file exists

        Returns:
            Path to downloaded file, or None if download failed
        """
        file_path = self.download_dir / file_info['filename']

        # Check if file already exists
        if file_path.exists() and not force:
            print(f"File already exists: {file_path}")
            return file_path

        try:
            print(f"Downloading {file_info['filename']}...")
            response = requests.get(file_info['url'], stream=True)
            response.raise_for_status()

            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"Downloaded to {file_path}")
            return file_path

        except Exception as e:
            print(f"Error downloading {file_info['filename']}: {e}")
            return None

    def download_latest(self, contracts: List[str], force: bool = False) -> List[Path]:
        """
        Download the latest reports for specified contracts.

        Args:
            contracts: List of contract codes (e.g., ['DEBM', 'DEPM'])
            force: If True, download even if files exist

        Returns:
            List of paths to downloaded files
        """
        latest_files = self.get_latest_files(contracts)

        downloaded_paths = []
        for file_info in latest_files:
            path = self.download_file(file_info, force=force)
            if path:
                downloaded_paths.append(path)
            time.sleep(0.5)  # Be nice to the server

        return downloaded_paths

    def get_contract_history(self, contract: str, limit: Optional[int] = None) -> List[Dict[str, str]]:
        """
        Get historical files for a specific contract.

        Args:
            contract: Contract code (e.g., 'DEBM')
            limit: Maximum number of files to return (most recent first)

        Returns:
            List of dictionaries with file information
        """
        all_files = self.get_available_files()
        contract_files = [f for f in all_files if f['contract_code'] == contract]

        if limit:
            contract_files = contract_files[:limit]

        return contract_files


def download_contracts(contracts: List[str], download_dir: str = ".", force: bool = False) -> List[Path]:
    """
    Convenience function to download latest reports for contracts.

    Args:
        contracts: List of contract codes
        download_dir: Directory to save files
        force: If True, redownload even if files exist

    Returns:
        List of paths to downloaded files
    """
    downloader = EEXDownloader(download_dir)
    return downloader.download_latest(contracts, force=force)


if __name__ == '__main__':
    import sys

    # Default contracts
    contracts = ['DEBM', 'DEPM']

    if len(sys.argv) > 1:
        contracts = sys.argv[1].split(',')

    print(f"Downloading latest reports for: {', '.join(contracts)}")
    print("=" * 80)

    downloader = EEXDownloader(".")

    # Show available latest files
    print("\n=== Latest Available Files ===")
    latest_files = downloader.get_latest_files(contracts)
    for file_info in latest_files:
        print(f"Contract: {file_info['contract_code']}")
        print(f"  Report Date: {file_info['report_date']}")
        print(f"  Filename: {file_info['filename']}")
        print()

    # Download
    print("=== Downloading ===")
    downloaded = downloader.download_latest(contracts)
    print(f"\nDownloaded {len(downloaded)} files:")
    for path in downloaded:
        print(f"  - {path}")
