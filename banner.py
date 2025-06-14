def show_banner():
    print("""\033[1;36m
   _____ _______       _____  _____  
  |_   _|__   __|/\   |  __ \|  __ \ 
    | |    | |  /  \  | |__) | |__) |
    | |    | | / /\ \ |  ___/|  ___/ 
   _| |_   | |/ ____ \| |    | |     
  |_____|  |_/_/    \_\_|    |_|     

  \033[1;32mTermux VPN Rotator Pro
  \033[1;33m• Auto-IP Rotation
  \033[1;35m• Multi-Server Support
  \033[1;34m• DNS Protection
  \033[1;36m• Fake Gps
  \033[1;37m• Auto Update
  \033[1;31m• No Root Required
  \033[0m""")

def show_status(ip_info, server_name):
    print(f"""\033[1;35m
  ╔══════════════════════════╗
  ║       VPN STATUS        ║
  ╠══════════════════════════╣
  ║ Server: {server_name or 'Not Connected':<16} ║
  ║ IP: {ip_info.get('ip','Unknown'):<21}║
  ║ Location: {ip_info.get('country','Unknown'):<14} ║
  ║ City: {ip_info.get('city','Unknown'):<18} ║
  ╚══════════════════════════╝
  \033[0m""")
