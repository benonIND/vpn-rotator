import requests
import os

class Updater:
    @staticmethod
    def check_update():
        """Cek update dari GitHub"""
        try:
            current_ver = "1.2.0"
            req = requests.get("https://raw.githubusercontent.com/username/vpn-rotator/main/version.txt")
            if req.status_code == 200:
                latest_ver = req.text.strip()
                if latest_ver != current_ver:
                    print(f"\033[1;33m[!] Update tersedia: v{latest_ver}\033[0m")
                    return True
            return False
        except:
            return False

    @staticmethod
    def self_update():
        """Update script otomatis"""
        try:
            os.system("git pull origin main 2>/dev/null || curl -L https://github.com/username/vpn-rotator/archive/main.zip -o update.zip && unzip -o update.zip")
            print("\033[1;32m[✓] Script berhasil diupdate\033[0m")
            return True
        except Exception as e:
            print(f"\033[1;31m[!] Gagal update: {str(e)}\033[0m")
            return False
