import random
import os
import subprocess
import time

class GPSSpoofer:
    @staticmethod
    def random_location():
        """Generate random GPS coordinates"""
        lat = round(random.uniform(-90, 90), 6)
        lon = round(random.uniform(-180, 180), 6)
        return lat, lon

    @staticmethod
    def _check_adb():
        """Check ADB connection"""
        try:
            result = subprocess.getoutput("adb devices")
            return "127.0.0.1:5555" in result
        except:
            return False

    @staticmethod
    def set_location(lat, lon):
        """Set fake GPS location"""
        if not GPSSpoofer._check_adb():
            print("\033[1;31m[!] Connect ADB first:\n1. adb tcpip 5555\n2. adb connect 127.0.0.1:5555\033[0m")
            return False
            
        try:
            cmd = f"adb shell am start-foreground-service -n com.termux/com.termux.app.TermuxService -a fake.gps.set --ef lat {lat} --ef lng {lon}"
            os.system(cmd)
            print(f"\033[1;32m[✓] Location set to: {lat}, {lon}\033[0m")
            return True
        except Exception as e:
            print(f"\033[1;31m[!] Error: {str(e)}\033[0m")
            return False
