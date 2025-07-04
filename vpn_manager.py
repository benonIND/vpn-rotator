import os
import time
import random
import requests

class VPNManager:
    def __init__(self):
        self.ip_list = self._load_ip_list()
        self.current_connection = None
        self.connected_server = None
        self.openvpn_process = None
        self.rotate_active = False

    def get_ip_info(self):
        """Dapatkan informasi IP dan lokasi"""
        try:
            response = requests.get('http://ip-api.com/json', timeout=5)
            data = response.json()
            return {
                'ip': data.get('query', 'Unknown'),
                'country': data.get('country', 'Unknown'),
                'city': data.get('city', 'Unknown'),
                'isp': data.get('isp', 'Unknown')
            }
        except Exception as e:
            print(f"\033[1;31m[!] Error getting IP info: {str(e)}\033[0m")
            return {
                'ip': 'Error',
                'country': 'Unknown',
                'city': 'Unknown',
                'isp': 'Unknown'
            }
    
    def _load_ip_list(self):
        """Baca daftar IP dari file teks"""
        servers = {}
        try:
            with open("ip_list.txt", "r") as f:
                for line in f:
                    if line.strip() and not line.startswith("#"):
                        parts = line.strip().split(",")
                        servers[parts[0]] = {
                            "ip": parts[1],
                            "port": parts[2],
                            "username": parts[3],
                            "password": parts[4]
                        }
            return servers
        except Exception as e:
            print(f"\033[1;31m[!] Error baca ip_list.txt: {str(e)}\033[0m")
            return {}

    def connect(self, server_name):
        """Koneksi menggunakan IP dari list"""
        if not self.ip_list:
            print("\033[1;31m[!] Daftar IP kosong\033[0m")
            return False

        server = self.ip_list.get(server_name)
        if not server:
            print(f"\033[1;31m[!] Server {server_name} tidak ditemukan\033[0m")
            return False

        print(f"\033[1;34m[•] Connecting to {server_name} ({server['ip']})...\033[0m")
        
        # Buat config sementara
        with open("temp_vpn.conf", "w") as f:
            f.write(f"""
client
dev tun
proto udp
remote {server['ip']} {server['port']}
auth-user-pass vpn_auth.txt
resolv-retry infinite
nobind
persist-key
persist-tun
""")

        os.system("openvpn --config temp_vpn.conf --daemon")
        time.sleep(3)
        print(f"\033[1;32m[✓] Connected to {server_name}\033[0m")
        self.current_connection = server_name
        self.connected_server = server_name
        return True

    def disconnect(self):
        """Putuskan koneksi VPN"""
        try:
            if self.openvpn_process:
                os.kill(int(self.openvpn_process.pid), signal.SIGTERM)
            os.system("pkill -f 'openvpn.*temp_vpn.conf'")  # Double kill
            self.connected_server = None
            print("\033[1;32m[✓] VPN disconnected\033[0m")
            return True
        except Exception as e:
            print(f"\033[1;31m[!] Disconnect error: {str(e)}\033[0m")
            return False
    
    def auto_rotate(self, interval=300):
        """Ganti IP otomatis"""
        while True:
            server = random.choice(list(self.ip_list.keys()))
            self.connect(server)
            time.sleep(interval)
