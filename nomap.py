import socket
import pyfiglet
from termcolor import colored
from datetime import datetime
import sys
import os
import subprocess

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_banner():
    eye_art = """
              .-------.
            /   X   X   \\
           |    -- --    |   
            \   _____   /    [ NoMap: Deep Scan Mode ]
              '-------'
    """
    ascii_name = pyfiglet.figlet_format("NoMap")
    print(colored(eye_art, 'red', attrs=['bold']))
    print(colored(ascii_name, 'cyan', attrs=['bold']))
    print(colored("=" * 60, 'yellow'))
    print(colored(f"  ENGINEER: en1passant | VERSION: 1.5 | {datetime.now().strftime('%H:%M:%S')}", 'white'))
    print(colored("=" * 60, 'yellow'))

def print_menu():
    print(colored("\n[#] SELECT YOUR MISSION:", 'magenta', attrs=['bold']))
    print(colored("  [1]", 'green') + " Quick Recon (Common Ports)")
    print(colored("  [2]", 'green') + " Deep Scan (Custom Range)")
    print(colored("  [3]", 'green') + " Whois Intel (Domain Data)")
    print(colored("  [4]", 'green') + " My Network & WiFi Intel")
    print(colored("  [5]", 'green') + " DNS Lookup (Host to IP)")
    print(colored("  [6]", 'green') + " Clear Terminal")
    print(colored("  [0]", 'red') + " Exit Program")
    print(colored("\n" + "_"*30, 'yellow'))

def scan_logic(target, ports):
    try:
        ip = socket.gethostbyname(target)
        print(colored(f"\n[!] Target Locked: {ip}", 'blue', attrs=['bold']))
        print(colored("-" * 40, 'white'))
        
        found_any = False
        for port in ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5) # وقت انتظار متوازن للسرعة والدقة
            result = s.connect_ex((ip, port))
            
            if result == 0:
                print(colored(f"[+] PORT {port:<5} | ", 'green') + colored("OPEN", 'white', 'on_green'))
                found_any = True
            s.close()
            
        if not found_any:
            print(colored("[?] No open ports found in this range.", 'yellow'))
            
    except Exception as e:
        print(colored(f"\n[X] Connection Error: {e}", 'red'))

if __name__ == "__main__":
    clear_screen()
    print_banner()
    
    while True:
        print_menu()
        cmd = input(colored("\nNoMap > ", 'yellow'))

        if cmd == '1':
            target = input(colored("Enter Target: ", 'white'))
            scan_logic(target, [21, 22, 23, 25, 53, 80, 110, 443, 445, 3389, 8080])
        
        elif cmd == '2': # إصلاح الخيار الثاني
            target = input(colored("Enter Target: ", 'white'))
            try:
                start_p = int(input(colored("Start Port: ", 'white')))
                end_p = int(input(colored("End Port: ", 'white')))
                scan_logic(target, range(start_p, end_p + 1))
            except ValueError:
                print(colored("[!] Enter valid numbers for ports!", 'red'))
            
        elif cmd == '3':
            target = input(colored("Enter Domain: ", 'white'))
            os.system(f"whois {target} | grep -E 'Domain Name|Registrar|Creation Date'")
            
        elif cmd == '4':
            # جلب معلومات الشبكة
            hostname = socket.gethostname()
            print(f"\n- Local IP: {socket.gethostbyname(hostname)}")
            print("- Public IP: ", end="", flush=True)
            os.system("curl -s https://ifconfig.me")
            # جلب Gateway
            cmd_g = "ip route | grep default | awk '{print $3}'"
            try:
                gateway = subprocess.check_output(cmd_g, shell=True).decode().strip()
                print(f"\n- Gateway (WiFi): {gateway}")
            except: pass
            print("\n")

        elif cmd == '5':
            target = input(colored("Enter Hostname: ", 'white'))
            try:
                print(colored(f"[+] IP: {socket.gethostbyname(target)}", 'green'))
            except: print(colored("[X] Failed to resolve.", 'red'))

        elif cmd == '6':
            clear_screen()
            print_banner()

        elif cmd == '0':
            print(colored("\n[!] Mission Aborted. Goodbye Engineer.", 'red', attrs=['bold']))
            break
