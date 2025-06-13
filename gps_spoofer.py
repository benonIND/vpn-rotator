import subprocess
import random

def set_mock_location(lat, lon):
    """Set lokasi GPS palsu via ADB"""
    try:
        # Perintah ADB untuk set lokasi mock
        subprocess.run([
            'adb', 'shell', 'settings', 'put', 'secure', 'mock_location', '1'
        ], check=True)
        
        subprocess.run([
            'adb', 'shell', 'am', 'start-foreground-service',
            f'--ei latitude {lat} --ei longitude {lon}',
            'com.termux.location_poller/.LocationPollerService'
        ], check=True)
        
        print(f"\033[1;32m[✓] Lokasi GPS diubah ke: {lat}, {lon}\033[0m")
    except Exception as e:
        print(f"\033[1;31m[!] Gagal mengubah GPS: {e}\033[0m")
        print("\033[1;33mPastikan:")
        print("- ADB terhubung (adb tcpip 5555)")
        print("- Mock location diaktifkan di Developer Options\033[0m")

def generate_random_location():
    """Generate koordinat acak di seluruh dunia"""
    lat = round(random.uniform(-90, 90), 6)
    lon = round(random.uniform(-180, 180), 6)
    return lat, lon