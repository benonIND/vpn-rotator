from gps_spoofer import set_mock_location, generate_random_location
from ip_changer import change_tor_ip, get_ip_info

def start_ip_and_location_rotation(interval=10, change_gps=True):
    """Ganti IP + GPS secara periodik"""
    def rotation_thread():
        while True:
            # Dapatkan info IP baru
            change_tor_ip()
            ip_info = get_ip_info()
            
            # Update GPS sesuai lokasi IP
            if change_gps and ip_info['lat']:
                set_mock_location(ip_info['lat'], ip_info['lon'])
            
            print(f"""
\033[1;36m=== Rotasi Berhasil ===
IP: {ip_info['ip']}
Lokasi: {ip_info['city']}, {ip_info['country']}
Koordinat: {ip_info['lat']}, {ip_info['lon']}
\033[0m""")
            
            time.sleep(interval)
    
    threading.Thread(target=rotation_thread, daemon=True).start()