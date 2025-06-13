import os
import requests
import random
import time
import threading
from urllib.parse import urlparse

class VPNManager:
    # Daftar server VPN gratis (OpenVPN config)
    VPN_SERVERS = {
        "ProtonVPN-Free": {
            "config_url": "https://account.protonvpn.com/api/vpn/logicals/Free",
            "type": "openvpn"
        },
        "VPNGate-US": {
            "config_url": "http://www.vpngate.net/api/iphone/",
            "server_id": 1,  # US server
            "type": "openvpn"
        },
        "FreeVPN-UK": {
            "config_url": "https://freevpn.me/accounts/",
            "credential": "freevpn/freevpn",
            "type": "openvpn"
        }
    }
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
    def __init__(self):
        self.current_vpn = None
        self.vpn_process = None

    def get_free_config(self, provider):
        """Download config VPN gratis"""
        try:
            if provider == "ProtonVPN-Free":
                resp = requests.get(self.FREE_VPN_SERVERS[provider]["config_url"])
                return resp.json()["LogicalServers"][0]["Servers"][0]["OpenVPNConfig"]
            elif provider == "VPNGate-US":
                resp = requests.get(self.FREE_VPN_SERVERS[provider]["config_url"])
                return resp.text.split("\n")[self.FREE_VPN_SERVERS[provider]["server_id"]]
            elif provider == "FreeVPN-UK":
                return f"""
                client
                dev tun
                proto udp
                remote uk.freevpn.me 1194
                auth-user-pass cred.txt
                """
        except Exception as e:
            print(f"⚠️ Gagal download config: {str(e)}")
            return None

    def connect(self, server_alias):
        """Connect to VPN server"""
        if server_alias not in self.FREE_VPN_SERVERS:
            print(f"❌ Server {server_alias} tidak tersedia")
            return False

        print(f"🔗 Menyiapkan {server_alias}...")
        config = self.get_free_config(server_alias)
        
        if not config:
            return False

        # Simpan config
        with open("vpnconfig.ovpn", "w") as f:
            f.write(config)

        # Jika butuh auth
        if "credential" in self.FREE_VPN_SERVERS[server_alias]:
            with open("cred.txt", "w") as f:
                f.write(self.FREE_VPN_SERVERS[server_alias]["credential"])

        # Jalankan OpenVPN
        self.vpn_process = os.popen(f"openvpn --config vpnconfig.ovpn &")
        time.sleep(10)  # Tunggu koneksi
        
        if self.check_connection():
            self.current_vpn = server_alias
            print(f"✅ Terhubung ke {server_alias} | IP: {self.get_current_ip()}")
            return True
        return False

    def disconnect(self):
        """Disconnect VPN"""
        if self.vpn_process:
            os.system("pkill openvpn")
            print("🔒 VPN dimatikan")
            self.current_vpn = None

    def check_connection(self):
        """Cek status koneksi"""
        try:
            ip = self.get_current_ip()
            return ip != requests.get('https://api.ipify.org').text
        except:
            return False

    def get_ip_info(self):
        """Get current IP address"""
        try:
            return requests.get('https://api.ipify.org', timeout=5).text
        except:
            return "Tidak terdeteksi"

    def list_servers(self):
        """List available VPN servers"""
        print("\n🔍 Daftar VPN Gratis:")
        for i, server in enumerate(self.FREE_VPN_SERVERS.keys(), 1):
            print(f"{i}. {server}")
