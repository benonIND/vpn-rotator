import os
import subprocess

class DNSManager:
    DNS_SERVERS = {
        'adguard': '94.140.14.14',
        'quad9': '9.9.9.9',
        'cloudflare': '1.1.1.1',
        'opendns': '208.67.222.222'
    }

    def __init__(self):
        self.resolv_conf = '/data/data/com.termux/files/usr/etc/resolv.conf'
        self.current_dns = None

    def set_dns(self, server_name):
        if server_name not in self.DNS_SERVERS:
            raise ValueError(f"DNS server tidak valid. Pilihan: {', '.join(self.DNS_SERVERS.keys())}")
        
        dns_ip = self.DNS_SERVERS[server_name]
        try:
            with open(self.resolv_conf, 'w') as f:
                f.write(f"nameserver {dns_ip}")
            self.current_dns = server_name
            print(f"\033[1;32m[✓] DNS diatur ke {server_name} ({dns_ip})\033[0m")
            self.flush_dns()
            return True
        except Exception as e:
            print(f"\033[1;31m[!] Gagal mengubah DNS: {str(e)}\033[0m")
            return False

    def flush_dns(self):
        try:
            subprocess.run(['termux-wifi-scaninfo'], check=False)  # Trigger refresh
            print("\033[1;33m[!] DNS cache di-flush\033[0m")
        except:
            pass

    def get_current_dns(self):
        try:
            with open(self.resolv_conf, 'r') as f:
                return f.read().strip()
        except:
            return "Unknown"
