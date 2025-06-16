from adblock_dns import *
from ../server.local_dns_server import start_dns_server

def start_dns_blocker():
    blacklist_path = "data/ads_blacklist.txt"
    try:
        with open(blacklist_path) as f:
            domains = [line.strip() for line in f if line.strip()]
        for domain in domains:
            status = check_domain_status(domain)
            print(f"[DNS Check] {domain}: {'BLOCKED' if status else 'NOT BLOCKED'}")
        start_dns_server(blacklist_path, port=5353)
        print("[✓] DNS blocker aktif di 127.0.0.1:5353")
    except Exception as e:
        print(f"[!] Gagal menjalankan DNS blocker: {e}")
