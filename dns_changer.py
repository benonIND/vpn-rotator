import os
import subprocess

class DNSChanger:
    def __init__(self):
        self.ad_block_dns = ["94.140.14.14", "1.1.1.1"]  # AdGuard + Cloudflare

    def set_ad_block_dns(self):
        print("\n\033[1;36m[*] Mengaktifkan DNS anti iklan:\033[0m")
        for i, dns in enumerate(self.ad_block_dns):
            os.system(f'setprop net.dns{i+1} {dns}')
            print(f" - {dns}")
        print("\033[1;32m[+] DNS berhasil diubah\033[0m")

    def restore_default_dns(self):
        os.system('setprop net.dns1 ""')
        os.system('setprop net.dns2 ""')
        print("\033[1;32m[+] DNS dikembalikan ke default\033[0m")