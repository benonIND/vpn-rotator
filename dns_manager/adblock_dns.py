import httpx

ADBLOCK_DOH_SERVERS = ["https://dns.adguard.com/dns-query"]

def test_block(domain):
    blocked = False
    print(f"\n[*] Mengecek domain: {domain}")

    for doh_url in ADBLOCK_DOH_SERVERS:
        try:
            params = {"name": domain, "type": "A"}
            headers = {"Accept": "application/dns-json"}

            resp = httpx.get(doh_url, params=params, headers=headers, timeout=5)
            data = resp.json()

            if "Answer" in data:
                print(f"[✗] {domain} TIDAK diblokir (IP: {', '.join([a['data'] for a in data['Answer']])})")
            elif data.get("Status") == 3:
                print(f"[✓] {domain} DIBLOKIR (NXDOMAIN) oleh DoH: {doh_url}")
                blocked = True
            else:
                print(f"[?] Hasil tak pasti dari {doh_url}: {data}")
        except Exception as e:
            print(f"[!] Gagal DoH {doh_url}: {e}")

    return blocked

def test_blacklist_from_file(file_path="ad_blacklist.txt"):
    try:
        with open(file_path, "r") as f:
            domains = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        print(f"\n[•] Mulai cek {len(domains)} domain iklan dari {file_path}...\n")
        for domain in domains:
            test_block(domain)
    except FileNotFoundError:
        print(f"[!] File '{file_path}' tidak ditemukan.")
