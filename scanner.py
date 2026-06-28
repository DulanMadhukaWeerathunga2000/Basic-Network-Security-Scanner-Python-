"""
Core scanner class - Orchestrates all modules
"""

import logging
from datetime import datetime
from typing import List, Dict
from host_discovery import HostDiscovery
from port_scanner import PortScanner
from vulnerability import VulnerabilityScanner
from report import ReportGenerator
from utils import get_service_name

logger = logging.getLogger(__name__)

class NetworkScanner:
    """Main scanner orchestrator"""
    
    def __init__(self, config):
        self.config = config
        self.live_hosts = []
        self.results = {}
        self.start_time = datetime.now()
        
        # Initialize modules
        self.host_discovery = HostDiscovery(config)
        self.port_scanner = PortScanner(config)
        self.vuln_scanner = VulnerabilityScanner(config)
        self.report_gen = ReportGenerator(config)
    
    def run(self):
        """Run complete scan"""
        print("\n" + "="*60)
        print(f"  Target: {self.config.target}")
        print(f"  Ports: {len(self.config.get_ports())} ports")
        print(f"  Threads: {self.config.max_threads}")
        print("="*60)
        
        logger.info(f"Starting scan on {self.config.target}")
        
        # Phase 1: Host Discovery
        self.live_hosts = self.host_discovery.discover()
        
        if not self.live_hosts:
            print("\n❌ No live hosts found. Exiting.")
            return
        
        # Phase 2: Port Scanning
        print("\n🔎 Scanning ports...")
        for host in self.live_hosts:
            print(f"\n📡 {host}")
            scan_result = self.port_scanner.scan_host(host)
            
            # Process results
            services = {}
            vulnerabilities = []
            
            for port, banner in scan_result.get('banners', {}).items():
                service = get_service_name(port)
                services[port] = service
                
                # Check vulnerabilities
                vulns = self.vuln_scanner.scan(host, port, banner, service)
                vulnerabilities.extend(vulns)
            
            self.results[host] = {
                'open_ports': scan_result['open_ports'],
                'banners': scan_result['banners'],
                'services': services,
                'vulnerabilities': vulnerabilities
            }
            
            # Print summary for this host
            if scan_result['open_ports']:
                print(f"  ✅ {len(scan_result['open_ports'])} open ports")
                if vulnerabilities:
                    print(f"  ⚠️  {len(vulnerabilities)} vulnerabilities found")
            else:
                print(f"  ℹ️  No open ports")
        
        # Phase 3: Reports
        self.report_gen.generate(self.live_hosts, self.results)
        
        # Final
        duration = datetime.now() - self.start_time
        total_vulns = sum(len(r.get('vulnerabilities', [])) for r in self.results.values())
        
        print("\n" + "="*60)
        print("  ✅ SCAN COMPLETED")
        print("="*60)
        print(f"  Duration: {duration}")
        print(f"  Vulnerabilities found: {total_vulns}")
        print("="*60)