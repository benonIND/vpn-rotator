#!/data/data/com.termux/files/usr/bin/python3

import sys
import os
import time
from banner import show_banner, show_status
from ip_changer import IPChanger
from dns_adblock import DNSManager

def setup_environment():
    os.system('clear')
    if not os.path.exists('/data/data/com.termux/files/usr/bin/tor'):
        print("\033[1;31m[!] Tor belum terinstall! Jalankan:")
        print("pkg install tor -y")
        print("pip install stem requests\033[0m")
        sys.exit(1)

def main():
    setup_environment()
    show_banner()
    
    # Init modules
    ip_changer = IPChanger()
    dns_manager = DNSManager()
    
    try:
        # Set default DNS
        dns_manager.set_dns('adguard')
        
        # Start IP rotation
        ip_changer.start(interval=10)
        
        # Show initial status
        initial_ip = ip_changer.get_ip_info()
        show_status(initial_ip['ip'], initial_ip['country'], dns_manager.current_dns)
        
        # Keep alive
        input("\nTekan Enter untuk berhenti...\n")
        
    except KeyboardInterrupt:
        pass
    finally:
        ip_changer.stop()
        print("\n\033[1;31m[!] Service dihentikan\033[0m")

if __name__ == "__main__":
    main()
