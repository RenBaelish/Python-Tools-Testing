import socket
from ipaddress import ip_network

def scan_host(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except Exception:
        return False

def scan_network(network, port):
    print(f"Scanning network {network} on port {port}...\n")
    for ip in ip_network(network).hosts():
        if scan_host(str(ip), port):
            print(f"[+] Host {ip} has port {port} OPEN")
        else:
            print(f"[-] Host {ip} port {port} closed")

if __name__ == "__main__":
    subnet = input("Enter subnet (ex: 192.168.1.0/24): ")
    port = int(input("Enter port to scan (ex: 80): "))
    scan_network(subnet, port)
