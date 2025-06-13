import os
import requests
import time
from urllib.request import urlopen

class VPNManager:
    SERVERS = {
        'US': {'ip': 'us.vpn.example.com', 'port': 1194},
        'UK': {'ip': 'uk.vpn.example.com', 'port': 1194},
        'JP': {'ip': 'jp.vpn.example.com', 'port': 1194}
    }

    def __init__(self):
        self.connected = False
        self.current_server = None

    def connect(self, country):
        try:
            if country not in self.SERVERS:
                raise ValueError(f"Country not available. Choose from: {', '.join(self.SERVERS.keys())}")
            
            server = self.SERVERS[country]
            print(f"\033[1;34m[•] Connecting to {country} server...\033[0m")
            
            # Simulate connection (replace with actual VPN command)
            os.system(f"termux-open-url 'vpn://{server['ip']}:{server['port']}'")
            time.sleep(5)
            
            if self.check_connection():
                self.connected = True
                self.current_server = country
                print(f"\033[1;32m[✓] Connected to {country}\033[0m")
                return True
            return False
        except Exception as e:
            print(f"\033[1;31m[!] Connection failed: {str(e)}\033[0m")
            return False

    def disconnect(self):
        try:
            os.system("termux-vpn disconnect")
            self.connected = False
            self.current_server = None
            print("\033[1;33m[!] VPN disconnected\033[0m")
            return True
        except Exception as e:
            print(f"\033[1;31m[!] Disconnect failed: {str(e)}\033[0m")
            return False

    def check_connection(self):
        try:
            resp = requests.get('https://api.ipify.org', timeout=5)
            return resp.status_code == 200
        except:
            return False

    def get_ip_info(self):
        try:
            resp = requests.get('http://ip-api.com/json', timeout=5)
            data = resp.json()
            return {
                'ip': data.get('query', 'Unknown'),
                'country': data.get('country', 'Unknown'),
                'city': data.get('city', 'Unknown')
            }
        except Exception as e:
            print(f"\033[1;31m[!] IP check failed: {str(e)}\033[0m")
            return {'ip': 'Error', 'country': 'Unknown', 'city': 'Unknown'}
