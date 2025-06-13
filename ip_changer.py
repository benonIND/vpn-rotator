from stem.control import Controller
import requests
import time

def change_tor_ip(country=None):
    """Ganti IP dengan opsi negara tertentu"""
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()
        
        if country:
            controller.set_conf('ExitNodes', f'{{{country}}}')  # Contoh: {us}
            print(f"\033[1;34m[•] Memilih exit node: {country.upper()}\033[0m")
        
        controller.signal(Signal.NEWNYM)
        time.sleep(5)

def get_ip_info():
    """Dapatkan detail IP termasuk lokasi"""
    try:
        response = requests.get('http://ip-api.com/json/').json()
        return {
            'ip': response.get('query', ''),
            'country': response.get('country', 'Unknown'),
            'city': response.get('city', 'Unknown'),
            'lat': response.get('lat', 0),
            'lon': response.get('lon', 0)
        }
    except:
        return {'ip': 'Error', 'country': 'Unknown', 'city': 'Unknown'}