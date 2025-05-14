import time
import random
import pyfiglet
from termcolor import colored

# ─────────────────────────────────────────────
# ✅ FAKE CRYPTO PRICE GENERATOR
# ─────────────────────────────────────────────

def get_mock_crypto_price(crypto_name):
    # Fake data untuk harga cryptocurrency
    cryptos = {
        "bitcoin": random.uniform(25000, 60000),  # Harga antara $25k - $60k
        "ethereum": random.uniform(1000, 3500),  # Harga antara $1k - $3.5k
        "dogecoin": random.uniform(0.05, 0.8),   # Harga antara $0.05 - $0.8
        "binancecoin": random.uniform(100, 700),  # Harga antara $100 - $700
        "cardano": random.uniform(0.2, 2.5),     # Harga antara $0.2 - $2.5
        "solana": random.uniform(10, 250),       # Harga antara $10 - $250
    }

    # Mengambil harga berdasarkan nama crypto (mengubah ke lower case)
    crypto_name = crypto_name.lower()

    # Cek jika crypto ada di daftar
    if crypto_name in cryptos:
        return cryptos[crypto_name]
    else:
        return None

# ─────────────────────────────────────────────
# ✅ PRICE TREND ANALYSIS (mock)
# ─────────────────────────────────────────────

def analyze_trend(current_price, previous_price):
    if current_price > previous_price:
        return "Harga naik 🚀"
    elif current_price < previous_price:
        return "Harga turun 📉"
    else:
        return "Harga stabil 🔄"

# ─────────────────────────────────────────────
# ✅ GRAFIK ASCII (untuk vibes)
# ─────────────────────────────────────────────

def display_graph(current_price, previous_price):
    trend = "🚀" if current_price > previous_price else "📉" if current_price < previous_price else "🔄"
    graph = "█" * int(current_price / 1000)  # Buat grafis sederhana
    print(colored(f"Grafik Harga (Harga Sekarang: ${current_price:.2f}):", 'cyan'))
    print(colored(graph + trend, 'yellow'))
    print("-" * 40)

# ─────────────────────────────────────────────
# ✅ MENU UTAMA & INTERFACE
# ─────────────────────────────────────────────

def banner(text):
    ascii_art = pyfiglet.figlet_format(text)
    print(colored(ascii_art, 'green'))

def menu():
    print("\n===== BITTRACKER - Crypto Price Tracker =====")
    print("1. Lihat Harga Cryptocurrency")
    print("2. Exit")

def main():
    banner("BitTracker")
    print(colored("Cryptocurrency Price Tracker - Mock Version", 'cyan'))

    while True:
        menu()
        choice = input("Pilih menu > ")

        if choice == '1':
            crypto_name = input("Masukkan nama cryptocurrency (misal: Bitcoin, Ethereum): ").strip()

            # Mendapatkan harga mock dari koin yang dipilih
            current_price = get_mock_crypto_price(crypto_name)
            if current_price:
                print(colored(f"Harga {crypto_name.capitalize()}: ${current_price:.2f}", 'green'))

                # Menampilkan trend harga (mock)
                previous_price = random.uniform(current_price - 500, current_price + 500)  # Harga sebelumnya (mock)
                trend = analyze_trend(current_price, previous_price)
                print(colored(trend, 'yellow'))

                # Menampilkan grafik harga dengan simbol ASCII
                display_graph(current_price, previous_price)

            else:
                print(colored(f"[!] Cryptocurrency {crypto_name} tidak ditemukan dalam daftar.", 'red'))

        elif choice == '2':
            print("Keluar... Semoga hari mu menguntungkan! 💸")
            break
        else:
            print("Pilihan tidak valid, coba lagi.")

        input("Tekan Enter untuk kembali ke menu...")

if __name__ == "__main__":
    main()
