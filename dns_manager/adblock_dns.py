import httpx

ADGUARD_DOH_JSON = "https://dns.adguard-dns.com/resolve"

def test_block(domain):
    print(f"[*] Mengecek: {domain}")
    try:
        resp = httpx.get(
            ADGUARD_DOH_JSON,
            params={"name": domain, "type": "A"},
            headers={"Accept": "application/dns-json"},
            timeout=5
        )
        data = resp.json()

        if data.get("Status") == 3:
            print(f"[✓] {domain} DIBLOKIR (NXDOMAIN)")
            return True
        elif "Answer" in data:
            ips = ', '.join([a['data'] for a in data['Answer']])
            print(f"[✗] {domain} TIDAK diblokir (resolves to {ips})")
            return False
        else:
            print("[?] Respon tidak jelas:", data)
            return False
    except Exception as e:
        print("[!] Gagal melakukan DoH:", e)
        return False

def test_blacklist_from_file(file_path="ad_blacklist.txt"):
    try:
        with open(file_path, "r") as f:
            domains = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        print(f"\n[•] Mulai cek {len(domains)} domain dari {file_path}...\n")
        results = {}
        for domain in domains:
            results[domain] = test_block(domain)
        return results
    except FileNotFoundError:
        print(f"[!] File '{file_path}' tidak ditemukan.")
        return {}
