"""
Report generation module - CSV and HTML
"""

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class ReportGenerator:
    """Generate professional reports"""
    
    def __init__(self, config):
        self.config = config
        self.output_dir = Path(config.output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def generate(self, live_hosts: List[str], results: Dict):
        """Generate all reports"""
        print("\n📊 Generating reports...")
        
        # CSV Report
        csv_file = self._generate_csv(live_hosts, results)
        print(f"✅ CSV: {csv_file}")
        
        # HTML Report
        html_file = self._generate_html(live_hosts, results)
        print(f"✅ HTML: {html_file}")
        
        # Summary
        self._print_summary(live_hosts, results)
        
        return csv_file, html_file
    
    def _generate_csv(self, live_hosts: List[str], results: Dict) -> str:
        """Generate CSV report"""
        filename = self.output_dir / f"scan_report_{self.timestamp}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Host', 'Open Ports', 'Services', 'Vulnerabilities', 'Severity'])
            
            for host in live_hosts:
                result = results.get(host, {})
                open_ports = result.get('open_ports', [])
                services = result.get('services', {})
                vulnerabilities = result.get('vulnerabilities', [])
                
                if vulnerabilities:
                    for vuln in vulnerabilities:
                        writer.writerow([
                            host,
                            ', '.join(map(str, open_ports[:10])),
                            ', '.join(set(services.values())),
                            vuln.get('description', ''),
                            vuln.get('severity', 'LOW')
                        ])
                else:
                    writer.writerow([
                        host,
                        ', '.join(map(str, open_ports[:10])),
                        ', '.join(set(services.values())),
                        'No vulnerabilities found',
                        'LOW'
                    ])
        
        return str(filename)
    
    def _generate_html(self, live_hosts: List[str], results: Dict) -> str:
        """Generate HTML report"""
        filename = self.output_dir / f"scan_report_{self.timestamp}.html"
        
        total_ports = sum(len(r.get('open_ports', [])) for r in results.values())
        total_vulns = sum(len(r.get('vulnerabilities', [])) for r in results.values())
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Network Security Scan Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; }}
        .summary {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin: 20px 0; }}
        .card {{ background: #f8f9fa; padding: 15px; border-radius: 8px; text-align: center; }}
        .card .value {{ font-size: 24px; font-weight: bold; }}
        .host-section {{ margin: 20px 0; padding: 15px; background: #f8f9fa; border-radius: 8px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #e9ecef; }}
        .critical {{ color: #dc3545; font-weight: bold; }}
        .high {{ color: #fd7e14; font-weight: bold; }}
        .medium {{ color: #ffc107; font-weight: bold; }}
        .low {{ color: #28a745; font-weight: bold; }}
        .footer {{ text-align: center; margin-top: 30px; color: #6c757d; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔒 Network Security Scan Report</h1>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>Target: {self.config.target}</p>
        </div>
        
        <div class="summary">
            <div class="card"><h3>Hosts</h3><div class="value">{len(live_hosts)}</div></div>
            <div class="card"><h3>Open Ports</h3><div class="value">{total_ports}</div></div>
            <div class="card"><h3>Vulnerabilities</h3><div class="value">{total_vulns}</div></div>
            <div class="card"><h3>Critical</h3><div class="value" style="color:#dc3545;">{sum(1 for r in results.values() for v in r.get('vulnerabilities', []) if v.get('severity') == 'CRITICAL')}</div></div>
        </div>
"""
        
        # Host details
        for host in live_hosts:
            result = results.get(host, {})
            vulns = result.get('vulnerabilities', [])
            
            html += f"""
        <div class="host-section">
            <h3>{host}</h3>
            <p><strong>Open Ports:</strong> {', '.join(map(str, result.get('open_ports', [])[:10]))}</p>
            <p><strong>Services:</strong> {', '.join(set(result.get('services', {}).values()))}</p>
            
            <h4>Vulnerabilities ({len(vulns)})</h4>
            <table>
                <tr><th>Port</th><th>Service</th><th>Description</th><th>Severity</th></tr>
"""
            
            if vulns:
                for vuln in vulns:
                    severity = vuln.get('severity', 'LOW').lower()
                    html += f"""
                <tr>
                    <td>{vuln.get('port', '')}</td>
                    <td>{vuln.get('service', '')}</td>
                    <td>{vuln.get('description', '')}</td>
                    <td class="{severity}">{vuln.get('severity', 'LOW')}</td>
                </tr>
"""
            else:
                html += """
                <tr><td colspan="4" style="text-align:center; color:#28a745;">✅ No vulnerabilities found</td></tr>
"""
            
            html += """
            </table>
        </div>
"""
        
        html += """
        <div class="footer">
            <p>Generated by Enterprise Network Security Scanner</p>
            <p style="color:#dc3545;">⚠️ This report contains sensitive security information</p>
        </div>
    </div>
</body>
</html>
"""
        
        with open(filename, 'w') as f:
            f.write(html)
        
        return str(filename)
    
    def _print_summary(self, live_hosts: List[str], results: Dict):
        """Print summary to console"""
        total_ports = sum(len(r.get('open_ports', [])) for r in results.values())
        total_vulns = sum(len(r.get('vulnerabilities', [])) for r in results.values())
        critical = sum(1 for r in results.values() for v in r.get('vulnerabilities', []) if v.get('severity') == 'CRITICAL')
        
        print("\n" + "="*60)
        print("  📋 SCAN SUMMARY")
        print("="*60)
        print(f"  Total Hosts: {len(live_hosts)}")
        print(f"  Total Open Ports: {total_ports}")
        print(f"  Total Vulnerabilities: {total_vulns}")
        print(f"  Critical Vulnerabilities: {critical}")
        print("="*60)