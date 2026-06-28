#!/usr/bin/env python3
"""
Enterprise Network Security Scanner - Main Entry Point
"""

import argparse
import sys
import logging
from scanner import NetworkScanner
from config import Config
from utils import setup_logging, print_banner

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Enterprise Network Security Scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py 192.168.1.0/24
  python main.py 192.168.1.1-100
  python main.py 192.168.1.1 -p 22,80,443
  python main.py 192.168.1.0/24 -t 100
        """
    )
    
    parser.add_argument('target', help='Target (IP, range, or CIDR)')
    parser.add_argument('-p', '--ports', default='1-1000', help='Port range (default: 1-1000)')
    parser.add_argument('-t', '--threads', type=int, default=50, help='Threads (default: 50)')
    parser.add_argument('--timeout', type=float, default=1.0, help='Timeout in seconds')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Setup
    setup_logging(args.verbose)
    print_banner()
    
    # Create config
    config = Config(
        target=args.target,
        port_range=args.ports,
        max_threads=args.threads,
        timeout=args.timeout,
        verbose=args.verbose
    )
    
    # Run scanner
    scanner = NetworkScanner(config)
    scanner.run()

if __name__ == "__main__":
    main()