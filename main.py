from host_discovery import discover_hosts
from port_scanner import scan_ports
from vulnerability import check

print("="*50)
print("Enterprise Network Security Scanner")
print("="*50)

network=input("Enter Network (Example 192.168.1.0/24): ")

hosts=discover_hosts(network)

print("\nActive Hosts\n")

for host in hosts:

    print(host)

    ports=scan_ports(host)

    print("Open Ports :",ports)

    print("Risk")

    for item in check(ports):

        print(item)

    print("-"*40)