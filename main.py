#!/data/data/com.termux/files/usr/bin/python3
from banner import show_banner, show_status
from vpn_manager import VPNManager
from dns_manager import DNSManager
from gps_spoofer import GPSSpoofer
from updater import Updater
import os
import sys
import time
import signal

# Inisialisasi
vpn = VPNManager()
dns = DNSManager()
gps = GPSSpoofer()
updater = Updater()

def signal_handler(sig, frame):
    print("\n\033[1;33m[!] Received CTRL+C, cleaning up...\033[0m")
    vpn.disconnect()
    sys.exit(0)

def show_menu():
    print("\n\033[1;33mMAIN MENU:\033[0m")
    print("1. Connect VPN Manual")
    print("2. Auto-Rotate VPN (Ganti IP Otomatis)")
    print("3. Change DNS Server")
    print("4. Check Status")
    print("5. Stop Auto-Rotate")
    print("6. Fake GPS")
    print("7. Auto Update")
    print("8. Exit")
    
def main():
    os.system("adb connect 127.0.0.1:5555 > /dev/null 2>&1")
    show_banner()
    show_status(vpn.get_ip_info(), vpn.connected_server)
    
    def status_callback(ip_info):
        """Callback saat IP berhasil dirotate"""
        print(f"\n\033[1;36m[•] IP Baru: {ip_info['ip']}")
        print(f"Lokasi: {ip_info['country']}\033[0m")
    
    signal.signal(signal.SIGINT, signal_handler)
    try:
        while True:
            show_menu()
            choice = input("\n\033[1;36mPilih menu: \033[0m")
            
            if choice == '1':
                print("\nAvailable Servers:")
                for i, name in enumerate(vpn.ip_list.keys(), 1):
                    print(f"{i}. {name}")
                try:
                    selection = int(input("Pilih server: ")) - 1
                    server_name = list(vpn.ip_list.keys())[selection]
                    vpn.connect(server_name)
                except:
                    print("\033[1;31m[!] Input tidak valid\033[0m")
            elif choice == '2':
                try :
                    interval = int(input("Interval (detik): "))
                    print("\033[1;33m[!] Auto-rotate mulai...\033[0m")
                    vpn.auto_rotate(interval)
                except ValueError:
                    print("\033[1;31m[!] Masukkan angka\033[0m")
                
            elif choice == '3':
                print("\n\033[1;34mDNS SERVERS:\033[0m")
                for i, server in enumerate(dns.DNS_SERVERS.keys(), 1):
                    print(f"{i}. {server} ({dns.DNS_SERVERS[server]})")
                
                try:
                    selection = int(input("\nPilih DNS (1-4): ")) - 1
                    dns.set_dns(list(dns.DNS_SERVERS.keys())[selection])
                except:
                    print("\033[1;31m[!] Pilihan tidak valid\033[0m")
            
            elif choice == '4':  # Check Status
                if not hasattr(vpn, 'get_ip_info'):
                    print("\033[1;31m[!] Fitur cek IP tidak tersedia\033[0m")
                else:
                    ip_info = vpn.get_ip_info()
                    print("\n\033[1;36m=== STATUS TERKINI ===\033[0m")
                    print(f"VPN: {vpn.connected_server or 'Tidak terhubung'}")
                    print(f"IP: {ip_info['ip']}")
                    print(f"Lokasi: {ip_info['city']}, {ip_info['country']}")
                    print(f"ISP: {ip_info['isp']}")
            
            elif choice == '5':  # Stop Auto-Rotate
                if hasattr(vpn, 'disconnect'):
                    vpn.disconnect()
                else:
                    print("\033[1;31m[!] Fitur disconnect tidak tersedia\033[0m")
    
                if hasattr(vpn, 'stop_auto_rotate'):
                    vpn.stop_auto_rotate()

            elif choice == '6':  # Fake GPS
                print("\n\033[1;35mFAKE GPS OPTIONS:\033[0m")
                print("1. Set Random Location")
                print("2. Input Coordinates")
                print("3. Back")
    
                gps_choice = input("Pilih opsi: ")
    
                if gps_choice == '1':
                    lat, lon = gps.random_location()
                    if gps.set_location(lat, lon):
                        print(f"\033[1;32m[✓] Lokasi acak dipilih: {lat}, {lon}\033[0m")
    
                elif gps_choice == '2':
                    try:
                        lat = float(input("Latitude (-90 to 90): "))
                        lon = float(input("Longitude (-180 to 180): "))
                        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                            raise ValueError
                        if gps.set_location(lat, lon):
                            print(f"\033[1;32m[✓] Lokasi diatur ke: {lat}, {lon}\033[0m")
                    except:
                        print("\033[1;31m[!] Koordinat tidak valid\033[0m")

            elif choice == '7':  # Update Script
                if updater.check_update():
                    updater.self_update()
            
            elif choice == '8':
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
    try :
        # Persiapan environment
        if not os.path.exists('/data/data/com.termux/files/usr/bin/openvpn'):
            print("\033[1;31m[!] OpenVPN belum terinstall!")
            print("Jalankan: pkg install openvpn -y\033[0m")
            sys.exit(1)
        # Cek ADB terlebih dahulu
        if os.system("adb devices > /dev/null 2>&1") != 0:
            print("\033[1;33m[!] Jalankan ini terlebih dahulu:")
            print("adb tcpip 5555")
            print("adb connect 127.0.0.1:5555\033[0m")
        else :
            os.system("clear")
            main()
    except KeyboardInterrupt:
        print("\n\033[1;33m[!] Program dihentikan\033[0m")
        sys.exit(0)
