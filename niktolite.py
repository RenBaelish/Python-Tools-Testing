import httpx
import time
import pyfiglet
from rich.console import Console
from rich.progress import Progress
from rich.text import Text

# ─────────────────────────────────────────────
# ✅ LIST OF COMMON VULNERABILITY ENDPOINTS
# ─────────────────────────────────────────────

common_endpoints = [
    "/admin", "/login", "/panel", "/admin/login", "/config", "/.git", "/.env",
    "/backup", "/uploads", "/test", "/debug", "/server-status", "/wp-login.php", "/wp-admin"
]

# ─────────────────────────────────────────────
# ✅ FUNGSI UNTUK CEK ENDPOINT DENGAN HTTPX
# ─────────────────────────────────────────────

async def check_vulnerability(client, url, endpoint, console):
    target_url = url + endpoint
    try:
        # Kirim permintaan GET menggunakan httpx
        response = await client.get(target_url, timeout=3)

        # Cek status code 200 (OK)
        if response.status_code == 200:
            console.print(f"[green][+] Endpoint ditemukan: {target_url}[/green]")
        else:
            console.print(f"[red][!] Endpoint tidak ditemukan: {target_url} (Status: {response.status_code})[/red]")
    except httpx.RequestError as e:
        console.print(f"[yellow][!] Error saat mengecek {target_url}: {str(e)}[/yellow]")

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
    print("\n===== NIKTO-LIKE SCANNER =====")
    print("1. Cek Website untuk Vulnerability")
    print("2. Keluar")

async def main():
    # Setup console dari Rich
    console = Console()

    # Menampilkan banner
    banner("Nikto-Like", console)
    console.print("[cyan]Web Vulnerability Scanner - Simulasi[/cyan]", style="bold")

    while True:
        menu()
        choice = input("Pilih menu > ")

        if choice == '1':
            url = input("[yellow]Masukkan URL target (misal: https://example.com): [/yellow]")

            # Memulai koneksi HTTP client dengan httpx
            async with httpx.AsyncClient() as client:
                # Progress bar
                with Progress() as progress:
                    task = progress.add_task("[cyan]Memindai endpoint...", total=len(common_endpoints))

                    # Memeriksa setiap endpoint
                    for endpoint in common_endpoints:
                        await check_vulnerability(client, url, endpoint, console)
                        progress.update(task, advance=1)  # Update progress bar
                        time.sleep(0.5)  # Jeda waktu antar request

        elif choice == '2':
            console.print("[red]Keluar... Semoga aman ya! ✌️[/red]", style="bold")
            break
        else:
            console.print("[red]Pilihan tidak valid, coba lagi.[/red]", style="bold")

        input("Tekan Enter untuk kembali ke menu...")

# ─────────────────────────────────────────────
# ✅ Jalankan Program
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
