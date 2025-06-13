#!/data/data/com.termux/files/usr/bin/python3
from banner import show_banner
from dns_manager import DNSManager
from vpn_manager import VPNManager
import sys

def show_menu():
    print("\n\033[1;33mMAIN MENU:\033[0m")
    print("1. Connect VPN")
    print("2. Change DNS")
    print("3. Check Connection")
    print("4. Disconnect VPN")
    print("5. Exit")

def main():
    show_banner()
    vpn = VPNManager()
    dns = DNSManager()

    try:
        while True:
            show_menu()
            choice = input("\n\033[1;36mSelect option: \033[0m")

            if choice == '1':
                print("\n\033[1;35mAvailable Countries:\033[0m")
                for i, country in enumerate(vpn.SERVERS.keys(), 1):
                    print(f"{i}. {country}")
                
                try:
                    selection = int(input("\nSelect country (1-3): ")) - 1
                    country = list(vpn.SERVERS.keys())[selection]
                    vpn.connect(country)
                except (ValueError, IndexError):
                    print("\033[1;31m[!] Invalid selection\033[0m")

            elif choice == '2':
                print("\n\033[1;35mAvailable DNS Servers:\033[0m")
                for i, server in enumerate(dns.DNS_SERVERS.keys(), 1):
                    print(f"{i}. {server}")
                
                try:
                    selection = int(input("\nSelect DNS (1-4): ")) - 1
                    server = list(dns.DNS_SERVERS.keys())[selection]
                    dns.set_dns(server)
                except (ValueError, IndexError):
                    print("\033[1;31m[!] Invalid selection\033[0m")

            elif choice == '3':
                ip_info = vpn.get_ip_info()
                print(f"\n\033[1;35mCurrent Status:\033[0m")
                print(f"IP Address: {ip_info['ip']}")
                print(f"Country: {ip_info['country']}")
                print(f"City: {ip_info['city']}")
                print(f"VPN Connected: {'Yes' if vpn.connected else 'No'}")

            elif choice == '4':
                vpn.disconnect()

            elif choice == '5':
                print("\033[1;32m[✓] Exiting...\033[0m")
                vpn.disconnect()
                sys.exit(0)

            else:
                print("\033[1;31m[!] Invalid option\033[0m")

    except KeyboardInterrupt:
        print("\n\033[1;33m[!] Program interrupted\033[0m")
        vpn.disconnect()
        sys.exit(0)

if __name__ == "__main__":
    main()
