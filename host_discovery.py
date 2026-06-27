import platform
import subprocess
import ipaddress

def ping_host(ip):
    param = "-n" if platform.system().lower() == "windows" else "-c"

    result = subprocess.run(
        ["ping", param, "1", str(ip)],
        stdout=subprocess.DEVNULL
    )

    return result.returncode == 0


def discover_hosts(network):
    active_hosts = []

    for ip in ipaddress.ip_network(network, strict=False).hosts():
        if ping_host(ip):
            active_hosts.append(str(ip))

    return active_hosts