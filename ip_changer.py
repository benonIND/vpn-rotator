import time
import requests
from stem import Signal
from stem.control import Controller
from stem.util import log
import threading

log.get_logger().disabled = True  # Nonaktifkan log Stem

class IPChanger:
    def __init__(self):
        self.running = False
        self.thread = None

    def get_ip_info(self):
        try:
            resp = requests.get('http://ip-api.com/json/', timeout=10)
            data = resp.json()
            return {
                'ip': data.get('query', 'N/A'),
                'country': data.get('country', 'N/A'),
                'city': data.get('city', 'N/A')
            }
        except:
            return {'ip': 'Error', 'country': 'N/A', 'city': 'N/A'}

    def change_ip(self):
        try:
            with Controller.from_port(port=9051) as controller:
                controller.authenticate()
                controller.signal(Signal.NEWNYM)
                time.sleep(5)  # Tunggu sirkuit baru
        except Exception as e:
            print(f"\033[1;31m[!] Tor Error: {str(e)}\033[0m")
            return False
        return True

    def start(self, interval=10):
        self.running = True
        def changer():
            while self.running:
                old_info = self.get_ip_info()
                if self.change_ip():
                    new_info = self.get_ip_info()
                    print(f"\n\033[1;34m[•] IP Lama: {old_info['ip']} ({old_info['country']})")
                    print(f"\033[1;32m[✓] IP Baru: {new_info['ip']} ({new_info['country']})\033[0m")
                time.sleep(interval)
        
        self.thread = threading.Thread(target=changer)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
