"""
Update the index.html with list of available reports
Run this after generating reports to update the landing page
"""
from pathlib import Path
import re
from datetime import datetime


def update_index():
    """Update index.html with list of available reports."""
    reports_dir = Path('reports')

    # Find all report HTML files
    report_files = sorted(
        [f for f in reports_dir.glob('cot_report_*.html')],
        reverse=True  # Most recent first
    )

    if not report_files:
        print("No reports found to list")
        return

    # Generate HTML for report list
    report_list_html = '<ul class="report-list">\n'

    for report_file in report_files:
        # Extract date from filename: cot_report_20260123.html
        match = re.search(r'cot_report_(\d{8})\.html', report_file.name)
        if match:
            date_str = match.group(1)
            # Parse date
            report_date = datetime.strptime(date_str, '%Y%m%d')
            formatted_date = report_date.strftime('%B %d, %Y')

            # Determine contracts (assume DEBM, DEPM for now - could be read from file)
            contracts = 'DEBM, DEPM'

            report_list_html += f'''                    <li class="report-item">
                        <a href="{report_file.name}">
                            <div class="report-date">{formatted_date}</div>
                            <div class="report-contracts">Contracts: {contracts}</div>
                        </a>
                    </li>
'''

    report_list_html += '                </ul>'

    # Read index.html template
    index_file = reports_dir / 'index.html'
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace the no-reports section with actual report list
    if len(report_files) > 0:
        # Remove no-reports div and add report list
        content = re.sub(
            r'<div class="no-reports">.*?</div>',
            report_list_html,
            content,
            flags=re.DOTALL
        )

        # Also remove the commented example if present
        content = re.sub(
            r'<!--\s*<ul class="report-list">.*?</ul>\s*-->',
            '',
            content,
            flags=re.DOTALL
        )

    # Update last updated timestamp
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Write updated index
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Updated index.html with {len(report_files)} reports")
    print(f"Latest report: {report_files[0].name}")


if __name__ == '__main__':
    update_index()
