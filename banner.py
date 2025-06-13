def show_banner():
    print("""\033[1;36m
   _____ _______       _____  _____  
  |_   _|__   __|/\   |  __ \|  __ \ 
    | |    | |  /  \  | |__) | |__) |
    | |    | | / /\ \ |  ___/|  ___/ 
   _| |_   | |/ ____ \| |    | |     
  |_____|  |_/_/    \_\_|    |_|     

  \033[1;32mTermux Privacy Toolkit
  \033[1;33mFitur:
  - Rotasi IP via Tor
  - DNS Adblock
  - Geolokasi Acak
  \033[1;31m⚠ Gunakan Secara Bertanggung Jawab ⚠
  \033[0m""")

def show_status(ip, country, dns_server):
    print(f"""\033[1;35m
  STATUS:
  IP: {ip}
  Lokasi: {country}
  DNS: {dns_server}
  \033[0m""")
