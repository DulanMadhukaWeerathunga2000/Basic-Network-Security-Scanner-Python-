"""
Host discovery module - Ping sweep
"""

import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List
import logging
from tqdm import tqdm
from utils import get_ip_list

logger = logging.getLogger(__name__)

class HostDiscovery:
    """Discover live hosts on network"""
    
    def __init__(self, config):
        self.config = config
        self.is_windows = sys.platform.startswith('win')
    
    def discover(self) -> List[str]:
        """Discover live hosts"""
        ips = get_ip_list(self.config.target)
        live_hosts = []
        
        logger.info(f"Checking {len(ips)} IPs")
        print("\n🔍 Discovering live hosts...")
        
        with ThreadPoolExecutor(max_workers=self.config.max_threads) as executor:
            futures = {executor.submit(self._ping, ip): ip for ip in ips}
            
            for future in tqdm(as_completed(futures), total=len(futures), desc="Pinging"):
                ip = futures[future]
                if future.result():
                    live_hosts.append(ip)
        
        print(f"✅ Found {len(live_hosts)} live hosts")
        return live_hosts
    
    def _ping(self, ip: str) -> bool:
        """Ping a single host"""
        try:
            if self.is_windows:
                cmd = ['ping', '-n', '1', '-w', '1000', ip]
            else:
                cmd = ['ping', '-c', '1', '-W', '1', ip]
            
            result = subprocess.run(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=2
            )
            return result.returncode == 0
        except:
            return False