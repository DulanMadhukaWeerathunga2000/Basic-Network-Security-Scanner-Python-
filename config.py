"""
Configuration management
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
    """Scanner configuration"""
    target: str
    port_range: str = "1-1000"
    max_threads: int = 50
    timeout: float = 1.0
    verbose: bool = False
    output_dir: str = "reports"
    
    def __post_init__(self):
        import os
        os.makedirs(self.output_dir, exist_ok=True)
    
    def get_ports(self) -> list:
        """Parse port range to list"""
        ports = []
        if '-' in self.port_range:
            start, end = map(int, self.port_range.split('-'))
            ports = list(range(start, min(end, 10000) + 1))
        else:
            ports = [int(p.strip()) for p in self.port_range.split(',')]
        return ports[:2000]  # Limit for performance