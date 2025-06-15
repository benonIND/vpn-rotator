import os
import subprocess

def is_git_repo(path):
    return os.path.exists(os.path.join(path, ".git"))

def run_git_command(args, cwd):
    try:
        result = subprocess.run(["git"] + args, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except Exception as e:
        return f"[ERROR] {e}"

def check_and_update_repo():
    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    if not is_git_repo(repo_dir):
        print("[ERROR] Direktori ini bukan repositori Git. Gunakan 'git clone' untuk kloning repositori.")
        return

    print("[INFO] Memeriksa pembaruan dari GitHub...")

    # Ambil update tanpa merge
    fetch_output = run_git_command(["fetch"], repo_dir)
    print(fetch_output)

    # Cek status lokal vs remote
    status_output = run_git_command(["status", "-uno"], repo_dir)
    if "Your branch is behind" in status_output:
        print("[INFO] Update tersedia. Menarik pembaruan...")
        pull_output = run_git_command(["pull"], repo_dir)
        print(pull_output)
        print("[SUCCESS] Script berhasil diperbarui.")
    else:
        print("[INFO] Sudah versi terbaru. Tidak ada update.")
