# 🔎 Network Tracker – Advanced Device Discovery with Nmap

Network Tracker is a Python-based real-time device discovery tool built on top of `nmap`. It identifies devices on your local network, detects new or disconnected hosts, and provides extended insights including:

- IP address
- Hostname (reverse DNS)
- MAC address & Vendor
- Operating System (OS fingerprint)
- Open TCP ports & running services

> Ideal for IT admins, security analysts, network engineers, and home lab enthusiasts.

---

## 📦 Features

- ✅ Real-time subnet scanning
- ✅ Detects new devices joining or leaving the network
- ✅ Displays MAC & vendor (Layer 2)
- ✅ Identifies OS & service versions (Layer 7)
- ✅ Works with manual or automatically detected subnets
- ✅ Fully CLI-based; easily extendable to Web UI or logging

---

## 🛠 Requirements

- Python 3.7+
- `nmap` (installed on the system)
- sudo/root privileges (for full OS/port scan support)

---

## 🔧 Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/network-tracker.git
cd network-tracker
