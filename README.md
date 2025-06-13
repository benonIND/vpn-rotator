# 🌐 IP/DNS Changer untuk Termux

Alat untuk mengubah IP address secara otomatis via Tor dan menerapkan DNS anti-iklan di Termux (Android).

## 🔧 Fitur Utama
- ✅ Ganti IP otomatis setiap 5 detik
- 🌍 Deteksi lokasi virtual (Negara, Kota, ISP)
- 🛡️ DNS anti-iklan (AdGuard + Cloudflare)
- 🎨 Tampilan berwarna dengan emoji
- 📱 Kompatibel dengan Termux (root/non-root)

## 📥 Instalasi
Pastikan Termux sudah terupdate:
```bash
pkg update && pkg upgrade
pkg install python tor -y
pip install stem requests
git clone https://github.com/benonIND/IP-and-DNS-change.git
cd ip-dns-changer
```

### jalankan tor di sessions yang berbeda
- tor ( enter )
- kembali ke sessions pertama jalankan
python main.py
