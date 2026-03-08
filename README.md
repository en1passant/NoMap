# 🎯 NoMap v2.0
**Advanced Network Reconnaissance & Auto-Chaining Tool**

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Version](https://img.shields.io/badge/Version-2.0%20Stable-green.svg)
![License](https://img.shields.io/badge/License-MIT-red.svg)

**NoMap** is a lightning-fast, multi-threaded network scanner designed by **en1passant**. It aims to provide a cleaner, faster, and highly automated alternative to traditional scanning tools.

---

## 🔥 Features (v2.0)
* ⚡ **Multi-threaded Deep Scan:** Scans 1000+ ports in milliseconds.
* 🤖 **Auto-Chaining:** Automatically detects open ports -> Asks to extract Service Intel (Banners) -> Saves a detailed report to a `.txt` file.
* 🌐 **Network Intel:** Gathers local IP, public gateway, and resolves hostnames on the fly.
* 🥷 **Stealth Scan [IN DEV]:** Upcoming SYN-packet stealth scanning to bypass firewalls.
* 🐛 **Vuln Checker [IN DEV]:** Upcoming local database integration to match banners with known CVEs.

---
<img width="1085" height="832" alt="Screenshot_2026-03-08_08-03-58" src="https://github.com/user-attachments/assets/cb6a4623-08e7-48cb-86c9-cdeff7bbbff4" />
Developed by Eng.EnPassant 🇰🇼 
## 🚀 Installation & Usage
# 1. Clone the repository
git clone https://github.com/en1passant/NoMap.git

# 2. Enter the directory
cd NoMap

# 3. Install dependencies
pip install termcolor

# 4. Run the tool
python3 nomap.py
