class GPSSpoofer:
    @staticmethod
    def _ensure_adb_connection():
        """Pastikan koneksi ADB aktif"""
        max_retries = 3
        for _ in range(max_retries):
            try:
                # Cek status koneksi
                result = subprocess.getoutput("adb devices")
                if "127.0.0.1:5555" in result:
                    return True
                
                # Jika belum terkoneksi
                print("\033[1;33m[•] Establishing ADB connection...\033[0m")
                os.system("adb kill-server > /dev/null 2>&1")
                os.system("adb start-server > /dev/null 2>&1")
                os.system("adb connect 127.0.0.1:5555 > /dev/null 2>&1")
                time.sleep(2)  # Beri waktu untuk koneksi
            except Exception as e:
                print(f"\033[1;31m[!] ADB Error: {str(e)}\033[0m")
        return False

    @staticmethod
    def set_location(lat, lon):
        if not GPSSpoofer._ensure_adb_connection():
            print("\033[1;31m[×] Pastikan:\n1. USB Debugging aktif\n2. Termux punya akses Mock Location\033[0m")
            return False
        
        try:
            # Set lokasi
            os.system(f"adb shell am start-foreground-service -n 'com.termux/com.termux.app.TermuxService' -a 'fake.gps.set' --ef lat {lat} --ef lng {lon}")
            print(f"\033[1;32m[✓] Lokasi diubah ke: {lat}, {lon}\033[0m")
            return True
        except Exception as e:
            print(f"\033[1;31m[!] Gagal set lokasi: {str(e)}\033[0m")
            return False
