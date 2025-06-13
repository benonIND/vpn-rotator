# Termux VPN Rotator Pro

VPN Manager dengan fitur auto-rotate IP dan DNS protection untuk Termux

## 🚀 Fitur Utama
- Auto ganti IP setiap X menit
- Support 100+ server via file config
- DNS adblock otomatis
- Tanpa perlu root

## 📦 Instalasi
1. Install requirements:
```bash
pkg update && pkg install python openvpn -y
pip install requests
```

2. Download script:
```bash
git clone https://github.com/username/vpn-rotator.git
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
```

### 🎨 Tampilan Banner di Termux
![Banner Preview](https://i.imgur.com/example.png)  
*(Gunakan terminal dengan tema biru untuk tampilan optimal)*

### 🔧 Struktur Proyek
```
📂 vpn-rotator/
├── 📄 main.py
├── 📄 vpn_manager.py
├── 📄 banner.py
├── 📄 ip_list.txt
├── 📄 README.md
└── 📂 logs/
     └── vpn.log
```

Fitur khusus banner:
1. Warna terminal (ANSI escape codes)
2. Box status yang rapi
3. Informasi penting dalam layout compact
4. Support dark/light mode terminal

README.md mencakup:
✅ Instalasi lengkap  
✅ Contoh config  
✅ Solusi error umum  
※ Ganti `username` dengan GitHub Anda
