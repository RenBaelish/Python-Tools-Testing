import random
import string
import re
import pyperclip
import time

# ─────────────────────────────────────────────────────────
# ✅ FUNGSI GENERATE PASSWORD
# ─────────────────────────────────────────────────────────

def generate_password(length=12):
    # Semua karakter yang bisa dipakai dalam password
    all_characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(all_characters) for i in range(length))
    return password

# ─────────────────────────────────────────────────────────
# ✅ STRENGTH CHECKER
# ─────────────────────────────────────────────────────────

def check_password_strength(password):
    # Cek panjang password
    if len(password) < 8:
        return "Weak"

    # Cek apakah ada angka
    if not re.search(r"\d", password):
        return "Weak"

    # Cek apakah ada huruf besar
    if not re.search(r"[A-Z]", password):
        return "Medium"

    # Cek apakah ada simbol
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return "Medium"

    # Password strong jika ada huruf kecil, besar, angka, dan simbol
    return "Strong"

# ─────────────────────────────────────────────────────────
# ✅ TAMPILKAN PASSWORD & COPY KE CLIPBOARD
# ─────────────────────────────────────────────────────────

def copy_to_clipboard(password):
    pyperclip.copy(password)
    print(f"Password berhasil disalin ke clipboard: {password}")

def menu():
    print("\n===== PASSGENX: PASSWORD GENERATOR & STRENGTH CHECKER =====")
    print("1. Generate Password")
    print("2. Check Password Strength")
    print("3. Exit")

def main():
    while True:
        menu()
        choice = input("Pilih menu > ")

        if choice == '1':
            length = int(input("Masukkan panjang password (default 12): ") or 12)
            password = generate_password(length)
            print(f"Password yang dihasilkan: {password}")
            copy_option = input("Apakah ingin menyalin ke clipboard? (y/n): ")
            if copy_option.lower() == 'y':
                copy_to_clipboard(password)

        elif choice == '2':
            password = input("Masukkan password untuk cek kekuatan: ")
            strength = check_password_strength(password)
            print(f"Kekuatan password: {strength}")

        elif choice == '3':
            print("Keluar... Tetap aman!")
            break

        else:
            print("Pilihan tidak valid, coba lagi.")

        input("Tekan Enter untuk kembali ke menu...")

if __name__ == "__main__":
    main()
