import os
import time
import random

class VPNManager:
    def __init__(self):
        self.ip_list = self._load_ip_list()
        self.current_connection = None

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
auth-user-pass
username {server['username']}
password {server['password']}
resolv-retry infinite
nobind
persist-key
persist-tun
""")

        os.system("openvpn --config temp_vpn.conf --daemon")
        time.sleep(3)
        print(f"\033[1;32m[✓] Connected to {server_name}\033[0m")
        self.current_connection = server_name
        return True

    def auto_rotate(self, interval=300):
        """Ganti IP otomatis"""
        while True:
            server = random.choice(list(self.ip_list.keys()))
            self.connect(server)
            time.sleep(interval)
