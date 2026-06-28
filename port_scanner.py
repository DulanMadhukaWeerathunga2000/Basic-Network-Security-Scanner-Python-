"""
Port scanning module - Multi-threaded TCP scanner
"""

import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict
import logging
from tqdm import tqdm

logger = logging.getLogger(__name__)

class PortScanner:
    """Multi-threaded port scanner"""
    
    def __init__(self, config):
        self.config = config
        self.ports = config.get_ports()
        
        # Service probes
        self.probes = {
            21: b'USER anonymous\r\n',
            22: b'SSH-2.0-OpenSSH\r\n',
            25: b'EHLO localhost\r\n',
            80: b'HEAD / HTTP/1.0\r\n\r\n',
            110: b'STAT\r\n',
            143: b'A001 CAPABILITY\r\n',
            443: b'HEAD / HTTP/1.0\r\n\r\n',
            3306: b'\x00\x00\x00\x01',
            5432: b'\x00\x00\x00\x08\x04\xd2\x16\x2f',
            6379: b'PING\r\n',
        }
    
    def scan_host(self, host: str) -> Dict:
        """Scan ports on a single host"""
        open_ports = []
        banners = {}
        
        logger.debug(f"Scanning {host}")
        
        with ThreadPoolExecutor(max_workers=self.config.max_threads) as executor:
            futures = {executor.submit(self._scan_port, host, port): port for port in self.ports}
            
            for future in tqdm(as_completed(futures), total=len(futures), desc=f"Scanning {host}", leave=False):
                port = futures[future]
                if future.result():
                    open_ports.append(port)
        
        # Grab banners for open ports
        for port in open_ports[:30]:  # Limit for speed
            banner = self._grab_banner(host, port)
            if banner:
                banners[port] = banner
        
        return {
            'host': host,
            'open_ports': open_ports,
            'banners': banners
        }
    
    def _scan_port(self, host: str, port: int) -> bool:
        """Check if port is open"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.config.timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def _grab_banner(self, host: str, port: int) -> str:
        """Grab service banner"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.config.timeout)
            sock.connect((host, port))
            
            # Send probe if available
            if port in self.probes:
                sock.send(self.probes[port])
            
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            sock.close()
            return banner[:200]  # Limit length
        except:
            return ""