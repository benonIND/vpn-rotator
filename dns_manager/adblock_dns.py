import dns.resolver
import requests

# === DNS Filtering AdGuard ===
ADGUARD_DNS = ["94.140.14.14", "94.140.15.15"]

def set_adblock_dns():
    """Set resolver DNS ke AdGuard DNS"""
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = ADGUARD_DNS
    resolver.timeout = 10
    resolver.lifetime = 10
    dns.resolver.default_resolver = resolver
    print("[+] DNS resolver telah diganti ke AdGuard:", ADGUARD_DNS)

def restore_default_resolver():
    """Kembalikan ke DNS resolver default sistem"""
    resolver = dns.resolver.Resolver()
    dns.resolver.default_resolver = resolver
    print("[*] DNS resolver dikembalikan ke default sistem.")

def test_dns_resolver():
    """Cek apakah ads.google.com diblokir oleh DNS saat ini"""
    try:
        answer = dns.resolver.resolve("ads.google.com")
        print("[!] DNS aktif, tetapi ads.google.com resolve ke:", [rdata.address for rdata in answer])
        return False
    except dns.resolver.NXDOMAIN:
        print("[✓] DNS bekerja: ads.google.com diblokir.")
        return True
    except Exception as e:
        print("[!] Error saat cek DNS:", e)
        return False

def check_ip_dns():
    """Cek IP publik dan status pemblokiran DNS"""
    try:
        ip = requests.get("https://api.ipify.org").text
        print("[✓] IP Publik Anda:", ip)
        test_dns_resolver()
    except Exception as e:
        print("[!] Gagal cek IP publik:", e)
