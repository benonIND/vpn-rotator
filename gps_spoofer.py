import os
import random

class GPSSpoofer:
    @staticmethod
    def set_location(lat, lon):
        """Set lokasi fake via ADB (tanpa root)"""
        try:
            # Cek device terhubung
            if os.system("adb devices > /dev/null 2>&1") != 0:
                raise Exception("ADB not connected")
            
            # Set mock location
            os.system(f"adb shell settings put secure mock_location 1")
            os.system(f"adb shell am start-foreground-service -a 'fake.gps.set' --ef lat {lat} --ef lng {lon}")
            print(f"\033[1;32m[✓] Lokasi diubah ke: {lat}, {lon}\033[0m")
            return True
        except Exception as e:
            print(f"\033[1;31m[!] Error: {str(e)}\033[0m")
            return False

    @staticmethod
    def random_location():
        """Generate lokasi acak"""
        lat = round(random.uniform(-90, 90), 6)
        lon = round(random.uniform(-180, 180), 6)
        return lat, lon
