import socket
import time

def wait_for_internet(host="8.8.8.8", port=53, timeout=3, retries=5):
    print("[*] Menunggu koneksi internet tersedia...")
    for i in range(retries):
        try:
            with socket.create_connection((host, port), timeout=timeout):
                print("[✓] Koneksi internet aktif.")
                return True
        except OSError:
            print(f"[!] Tidak ada koneksi, percobaan ke-{i+1}/{retries}")
            time.sleep(2)
    print("[✗] Gagal mendeteksi internet.")
    return False
