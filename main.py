#!/data/data/com.termux/files/usr/bin/python3
from banner import show_banner, show_status
from vpn_manager import VPNManager
from dns_manager import DNSManager
import sys
import time

def main():
    # Inisialisasi
    show_banner()
    vpn = VPNManager()
    dns = DNSManager()
    
    try:
        while True:
            print("\n\033[1;33mMAIN MENU:\033[0m")
            print("1. Connect to Free VPN")
            print("2. Change DNS Server")
            print("3. Check Current Status")
            print("4. Disconnect VPN")
            print("5. Exit")
            
            choice = input("\n\033[1;36mSelect option: \033[0m")
            
            if choice == '1':
                # Tampilkan server gratis
                print("\n\033[1;34mFREE VPN SERVERS:\033[0m")
                for i, server in enumerate(vpn.FREE_SERVERS.keys(), 1):
                    details = vpn.FREE_SERVERS[server]
                    print(f"{i}. {server} ({details['region']})")
                
                try:
                    selection = int(input("\nPilih server (1-3): ")) - 1
                    server_name = list(vpn.FREE_SERVERS.keys())[selection]
                    
                    # Connect dengan progress indicator
                    print("\033[1;33m[•] Connecting...\033[0m")
                    if vpn.connect(server_name):
                        # Auto-set DNS setelah VPN terhubung
                        dns.set_dns('adguard')
                        show_status(
                            {'server': server_name},
                            vpn.get_ip_info()
                        )
                except:
                    print("\033[1;31m[!] Pilihan tidak valid\033[0m")
            
            elif choice == '2':
                print("\n\033[1;34mDNS SERVERS:\033[0m")
                for i, server in enumerate(dns.DNS_SERVERS.keys(), 1):
                    print(f"{i}. {server} ({dns.DNS_SERVERS[server]})")
                
                try:
                    selection = int(input("\nPilih DNS (1-4): ")) - 1
                    dns.set_dns(list(dns.DNS_SERVERS.keys())[selection])
                except:
                    print("\033[1;31m[!] Pilihan tidak valid\033[0m")
            
            elif choice == '3':
                show_status(
                    {'server': vpn.connected_server},
                    vpn.get_ip_info()
                )
            
            elif choice == '4':
                vpn.disconnect()
                print("\033[1;32m[✓] VPN disconnected\033[0m")
            
            elif choice == '5':
                print("\033[1;32m[✓] Exiting...\033[0m")
                vpn.disconnect()
                sys.exit(0)
            
            else:
                print("\033[1;31m[!] Invalid option\033[0m")
            
            time.sleep(1)  # Jeda antar menu

    except KeyboardInterrupt:
        print("\n\033[1;33m[!] Program dihentikan\033[0m")
        vpn.disconnect()
        sys.exit(0)

if __name__ == "__main__":
    # Persiapan environment
    if not os.path.exists('/data/data/com.termux/files/usr/bin/openvpn'):
        print("\033[1;31m[!] OpenVPN belum terinstall!")
        print("Jalankan: pkg install openvpn -y\033[0m")
        sys.exit(1)
    
    main()
