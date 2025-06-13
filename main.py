#!/data/data/com.termux/files/usr/bin/python3
from banner import show_banner, show_status
from vpn_manager import VPNManager
from dns_manager import DNSManager
import os
import sys
import time

def show_menu():
    print("\n\033[1;33mMAIN MENU:\033[0m")
    print("1. Connect VPN Manual")
    print("2. Auto-Rotate VPN (Ganti IP Otomatis)")
    print("3. Change DNS Server")
    print("4. Check Status")
    print("5. Stop Auto-Rotate")
    print("6. Exit")
    
def main():
    # Inisialisasi
    show_banner()
    vpn = VPNManager()
    dns = DNSManager()
    
    def status_callback(ip_info):
        """Callback saat IP berhasil dirotate"""
        print(f"\n\033[1;36m[•] IP Baru: {ip_info['ip']}")
        print(f"Lokasi: {ip_info['country']}\033[0m")
    try:
        while True:
            show_menu()
            choice = input("\n\033[1;36mPilih menu: \033[0m")
            
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
            elif choice == '2':  # Auto-rotate
            try:
                interval = int(input("Interval (menit): ")) * 60
                vpn.start_auto_rotate(interval, status_callback)
            except ValueError:
                print("\033[1;31m[!] Masukkan angka valid\033[0m")
                
            elif choice == '3':
                print("\n\033[1;34mDNS SERVERS:\033[0m")
                for i, server in enumerate(dns.DNS_SERVERS.keys(), 1):
                    print(f"{i}. {server} ({dns.DNS_SERVERS[server]})")
                
                try:
                    selection = int(input("\nPilih DNS (1-4): ")) - 1
                    dns.set_dns(list(dns.DNS_SERVERS.keys())[selection])
                except:
                    print("\033[1;31m[!] Pilihan tidak valid\033[0m")
            
            elif choice == '4':
                show_status(
                    {'server': vpn.connected_server},
                    vpn.get_ip_info()
                )
            
            elif choice == '5':
                vpn.disconnect()
                print("\033[1;32m[✓] VPN disconnected\033[0m")
            
            elif choice == '6':
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
