import time
import random
import pyfiglet
from termcolor import colored

# ─────────────────────────────────────────────
# ✅ FAKE LOGIN FUNCTION
# ─────────────────────────────────────────────

def fake_login():
    print(colored("\n[INFO] Memulai simulasi login palsu...", 'cyan'))
    time.sleep(1)

    # Form login palsu
    username = input(colored("Masukkan Username: ", 'yellow'))
    password = input(colored("Masukkan Password: ", 'yellow'))

    # Simulasikan proses login dengan delay
    print(colored("\n[INFO] Memverifikasi data...", 'cyan'))
    time.sleep(2)

    # Simulasi data yang berhasil dimasukkan (log ke file atau di terminal)
    print(colored(f"\n[INFO] Data yang dimasukkan:", 'green'))
    print(colored(f"Username: {username}", 'green'))
    print(colored(f"Password: {password}", 'green'))

    # Simulasi sukses login
    print(colored("\n[INFO] Login Berhasil! Selamat datang!", 'green'))
    print(colored("[INFO] Anda sekarang terhubung ke sistem.", 'green'))

    # Simulasi log data ke file (bisa ganti ke database atau sistem lain)
    with open("login_log.txt", "a") as log_file:
        log_file.write(f"Username: {username}, Password: {password}\n")

    print(colored("\n[INFO] Data login telah dicatat.", 'yellow'))

# ─────────────────────────────────────────────
# ✅ TAMPILKAN BANNER
# ─────────────────────────────────────────────

def banner(text):
    ascii_art = pyfiglet.figlet_format(text)
    print(colored(ascii_art, 'green'))

def menu():
    print("\n===== FAKE LOGIN LOGGER =====")
    print("1. Mulai Login Palsu")
    print("2. Lihat Log Login")
    print("3. Keluar")

def main():
    banner("FakeLoginLogger")
    print(colored("Phishing Simulator untuk Edukasi", 'cyan'))

    while True:
        menu()
        choice = input("Pilih menu > ")

        if choice == '1':
            fake_login()

        elif choice == '2':
            # Menampilkan log yang dicatat
            try:
                print(colored("\n===== LOG LOGIN =====", 'cyan'))
                with open("login_log.txt", "r") as log_file:
                    logs = log_file.readlines()
                    if logs:
                        for log in logs:
                            print(colored(log.strip(), 'green'))
                    else:
                        print(colored("[INFO] Tidak ada data login.", 'yellow'))
            except FileNotFoundError:
                print(colored("[INFO] Log belum ada.", 'yellow'))

        elif choice == '3':
            print(colored("Keluar... Hati-hati di dunia maya!", 'red'))
            break
        else:
            print(colored("Pilihan tidak valid, coba lagi.", 'red'))

        input("Tekan Enter untuk kembali ke menu...")

if __name__ == "__main__":
    main()
