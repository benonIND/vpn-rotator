import os

class DNSManager:
    DNS_SERVERS = {
        'adguard': '94.140.14.14',
        'cloudflare': '1.1.1.1',
        'google': '8.8.8.8',
        'default': '1.1.1.1'  # Fallback server
    }

    def __init__(self):
        self.resolv_conf = '/data/data/com.termux/files/usr/etc/resolv.conf'
        self.current_dns = None

    def set_dns(self, server_name):
        try:
            if server_name not in self.DNS_SERVERS:
                raise ValueError(f"Invalid DNS server. Available: {', '.join(self.DNS_SERVERS.keys())}")
            
            dns_ip = self.DNS_SERVERS[server_name]
            with open(self.resolv_conf, 'w') as f:
                f.write(f"nameserver {dns_ip}")
            
            self.current_dns = server_name
            print(f"\033[1;32m[✓] DNS set to {server_name} ({dns_ip})\033[0m")
            return True
        except Exception as e:
            print(f"\033[1;31m[!] DNS Error: {str(e)}\033[0m")
            return False
