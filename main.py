#!/usr/bin/env python3
from banner import show_banner
from ip_changer import IPChanger
from dns_changer import DNSChanger
import time
import threading

def start_full_program():
    ip_changer = IPChanger()
    dns_changer = DNSChanger()
    
    dns_changer.set_ad_block_dns()
    ip_thread = threading.Thread(target=ip_changer.start_changing_ip, args=(5,))
    ip_thread.daemon = True
    ip_thread.start()
    
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        dns_changer.restore_default_dns()
        print("\n[+] Program dihentikan")

def start_ip_changer_only():
    IPChanger().start_changing_ip(5)

def start_dns_changer_only():
    DNSChanger().set_ad_block_dns()
    input("\nTekan Enter untuk kembali ke menu...")

def main():
    show_banner()
    while True:
        print("\n\033[1;36mMenu Utama:\033[0m")
        print("1. Ganti IP otomatis + DNS anti iklan")
        print("2. Ganti IP saja")
        print("3. DNS anti iklan saja")
        print("4. Keluar")
        
        choice = input("\nPilihan (1-4): ")
        
        if choice == '1':
            start_full_program()
        elif choice == '2':
            start_ip_changer_only()
        elif choice == '3':
            start_dns_changer_only()
        elif choice == '4':
            exit()
        else:
            print("\033[1;31mPilihan tidak valid!\033[0m")

if __name__ == "__main__":
    main()