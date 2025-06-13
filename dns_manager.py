import os
import requests

class DNSManager:
    DNS_SERVERS = {
        'adguard': '94.140.14.14',
        'cloudflare': '1.1.1.1',
        'quad9': '9.9.9.9',
        'default': '8.8.8.8'
    }

    def __init__(self):
        self.resolv_conf = '/data/data/com.termux/files/usr/etc/resolv.conf'
        self.current_dns = None

    def set_dns(self, server_name):
        """Set DNS dengan pengecekan koneksi"""
        try:
            if server_name not in self.DNS_SERVERS:
                raise ValueError(f"Invalid DNS server. Choose from: {', '.join(self.DNS_SERVERS.keys())}")
            
            # Test DNS sebelum apply
            if not self._test_dns(self.DNS_SERVERS[server_name]):
                print("\033[1;33m[!] DNS server tidak merespon, menggunakan fallback\033[0m")
                server_name = 'default'

            with open(self.resolv_conf, 'w') as f:
                f.write(f"nameserver {self.DNS_SERVERS[server_name]}")
            
            self.current_dns = server_name
            print(f"\033[1;32m[✓] DNS aktif: {server_name} ({self.DNS_SERVERS[server_name]})\033[0m")
            return True
        except Exception as e:
            print(f"\033[1;31m[!] Error: {str(e)}\033[0m")
            return False

    def _test_dns(self, dns_ip):
        """Test responsivitas DNS server"""
        try:
            return os.system(f"ping -c 1 {dns_ip} > /dev/null") == 0
        except:
            return False
