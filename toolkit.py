import pyfiglet
from termcolor import colored
import time
import os
import socket
import platform

# ─────────────────────────────────────────────
# ✅ GAYA & SUARA
# ─────────────────────────────────────────────

def beep():
    if platform.system() == 'Windows':
        import winsound
        winsound.Beep(1000, 150)

def banner(text):
    ascii_art = pyfiglet.figlet_format(text)
    print(colored(ascii_art, 'green'))

def loading(text, delay=0.1):
    print(colored(text, 'yellow'), end='', flush=True)
    for _ in range(10):
        print(colored('.', 'yellow'), end='', flush=True)
        time.sleep(delay)
    print('\n')

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# ─────────────────────────────────────────────
# ✅ FITUR
# ─────────────────────────────────────────────

def identitas_dev():
    banner("ANONNYMOUS")
    print(colored("Author  : Mr Robot", 'cyan'))
    print(colored("Versi   : 1.0", 'cyan'))
    print(colored("GitHub  : https://github.com/RenBaelish", 'cyan'))
    print(colored("Status  : Edukasi & Aman ✅", 'green'))
    print('-' * 40)
    time.sleep(1)

def scan_subdomain():
    loading("Scanning subdomain")
    fake_subs = ["admin.site.com", "api.site.com", "dev.site.com"]
    for sub in fake_subs:
        time.sleep(0.3)
        print(colored(f"[+] Ditemukan: {sub}", 'green'))
        beep()

def vuln_checker():
    loading("Cek kerentanan...")
    vulns = [
        "[-] Header X-Frame-Options tidak ditemukan",
        "[-] X-Powered-By bocor: PHP/5.6.40",
        "[-] Potensi SQLi pada URL parameter"
    ]
    for v in vulns:
        time.sleep(0.4)
        print(colored(v, 'red'))
        beep()

def pamer_mode():
    loading("Mengaktifkan mode pamer")
    banner("H4CK3R M0D3")
    for _ in range(3):
        print(colored(">> Akses granted ke sistem target... ", 'green'))
        time.sleep(0.5)
        print(colored(">> Menyuntikkan payload... ", 'yellow'))
        time.sleep(0.5)
        print(colored(">> Sukses! 🔥", 'red'))
        time.sleep(0.5)
        beep()
    print(colored("Temanmu sekarang takut. Misi selesai 😎", 'cyan'))

def cari_ip():
    domain = input(colored("Masukkan domain (contoh: google.com): ", 'cyan'))
    try:
        ip = socket.gethostbyname(domain)
        print(colored(f"[+] Alamat IP: {ip}", 'green'))
    except socket.gaierror:
        print(colored("[!] Gagal menemukan IP. Domain tidak valid atau offline.", 'red'))

def mock_lokasi():
    ip = input(colored("Masukkan IP Address (contoh: 8.8.8.8): ", 'cyan'))
    loading(f"Mencari lokasi dari {ip}")
    lokasi = {
        "Negara": "Amerika Serikat",
        "Kota": "Mountain View",
        "ISP": "Google LLC",
        "Koordinat": "37.3860° N, 122.0838° W"
    }
    for key, val in lokasi.items():
        print(colored(f"{key}: {val}", 'green'))
        time.sleep(0.3)

def keluar_berkelas():
    banner("BYE")
    pesan = "Terima kasih telah menggunakan tool ini.\nTetap belajar, tetap berkarya, tetap misterius 🥷"
    for huruf in pesan:
        print(colored(huruf, 'yellow'), end='', flush=True)
        time.sleep(0.03)
    print()

# ─────────────────────────────────────────────
# ✅ MENU & MAIN
# ─────────────────────────────────────────────

def menu():
    print(colored("\n===== MENU TOOL RENNBAELISH =====", 'yellow'))
    print(colored("1. Fake Subdomain Scanner", 'cyan'))
    print(colored("2. Fake Vulnerability Checker", 'cyan'))
    print(colored("3. Mode Pamer ke Teman", 'cyan'))
    print(colored("4. Cari IP dari Domain", 'cyan'))
    print(colored("5. Lihat Lokasi dari IP (Mock)", 'cyan'))
    print(colored("6. Exit", 'cyan'))

def main():
    clear()
    identitas_dev()
    loading("Memuat fitur elit")

    while True:
        menu()
        choice = input(colored("Pilih menu > ", 'green'))

        if choice == '1':
            scan_subdomain()
        elif choice == '2':
            vuln_checker()
        elif choice == '3':
            pamer_mode()
        elif choice == '4':
            cari_ip()
        elif choice == '5':
            mock_lokasi()
        elif choice == '6':
            keluar_berkelas()
            break
        else:
            print(colored("Pilihan tidak valid!", 'red'))

        input(colored("\nTekan Enter untuk kembali ke menu...", 'cyan'))
        clear()
        identitas_dev()

if __name__ == "__main__":
    main()

