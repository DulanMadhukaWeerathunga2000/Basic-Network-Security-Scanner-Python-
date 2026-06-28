# 🚀 Enterprise Network Security Scanner

Simple, fast, and professional network security scanner.

## ⚡ Quick Start

```bash
# Install dependency
pip install tqdm

# Scan a subnet
python main.py 192.168.1.0/24

# Scan a range
python main.py 192.168.1.1-100

# Scan single IP
python main.py 192.168.1.1

# Custom ports
python main.py 192.168.1.0/24 -p 1-10000

# More threads (faster)
python main.py 192.168.1.0/24 -t 100