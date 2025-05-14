import hashlib
from rich.console import Console
from rich.text import Text
import pyfiglet

# ─────────────────────────────────────────────
# ✅ FUNGSI UNTUK MEMBUAT HASH DARI TEKS
# ─────────────────────────────────────────────

def generate_hash(text, algorithm):
    """
    Fungsi untuk membuat hash dari teks berdasarkan algoritma yang dipilih.
    """
    if algorithm == 'MD5':
        return hashlib.md5(text.encode()).hexdigest()
    elif algorithm == 'SHA1':
        return hashlib.sha1(text.encode()).hexdigest()
    elif algorithm == 'SHA256':
        return hashlib.sha256(text.encode()).hexdigest()
    elif algorithm == 'SHA512':
        return hashlib.sha512(text.encode()).hexdigest()
    else:
        return None

# ─────────────────────────────────────────────
# ✅ TAMPILKAN BANNER
# ─────────────────────────────────────────────

def banner(text, console):
    ascii_art = pyfiglet.figlet_format(text)
    console.print(f"[bold red]{ascii_art}[/bold red]")

# ─────────────────────────────────────────────
# ✅ MENU UTAMA & INTERFACE
# ─────────────────────────────────────────────

def menu():
    print("\n===== HASH GENERATOR =====")
    print("1. Generate Hash")
    print("2. Keluar")

def main():
    console = Console()

    banner("HashX", console)

    while True:
        menu()
        choice = input("Pilih menu > ")

        if choice == '1':
            text = input("[yellow]Masukkan teks untuk di-hash: [/yellow]")

            # Pilih algoritma hash
            print("\nPilih algoritma hash:")
            print("1. MD5")
            print("2. SHA1")
            print("3. SHA256")
            print("4. SHA512")

            algorithm_choice = input("Pilih algoritma (1-4): ")
            if algorithm_choice == '1':
                algorithm = 'MD5'
            elif algorithm_choice == '2':
                algorithm = 'SHA1'
            elif algorithm_choice == '3':
                algorithm = 'SHA256'
            elif algorithm_choice == '4':
                algorithm = 'SHA512'
            else:
                console.print("[red]Pilihan algoritma tidak valid, coba lagi.[/red]", style="bold")
                continue

            # Generate hash
            hash_value = generate_hash(text, algorithm)
            if hash_value:
                console.print(f"\n[bold green]Hash {algorithm} untuk teks yang dimasukkan:[/bold green]")
                console.print(f"[cyan]{hash_value}[/cyan]")
            else:
                console.print("[red]Terjadi kesalahan dalam proses hashing.[/red]", style="bold")

        elif choice == '2':
            console.print("[red]Keluar... Semoga aman! ✌️[/red]", style="bold")
            break
        else:
            console.print("[red]Pilihan tidak valid, coba lagi.[/red]", style="bold")

        input("Tekan Enter untuk kembali ke menu...")

if __name__ == "__main__":
    main()
