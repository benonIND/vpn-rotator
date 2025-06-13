#!/data/data/com.termux/files/usr/bin/python3
from banner import show_banner
from dns_adblock import DNSManager
from vpn_changer import VPNManager  # Import modul baru

def main_menu():
    print("\n\033[1;33mMAIN MENU:\033[0m")
    print("1. Change VPN Location")
    print("2. DNS Adblock")
    print("3. Check Current IP")
    print("4. Exit")
    return input("\nSelect option: ")

def main():
    show_banner()
    dns = DNSManager()
    vpn = VPNManager()  # Inisialisasi VPN Manager

    while True:
        choice = main_menu()

        if choice == '1':  # VPN Changer
            print("\nAvailable Locations:")
            for i, loc in enumerate(VPNManager.VPN_SERVERS.keys(), 1):
                print(f"{i}. {loc}")
            
            try:
                loc_choice = int(input("Select location (1-3): ")) - 1
                location = list(VPNManager.VPN_SERVERS.keys())[loc_choice]
                if vpn.connect(location):
                    ip_info = vpn.get_ip_info()
                    print(f"\033[1;32m[✓] Connected to {location} | IP: {ip_info.get('query', '?')}\033[0m")
            except:
                print("\033[1;31m[!] Invalid input\033[0m")

        elif choice == '2':  # DNS Adblock
            dns.set_dns('adguard')

        elif choice == '3':  # Check IP
            ip_info = vpn.get_ip_info()
            print(f"\n\033[1;36mCurrent IP: {ip_info.get('query', '?')}")
            print(f"Location: {ip_info.get('country', '?')}\033[0m")

        elif choice == '4':  # Exit
            vpn.disconnect()
            dns.set_dns('default')
            break

if __name__ == "__main__":
    main()
