"""
Utility functions
"""

import logging
import sys
import socket
from typing import List

def setup_logging(verbose: bool = False):
    """Setup logging configuration"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('scanner.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    # Reduce noise from libraries
    logging.getLogger('urllib3').setLevel(logging.WARNING)

def print_banner():
    """Print scanner banner"""
    banner = """
╔══════════════════════════════════════════════════════╗
║                                                      ║
║   ███████╗███╗   ██╗████████╗███████╗██████╗       ║
║   ██╔════╝████╗  ██║╚══██╔══╝██╔════╝██╔══██╗      ║
║   █████╗  ██╔██╗ ██║   ██║   █████╗  ██████╔╝      ║
║   ██╔══╝  ██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗      ║
║   ███████╗██║ ╚████║   ██║   ███████╗██║  ██║      ║
║   ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝      ║
║                                                      ║
║       Enterprise Network Security Scanner           ║
║              Professional Edition                   ║
╚══════════════════════════════════════════════════════╝
    """
    print(banner)

def get_ip_list(target: str) -> List[str]:
    """Generate IP list from target"""
    ips = []
    
    # CIDR
    if '/' in target:
        try:
            import ipaddress
            network = ipaddress.ip_network(target, strict=False)
            return [str(ip) for ip in network.hosts()]
        except:
            pass
    
    # Range
    if '-' in target:
        parts = target.split('-')
        base = parts[0]
        if '.' in base:
            prefix = '.'.join(base.split('.')[:-1])
            start = int(base.split('.')[-1])
            end = int(parts[1])
            for i in range(start, end + 1):
                ips.append(f"{prefix}.{i}")
            return ips
    
    # Single IP
    ips.append(target)
    return ips

def is_valid_ip(ip: str) -> bool:
    """Check if valid IP"""
    try:
        socket.inet_aton(ip)
        return True
    except:
        return False

def get_service_name(port: int) -> str:
    """Get service name from port"""
    services = {
        21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP',
        53: 'DNS', 80: 'HTTP', 110: 'POP3', 111: 'RPC',
        135: 'MSRPC', 139: 'NetBIOS', 143: 'IMAP',
        443: 'HTTPS', 445: 'SMB', 993: 'IMAPS',
        995: 'POP3S', 1080: 'SOCKS', 1433: 'MSSQL',
        1521: 'Oracle', 3306: 'MySQL', 3389: 'RDP',
        5432: 'PostgreSQL', 5900: 'VNC', 6379: 'Redis',
        8080: 'HTTP-Alt', 27017: 'MongoDB'
    }
    return services.get(port, 'Unknown')