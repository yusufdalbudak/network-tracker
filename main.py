import subprocess
import time
import socket
import re
import sys

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception as e:
        print(f"[WARN] Unable to get local IP: {e}")
        return None
    finally:
        s.close()

def resolve_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return "unknown"

def nmap_scan(subnet="192.168.1.0/24"):
    print(f"[INFO] Running Nmap scan (detailed) on: {subnet}")
    result = subprocess.run(
        ['nmap', '-O', '-sS', '-sV', subnet],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True
    )

    devices = []
    device = {}
    capture_ports = False
    open_ports = []

    for line in result.stdout.splitlines():
        line = line.strip()

        if line.startswith("Nmap scan report for"):
            if device:
                if open_ports:
                    device['ports'] = open_ports
                    open_ports = []
                devices.append(device)
                device = {}
            ip = line.split()[-1]
            device = {'ip': ip}
            device['hostname'] = resolve_hostname(ip)

        elif "MAC Address:" in line:
            parts = line.split("MAC Address:")[1].strip().split(" ", 1)
            mac = parts[0]
            vendor = parts[1].strip("() ") if len(parts) > 1 else "Unknown"
            device['mac'] = mac
            device['vendor'] = vendor

        elif line.startswith("OS details:"):
            device['os'] = line.split(":", 1)[1].strip()

        elif line.startswith("PORT"):
            capture_ports = True
            continue

        elif capture_ports and line and re.match(r"^\d+/[a-z]+", line):
            open_ports.append(line)

        elif capture_ports and not line:
            capture_ports = False

    if device:
        if open_ports:
            device['ports'] = open_ports
        devices.append(device)

    for d in devices:
        print(f"\n[+] IP: {d['ip']} | Hostname: {d.get('hostname', '-')}")
        print(f"    MAC: {d.get('mac', '-')} | Vendor: {d.get('vendor', '-')}")
        print(f"    OS: {d.get('os', '-')}")
        if 'ports' in d:
            print("    Ports:")
            for port in d['ports']:
                print(f"      - {port}")
    return devices

def detect_changes(previous, current):
    old_ips = set(d['ip'] for d in previous)
    new_ips = set(d['ip'] for d in current)

    added = new_ips - old_ips
    removed = old_ips - new_ips

    if added:
        for ip in added:
            print(f"[NEW DEVICE] {ip} joined the network.")
    if removed:
        for ip in removed:
            print(f"[DISCONNECTED] {ip} left the network.")

def show_device_table(devices):
    print("\n[RESULT] Active Devices Detected:")
    print("IP Address\t\tHostname\t\tMAC Address\t\tVendor")
    print("-" * 90)
    for d in devices:
        print(f"{d.get('ip')}\t{d.get('hostname', '-')}\t{d.get('mac', '-')}\t{d.get('vendor', '-')}")

if __name__ == "__main__":
    try:
        # If a subnet is provided as an argument, use it. Otherwise, detect local subnet.
        if len(sys.argv) > 1:
            subnet_to_scan = sys.argv[1]
        else:
            local_ip = get_local_ip()
            subnet_to_scan = '.'.join(local_ip.split('.')[:3]) + '.0/24' if local_ip else '192.168.1.0/24'

        previous_devices = []

        while True:
            scanned_devices = nmap_scan(subnet_to_scan)
            detect_changes(previous_devices, scanned_devices)
            show_device_table(scanned_devices)
            previous_devices = scanned_devices.copy()
            print("\n[INFO] Waiting 60 seconds before next scan...\n")
            time.sleep(60)

    except KeyboardInterrupt:
        print("\n[INFO] Scan interrupted by user. Exiting cleanly...")
