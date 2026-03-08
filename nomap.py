import os
import sys
import socket
import threading
from datetime import datetime
try:
    from termcolor import colored
except ImportError:
    print("[!] Missing termcolor. Run: pip install termcolor")
    sys.exit()

# ==========================================
# [ UI & Banner ] 
# ==========================================
def show_banner():
    os.system('clear')
    print(colored("""
      .-""\"""-.
    .' \     / '.
   /    \   /    \ 
  |      \ /      |
  |  ===  X  ===  |
  |      / \      |
   \    /   \    /
    '. /     \ .'
      `"-...-"`
      
     N o M a p  v 2 . 0
    """, 'red', attrs=['bold']))
    
    print(colored("="*60, 'yellow'))
    print(colored(" ENGINEER: en1passant | TARGET: NMAP DEPRECATION", 'cyan', attrs=['bold']))
    print(colored("="*60, 'yellow'))
    
    print(colored("\n[#] SELECT YOUR MISSION:", 'magenta', attrs=['bold']))
    print(colored("  [1] Quick Recon (Common Ports)", 'white'))
    print(colored("  [2] Deep Scan (Auto-Chain Flow) [⚡ ACTIVE ]", 'green', attrs=['bold']))
    print(colored("  [3] Stealth Scan (SYN)          [🥷 DEV ]", 'yellow'))
    print(colored("  [4] Service Intel (Banner Grab) [🔍 INTEGRATED IN 2]", 'green'))
    print(colored("  [5] Vulnerability Check         [🐛 DEV ]", 'yellow'))
    print(colored("  [6] DNS Lookup (Host to IP)", 'white'))
    print(colored("  [7] My Network & WiFi Intel", 'white'))
    print(colored("  [0] Exit Program", 'red', attrs=['bold']))
    print("")

# ==========================================
# [ Core Functions ]
# ==========================================
def quick_scan(target):
    print(colored(f"\n[*] Starting Quick Scan on {target}...", 'cyan'))
    common_ports = [21, 22, 23, 25, 53, 80, 110, 139, 443, 445, 3306, 3389, 8080]
    for port in common_ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        if s.connect_ex((target, port)) == 0:
            print(colored(f"[+] PORT {port} \t| OPEN", 'green', attrs=['bold']))
        s.close()

def scan_port(target, port, open_ports):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        if s.connect_ex((target, port)) == 0:
            print(colored(f"[+] PORT {port} \t| OPEN", 'green', attrs=['bold']))
            open_ports.append(port)
    except:
        pass
    finally:
        s.close()

def grab_banner(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((target, port))
        if port in [80, 443, 8080]:
            s.send(b"HEAD / HTTP/1.1\r\nHost: " + target.encode() + b"\r\n\r\n")
        else:
            s.send(b"\r\n")
        
        banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
        s.close()
        if banner:
            return banner.split('\n')[0][:50] 
        return "No Banner Available"
    except:
        return "Unknown Service / Filtered"

def deep_scan_chained(target):
    print(colored(f"\n[*] Starting Multi-threaded Deep Scan on {target}...", 'cyan'))
    print(colored("[*] Scanning ports 1 to 1024 real fast...\n", 'yellow'))
    t1 = datetime.now()
    
    open_ports = []
    threads = []
    
    for port in range(1, 1025):
        thread = threading.Thread(target=scan_port, args=(target, port, open_ports))
        threads.append(thread)
        thread.start()
        
    for thread in threads:
        thread.join()
        
    t2 = datetime.now()
    print(colored(f"\n[!] Scan Completed in {t2 - t1}", 'magenta'))
    
    if not open_ports:
        print(colored("[-] No open ports found on this target.", 'red'))
        return

    banners_dict = {}
    print(colored(f"\n[?] Found {len(open_ports)} open ports.", 'yellow'))
    choice = input(colored("[?] Do you want to extract Service Intel (Banners)? (y/n): ", 'cyan')).strip().lower()
    
    if choice == 'y':
        print(colored("\n[*] Extracting Service Banners...", 'cyan'))
        for port in open_ports:
            banner = grab_banner(target, port)
            banners_dict[port] = banner
            print(colored(f"  -> PORT {port}: {banner}", 'green'))
    
    choice_save = input(colored("\n[?] Do you want to save this report to a file? (y/n): ", 'cyan')).strip().lower()
    if choice_save == 'y':
        filename = f"NoMap_Report_{target.replace('.', '_')}.txt"
        with open(filename, 'w') as f:
            f.write(f"--- NoMap v2.0 Scan Report ---\n")
            f.write(f"Target: {target}\n")
            f.write(f"Date: {t1.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Time Taken: {t2-t1}\n\n")
            for port in open_ports:
                service = banners_dict.get(port, "Not Checked")
                f.write(f"[+] PORT {port} | OPEN | Service: {service}\n")
        print(colored(f"[+] Report saved successfully as {filename}", 'green', attrs=['bold']))

def dns_lookup():
    hostname = input(colored("\nEnter Hostname (e.g., google.com): ", 'cyan'))
    try:
        ip = socket.gethostbyname(hostname)
        print(colored(f"[+] Target IP: {ip}", 'green', attrs=['bold']))
    except socket.gaierror:
        print(colored("[-] Error: Could not resolve hostname.", 'red'))

def network_intel():
    print(colored("\n[*] Gathering your network info...", 'cyan'))
    hostname = socket.gethostname()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except:
        local_ip = "127.0.0.1"
    print(colored(f"[+] Hostname : {hostname}", 'green'))
    print(colored(f"[+] Local IP : {local_ip}", 'green'))

# ==========================================
# [ Main Loop ]
# ==========================================
def main():
    while True:
        show_banner()
        try:
            choice = input(colored("NoMap > ", 'yellow', attrs=['bold']))
            
            if choice == '1':
                target = input(colored("\nEnter Target IP: ", 'cyan'))
                quick_scan(target)
                input("\nPress Enter to return to menu...")
                
            elif choice == '2':
                target = input(colored("\nEnter Target IP: ", 'cyan'))
                deep_scan_chained(target)
                input("\nPress Enter to return to menu...")
                
            elif choice in ['3', '5']:
                print(colored("\n[!] This module is currently under development (DEV phase).", 'red'))
                input("\nPress Enter to return to menu...")
                
            elif choice == '4':
                print(colored("\n[*] Service Intel is now fully integrated inside Option [2]!", 'green'))
                input("Press Enter to return to menu...")
                
            elif choice == '6':
                dns_lookup()
                input("\nPress Enter to return to menu...")
                
            elif choice == '7':
                network_intel()
                input("\nPress Enter to return to menu...")
                
            elif choice == '0':
                print(colored("\n[!] Mission Aborted. Goodbye Engineer.\n", 'red', attrs=['bold']))
                sys.exit()
            else:
                print(colored("\n[-] Invalid Choice!", 'red'))
                input("Press Enter to continue...")
                
        except KeyboardInterrupt:
            print(colored("\n\n[!] Program interrupted by user. Exiting...", 'red'))
            sys.exit()

if __name__ == "__main__":
    main()
