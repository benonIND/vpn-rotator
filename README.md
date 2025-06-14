![GitHub Author](https://img.shields.io/badge/Author-yorima-blue?logo=github&style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white&style=for-the-badge)
![GitHub Version](https://img.shields.io/badge/Version-1.0.0-blueviolet?style=for-the-badge)
> [!NOTE]
> Dunia ini seperti algoritma—setiap masalah memiliki solusi, tapi tidak semua solusi efisien.

> [!IMPORTANT]
> jika terjadi error padahal sudah mengikuti panduan harap teliti errornya atau minta bantuan AI untuk analisis error

# Termux VPN Rotator Pro

VPN Manager dengan fitur auto-rotate IP dan DNS protection untuk Termux

## 🚀 Fitur Utama
- Auto ganti IP setiap X menit
- Support 100+ server via file config and list txt
- DNS adblock otomatis
- Cek status info
- Auto update
- Tanpa perlu root

## 📦 Instalasi
1. Install requirements:
```bash
pkg update && pkg install python root-repo openvpn -y
pip install requests
```

2. Download script:
```bash
git clone https://github.com/benonIND/vpn-rotator.git
cd vpn-rotator
```

3. Tambahkan server VPN di `ip_list.txt`:
```txt
# Format: ServerName,IP,Port,User,Pass
Japan1,45.76.43.123,1194,vpn,vpn
USA1,154.16.116.158,1194,vpn,vpn
```

## 🎯 Cara Pakai
```bash
python main.py
```
Menu:
1. Connect Manual
2. Auto-Rotate (Ganti IP otomatis)
3. Ganti DNS Server
4. Cek Status
5. Stop VPN

## 🛠️ Troubleshooting
### ❌ Error: "Unable to locate package openvpn"
```bash
termux-change-repo  # Pilih mirror group 1
pkg update
pkg install openvpn -y
```

### ❌ VPN Tidak Terhubung
1. Cek IP aktif:
```bash
ping 45.76.43.123
```
2. Update daftar IP:
```bash
curl -s https://www.vpngate.net/api/iphone/ | awk -F, '/Japan.*UDP/ {print $1,$14,$3}' >> ip_list.txt
```

### ❌ Auto-Rotate Tidak Berhenti
```bash
pkill -f "openvpn.*temp_vpn.conf"
pkill python
```

## 📌 Contoh Config
File `ip_list.txt`:
```txt
# Negara,IP,Port,User,Pass
Japan_VPN,45.76.43.123,1194,vpn,vpn
USA_VPN,154.16.116.158,1194,vpn,vpn
Germany_VPN,49.12.115.24,1194,vpn,vpn
```

## 📞 Support
Lapor issue di: [GitHub Issues](https://github.com/benonIND/vpn-rotator/issues)

### 🎨 Tampilan Banner di Termux
![Banner Preview](https://d.top4top.io/p_3451xke020.jpg)  
*(Gunakan terminal dengan tema biru untuk tampilan optimal)*

### 🔧 Struktur Proyek
```bash
📂 vpn-rotator/
├── 📄 .gitignore
├── 📄 LICENSE
├── 📄 README.md
├── 📄 banner.py
├── 📄 dns_manager.py
├── 📄 gps_spoofer.py
├── 📄 ip_changer.py
├── 📄 ip_list.txt
├── 📄 main.py
├── 📄 requirements.txt
├── 📄 updater.py
├── 📄 vpn_auth.txt
└── 📄 vpn_manager.py
```
