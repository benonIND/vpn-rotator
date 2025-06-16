import httpx

ADGUARD_DOH = "https://dns.adguard-dns.com/resolve"

def check_domain_status(domain: str) -> bool:
    """
    Mengembalikan True jika domain diblokir oleh AdGuard (status = 3 atau tidak ada jawaban),
    dan False jika tidak diblokir.
    """
    try:
        response = httpx.get(
            ADGUARD_DOH,
            params={"name": domain, "type": "A"},
            headers={"accept": "application/dns-json"},
            timeout=5
        )
        json_data = response.json()
        status = json_data.get("Status", -1)
        if status == 3 or "Answer" not in json_data:
            return True
        return False
    except Exception as e:
        print(f"[!] Error checking {domain}: {e}")
        return False
