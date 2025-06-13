import os
import requests
import threading
import time
import subprocess
from urllib.request import urlretrieve

class VPNManager:
    FREE_SERVERS = {
        "ProtonVPN-Free-NL": {
            "config_url": "https://account.protonvpn.com/api/vpn/logicals/Free",
            "type": "openvpn",
            "region": "Netherlands"
        },
        "VPNGate-US": {
            "config_url": "http://www.vpngate.net/api/iphone/",
            "type": "openvpn",
            "server_id": 2174,  # ID server US
            "region": "United States"
        },
        "FreeVPN-UK": {
            "config_url": "https://freevpn.me/accounts/",
            "type": "openvpn",
            "credentials": ("freevpn", "freevpn"),
            "region": "United Kingdom"
        }
    }

    def __init__(self):
        self.process = None
        self.connected_server = None
        self.config_dir = os.path.expanduser("~/.vpn_configs")
        os.makedirs(self.config_dir, exist_ok=True)

    def start_auto_rotate(self, interval=300, callback=None):
        """Mulai auto-rotate IP setiap X detik"""
        self.stop_auto_rotate()  # Hentikan thread sebelumnya
        
        self._rotate_active = True
        def rotation_loop():
            while getattr(self, '_rotate_active', False):
                try:
                    new_server = random.choice(list(self.FREE_SERVERS.keys()))
                    if self.connect(new_server) and callback:
                        callback(self.get_ip_info())
                except Exception as e:
                    print(f"\033[1;31m[!] Rotate error: {e}\033[0m")
                time.sleep(interval)
        
        self._rotate_thread = threading.Thread(target=rotation_loop)
        self._rotate_thread.daemon = True
        self._rotate_thread.start()
        print(f"\033[1;32m[✓] Auto-rotate aktif setiap {interval//60} menit\033[0m")

    def stop_auto_rotate(self):
        """Hentikan auto-rotate"""
        if hasattr(self, '_rotate_thread'):
            self._rotate_active = False
            self._rotate_thread.join()
            print("\033[1;33m[!] Auto-rotate dihentikan\033[0m")
            
    def _download_config(self, server_name):
        """Download config file dari server gratis"""
        server = self.FREE_SERVERS[server_name]
        config_path = os.path.join(self.config_dir, f"{server_name}.ovpn")

        try:
            if server_name == "ProtonVPN-Free-NL":
                resp = requests.get(server["config_url"]).json()
                config = resp["LogicalServers"][0]["Servers"][0]["OpenVPNConfig"]
                with open(config_path, "w") as f:
                    f.write(config)
            
            elif server_name == "VPNGate-US":
                resp = requests.get(server["config_url"]).text
                lines = resp.split('\n')
                config = lines[server["server_id"] + 2]  # Ambil config dari CSV
                with open(config_path, "w") as f:
                    f.write(config.replace(",", "\n"))
            
            elif server_name == "FreeVPN-UK":
                config = f"""
                client
                dev tun
                proto udp
                remote uk.freevpn.me 1194
                auth-user-pass {self.config_dir}/creds.txt
                """
                with open(config_path, "w") as f:
                    f.write(config.strip())
                with open(f"{self.config_dir}/creds.txt", "w") as f:
                    f.write(f"{server['credentials'][0]}\n{server['credentials'][1]}")

            return config_path
        except Exception as e:
            print(f"\033[1;31m[!] Download gagal: {str(e)}\033[0m")
            return None

    def connect(self, server_name):
        """Hubungkan ke server VPN gratis"""
        if server_name not in self.FREE_SERVERS:
            print(f"\033[1;31m[!] Server {server_name} tidak tersedia\033[0m")
            return False

        print(f"\033[1;34m[•] Menyiapkan {server_name} ({self.FREE_SERVERS[server_name]['region']})...\033[0m")
        
        config_file = self._download_config(server_name)
        if not config_file:
            return False

        try:
            # Jalankan OpenVPN di background
            self.process = subprocess.Popen([
                "openvpn",
                "--config", config_file,
                "--auth-user-pass", f"{self.config_dir}/creds.txt",
                "--daemon"
            ])
            time.sleep(8)  # Tunggu koneksi

            if self._check_connection():
                self.connected_server = server_name
                ip_info = self.get_ip_info()
                print(f"\033[1;32m[✓] Terhubung ke {server_name}")
                print(f"IP: {ip_info['ip']}")
                print(f"Lokasi: {ip_info['country']}\033[0m")
                return True
            
            print("\033[1;31m[!] Gagal terhubung\033[0m")
            return False
        except Exception as e:
            print(f"\033[1;31m[!] Error: {str(e)}\033[0m")
            return False

    def disconnect(self):
        """Putuskan koneksi VPN"""
        if self.process:
            self.process.terminate()
        os.system("pkill openvpn")
        self.connected_server = None
        print("\033[1;33m[!] VPN dimatikan\033[0m")

    def _check_connection(self):
        """Cek status koneksi"""
        try:
            original_ip = requests.get('https://api.ipify.org', timeout=3).text
            vpn_ip = requests.get('https://api.ipify.org', timeout=3, 
                                proxies={'http': 'socks5://127.0.0.1:9050'}).text
            return original_ip != vpn_ip
        except:
            return False

    def get_ip_info(self):
        """Dapatkan info IP terkini"""
        try:
            resp = requests.get('http://ip-api.com/json', timeout=5)
            data = resp.json()
            return {
                'ip': data.get('query', 'Unknown'),
                'country': data.get('country', 'Unknown'),
                'city': data.get('city', 'Unknown'),
                'isp': data.get('isp', 'Unknown')
            }
        except:
            return {'ip': 'Error', 'country': 'Unknown', 'city': 'Unknown'}

    def list_servers(self):
        """Daftar server gratis yang tersedia"""
        print("\n\033[1;36mFREE VPN SERVERS:\033[0m")
        for i, (name, details) in enumerate(self.FREE_SERVERS.items(), 1):
            print(f"{i}. {name} ({details['region']})")
