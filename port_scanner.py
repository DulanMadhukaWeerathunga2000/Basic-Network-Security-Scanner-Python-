import socket

COMMON_PORTS = [
    21,
    22,
    23,
    25,
    53,
    80,
    110,
    139,
    443,
    445,
    3389
]

def scan_ports(ip):

    open_ports = []

    for port in COMMON_PORTS:

        sock = socket.socket()

        sock.settimeout(0.5)

        result = sock.connect_ex((ip, port))

        if result == 0:
            open_ports.append(port)

        sock.close()

    return open_ports