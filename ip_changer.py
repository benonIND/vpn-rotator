import os
import time
import requests
from stem import Signal
from stem.control import Controller
from stem.connection import connect

class IPChanger:
    def __init__(self):
        self.check_tor()
    
    def check_tor(self):
        if not os.path.exists('/data/data/com.termux/files/usr/bin/tor'):
            print("\033[1;31m[!] Tor belum terinstall!")
            print("Jalankan: pkg install tor && pip install stem\033[0m")
            exit(1)

    def change_ip(self):
        try:
            controller = connect(
                control_port=9051,
                #auth_method="COOKIE",  # atau "PASSWORD"
                password= "wongedan"
            )
            if controller:
                controller.signal(Signal.NEWNYM)
        except Exception as e:
            print(f"[TOR ERROR] {str(e)}")

    def check_location(self):
        try:
            session = requests.session()
            session.proxies = {'http': 'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050'}
            res = session.get('https://ipapi.co/json/', timeout=10).json()
            
            print(f"\n\033[1;32m[+] IP: {res.get('ip')}")
            print(f"📍 Lokasi: {res.get('country_name')} ({res.get('city')})")
            print(f"🛜 ISP: {res.get('org')}\033[0m")
        except:
            print("\033[1;33m[!] Gagal deteksi lokasi\033[0m")

    def start_changing_ip(self, interval):
        print(f"\n\033[1;36m[*] Ganti IP otomatis setiap {interval} detik (CTRL+C untuk berhenti)\033[0m")
        while True:
            self.change_ip()
            time.sleep(interval)
