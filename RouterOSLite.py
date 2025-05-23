import os
import subprocess
import platform
import socket # Diperlukan untuk konstanta socket.AF_INET dll.

# Import dari Rich
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.padding import Padding
from rich.live import Live # Untuk update dinamis jika diperlukan
from rich.traceback import install as install_rich_traceback

# Library tambahan
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

try:
    import netifaces
    NETIFACES_AVAILABLE = True
except ImportError:
    NETIFACES_AVAILABLE = False

# Inisialisasi console Rich dan traceback handler
console = Console()
install_rich_traceback(console=console, show_locals=True) # Traceback yang lebih baik

# --- Helper Functions ---
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title_text):
    clear_screen()
    console.print(Panel(Text(title_text, justify="center", style="bold white on #1E90FF"), # Biru Dodger
                        title="[bold #FFD700]PyTik CLI[/bold #FFD700]", # Emas
                        subtitle="[italic dim]Inspired by MikroTik OS[/italic dim]",
                        border_style="#FF4500")) # Oranye Merah
    console.print("")

def show_error(message, e=None):
    console.print(f"[bold red]ERROR:[/bold red] {message}")
    if e:
        console.print(f"[dim italic]Details: {str(e)}[/dim]")
    Prompt.ask("[dim]Press Enter to continue...[/dim]")

def show_warning(message):
    console.print(f"[bold yellow]WARNING:[/bold yellow] {message}")

def check_dependencies():
    if not PSUTIL_AVAILABLE:
        show_warning("`psutil` library not found. Some features will be limited or unavailable.")
        console.print("[dim]Install with: pip install psutil[/dim]")
    if not NETIFACES_AVAILABLE:
        show_warning("`netifaces` library not found. IP address features will be limited.")
        console.print("[dim]Install with: pip install netifaces[/dim]")
    console.line()

# --- Interface Menu ---
def get_interface_details_psutil(interface_name):
    """Mendapatkan detail spesifik untuk satu interface menggunakan psutil."""
    if not PSUTIL_AVAILABLE:
        show_warning("psutil library not available for detailed interface info.")
        return None

    try:
        all_addrs = psutil.net_if_addrs()
        all_stats = psutil.net_if_stats()

        if interface_name not in all_addrs or interface_name not in all_stats:
            show_error(f"Interface '{interface_name}' not found.")
            return None

        addrs = all_addrs[interface_name]
        stats = all_stats[interface_name]

        table = Table(title=f"Details for Interface: [bold cyan]{interface_name}[/bold cyan]",
                      show_header=True, header_style="bold magenta", box=None)
        table.add_column("Property", style="dim", width=20)
        table.add_column("Value")

        table.add_row("Status", "[green]UP[/green]" if stats.isup else "[red]DOWN[/red]")
        table.add_row("Speed", f"{stats.speed} Mbps" if stats.speed > 0 else "N/A")
        table.add_row("MTU", str(stats.mtu))
        # table.add_row("Duplex", str(stats.duplex) if hasattr(stats, 'duplex') else "N/A") # psutil.NIC_DUPLEX_FULL / HALF

        for addr in addrs:
            if addr.family == psutil.AF_LINK: # MAC Address
                table.add_row("MAC Address", f"[yellow]{addr.address}[/yellow]")
            elif addr.family == socket.AF_INET: # IPv4
                table.add_row("IPv4 Address", f"[green]{addr.address}[/green]")
                table.add_row("  Netmask", str(addr.netmask))
                if addr.broadcast:
                    table.add_row("  Broadcast", str(addr.broadcast))
            elif addr.family == socket.AF_INET6: # IPv6
                ipv6_addr = addr.address.split('%')[0] # Hapus scope ID jika ada
                table.add_row("IPv6 Address", f"[green]{ipv6_addr}[/green]")
                # Netmask IPv6 biasanya prefix, bisa lebih kompleks untuk ditampilkan sederhana
                # table.add_row("  Netmask (Prefix)", str(addr.netmask))


        # Statistik dasar (jika ada)
        if hasattr(stats, 'bytes_sent'):
            table.add_row("Bytes Sent", f"{stats.bytes_sent:,}")
        if hasattr(stats, 'bytes_recv'):
            table.add_row("Bytes Received", f"{stats.bytes_recv:,}")
        if hasattr(stats, 'packets_sent'):
            table.add_row("Packets Sent", f"{stats.packets_sent:,}")
        if hasattr(stats, 'packets_recv'):
            table.add_row("Packets Received", f"{stats.packets_recv:,}")
        if hasattr(stats, 'errin'):
            table.add_row("Errors In", str(stats.errin))
        if hasattr(stats, 'errout'):
            table.add_row("Errors Out", str(stats.errout))
        if hasattr(stats, 'dropin'):
            table.add_row("Drops In", str(stats.dropin))
        if hasattr(stats, 'dropout'):
            table.add_row("Drops Out", str(stats.dropout))

        return table

    except Exception as e:
        show_error(f"Could not retrieve details for '{interface_name}' using psutil.", e)
        return None

def print_interfaces_rich():
    print_header("Network Interfaces List")
    if not PSUTIL_AVAILABLE:
        show_warning("`psutil` library not found. Displaying basic info using OS commands.")
        try:
            cmd = ['ip', 'addr'] if platform.system() != "Windows" else ['ipconfig']
            result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=10)
            console.print(f"\n[b]Output from '{' '.join(cmd)}':[/b]")
            console.print(Padding(result.stdout, (1, 2)))
        except Exception as e:
            show_error(f"Failed to run OS command for interface list.", e)
        Prompt.ask("[dim]Press Enter to continue...[/dim]")
        return

    table = Table(title="Network Interfaces", show_header=True, header_style="bold #FF8C00", border_style="dim")
    table.add_column("Name", style="cyan", width=15, no_wrap=True)
    table.add_column("Status", justify="center")
    table.add_column("Speed (Mbps)", justify="right")
    table.add_column("MTU", justify="right")
    table.add_column("MAC Address", style="yellow")
    table.add_column("IP Addresses (IPv4/IPv6)", style="green", overflow="fold")

    try:
        stats = psutil.net_if_stats()
        addrs = psutil.net_if_addrs()

        for name, snicstats in stats.items():
            mac_address = "N/A"
            ip_info_list = []

            if name in addrs:
                for snicaddr in addrs[name]:
                    if snicaddr.family == psutil.AF_LINK:
                        mac_address = snicaddr.address
                    elif snicaddr.family == socket.AF_INET:
                        ip_info_list.append(f"IPv4: {snicaddr.address}" + (f"/{snicaddr.netmask}" if snicaddr.netmask else ""))
                    elif snicaddr.family == socket.AF_INET6:
                        ipv6_addr = snicaddr.address.split('%')[0] # Hapus scope
                        ip_info_list.append(f"IPv6: {ipv6_addr}")

            status_text = "[#32CD32]UP[/]" if snicstats.isup else "[#FF6347]DOWN[/]" # Hijau Limau / Merah Tomat
            speed_text = str(snicstats.speed) if snicstats.speed > 0 else "N/A"
            mtu_text = str(snicstats.mtu)
            ip_addresses_str = "\n".join(ip_info_list) if ip_info_list else "N/A"

            table.add_row(name, status_text, speed_text, mtu_text, mac_address, ip_addresses_str)
        console.print(table)
    except Exception as e:
        show_error("Could not retrieve interface list using psutil.", e)

    Prompt.ask("[dim]Press Enter to continue...[/dim]")


def interface_menu():
    while True:
        print_header("Interface Menu")
        menu_options = {
            "print": "Show interface list",
            "detail": "Show detailed info for an interface (e.g., detail eth0)",
            "back": "Return to Main Menu"
        }
        for cmd, desc in menu_options.items():
            console.print(f"  [bold cyan]{cmd:<10}[/bold cyan] - {desc}")
        console.print("-" * 50, style="dim")

        choice_str = Prompt.ask("[Interface]>", default="").strip().lower()
        if not choice_str: continue

        parts = choice_str.split()
        command = parts[0]
        args = parts[1:]

        if command == "print":
            print_interfaces_rich()
        elif command == "detail" and args:
            iface_name = args[0]
            print_header(f"Interface Detail: {iface_name}")
            detail_table = get_interface_details_psutil(iface_name)
            if detail_table:
                console.print(detail_table)
            Prompt.ask("[dim]Press Enter to continue...[/dim]")
        elif command == "back":
            break
        else:
            show_error(f"Unknown command: '{choice_str}'")

# --- IP Menu ---
def print_ip_addresses_rich():
    print_header("IP Address List")
    if not NETIFACES_AVAILABLE:
        show_warning("`netifaces` library not found. Cannot display detailed IP addresses.")
        console.print("[dim]You can try 'interface print' for basic info or OS commands.[/dim]")
        Prompt.ask("[dim]Press Enter to continue...[/dim]")
        return

    table = Table(title="Configured IP Addresses", show_header=True, header_style="bold #FF8C00", border_style="dim")
    table.add_column("Interface", style="cyan", width=15)
    table.add_column("Family", style="blue", width=8)
    table.add_column("Address", style="green")
    table.add_column("Netmask", style="yellow")
    table.add_column("Broadcast/Peer", style="magenta", overflow="fold")

    try:
        for iface_name in netifaces.interfaces():
            addrs = netifaces.ifaddresses(iface_name)
            if netifaces.AF_INET in addrs:
                for link_addr in addrs[netifaces.AF_INET]:
                    table.add_row(
                        iface_name, "IPv4",
                        link_addr.get('addr', 'N/A'),
                        link_addr.get('netmask', 'N/A'),
                        link_addr.get('broadcast', 'N/A')
                    )
            if netifaces.AF_INET6 in addrs:
                for link_addr in addrs[netifaces.AF_INET6]:
                    addr_info = link_addr.get('addr', 'N/A').split('%')[0]
                    table.add_row(
                        iface_name, "IPv6",
                        addr_info,
                        link_addr.get('netmask', 'N/A'), # Seringkali ini adalah prefix
                        "N/A"
                    )
        if not table.rows:
            console.print("[yellow]No IP addresses found or netifaces could not retrieve them.[/yellow]")
        else:
            console.print(table)
    except Exception as e:
        show_error("Could not retrieve IP address list using netifaces.", e)
    Prompt.ask("[dim]Press Enter to continue...[/dim]")


def print_routing_table():
    print_header("Routing Table")
    try:
        if platform.system() == "Windows":
            cmd = ['route', 'print', '-4'] # -4 untuk IPv4, bisa juga '-6' untuk IPv6
        elif platform.system() == "Linux":
            cmd = ['ip', 'route', 'show']
        elif platform.system() == "Darwin": # macOS
            cmd = ['netstat', '-rn']
        else:
            show_error(f"Routing table command not implemented for {platform.system()}.")
            return

        console.print(f"[dim]Executing: {' '.join(cmd)}[/dim]")
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=15)
        output = result.stdout

        # Sederhanakan output untuk Windows 'route print' yang sangat verbose
        if platform.system() == "Windows" and "IPv4 Route Table" in output:
             # Coba cari bagian tabel rute aktif
            active_routes_section = []
            in_active_routes = False
            for line in output.splitlines():
                if "Active Routes:" in line:
                    in_active_routes = True
                    active_routes_section.append("="*20 + " Active IPv4 Routes " + "="*20) # Header untuk bagian ini
                    continue
                if "Persistent Routes:" in line and in_active_routes:
                    break # Stop jika sudah masuk ke persistent routes
                if in_active_routes:
                    active_routes_section.append(line)
            output_to_display = "\n".join(active_routes_section) if active_routes_section else output
        else:
            output_to_display = output


        console.print(Panel(Text(output_to_display, overflow="fold"),
                            title="System Routing Table", border_style="green", expand=False))

    except subprocess.TimeoutExpired:
        show_error(f"Command '{' '.join(cmd)}' timed out.")
    except subprocess.CalledProcessError as e:
        show_error(f"Command '{' '.join(cmd)}' failed.", e)
        if e.stderr: console.print(f"[dim]STDERR:\n{e.stderr}[/dim]")
    except FileNotFoundError:
        show_error(f"Command '{cmd[0]}' not found. Is it installed and in PATH?")
    except Exception as e:
        show_error("An unexpected error occurred while fetching routing table.", e)
    Prompt.ask("[dim]Press Enter to continue...[/dim]")

def print_firewall_rules():
    print_header("Firewall Rules (Basic View)")
    cmd_info = None
    try:
        if platform.system() == "Linux":
            # Coba nftables dulu, lalu iptables
            try:
                subprocess.run(['nft', '--version'], capture_output=True, check=True, timeout=5)
                cmd = ['sudo', 'nft', 'list', 'ruleset']
                cmd_info = "nftables"
            except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
                try:
                    subprocess.run(['iptables', '--version'], capture_output=True, check=True, timeout=5)
                    cmd = ['sudo', 'iptables', '-L', '-n', '-v']
                    cmd_info = "iptables"
                except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
                    show_error("Neither nftables nor iptables found or accessible on Linux.")
                    return
        elif platform.system() == "Windows":
            cmd = ['netsh', 'advfirewall', 'firewall', 'show', 'rule', 'name=all', 'dir=in', 'status=enabled'] # Contoh: aturan masuk yang aktif
            cmd_info = "Windows Defender Firewall (Incoming Enabled)"
            # Untuk semua: netsh advfirewall firewall show rule name=all
        elif platform.system() == "Darwin": # macOS
            cmd = ['sudo', 'pfctl', '-sr'] # Show all current rules
            cmd_info = "PF (Packet Filter)"
        else:
            show_error(f"Firewall display not implemented for {platform.system()}.")
            return

        console.print(f"[dim]Attempting to display {cmd_info} rules using: {' '.join(cmd)}[/dim]")
        console.print("[yellow]Note: This may require administrator/sudo privileges.[/yellow]")

        # Untuk sudo, kita mungkin perlu cara lain jika skrip tidak dijalankan sebagai root
        # Untuk saat ini, kita asumsikan pengguna akan menjalankan skrip dengan sudo jika diperlukan
        # atau perintah sudo tidak memerlukan password (misalnya, via /etc/sudoers).

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)

        if result.returncode != 0 and "sudo" in cmd[0]:
            console.print(f"[yellow]Command '{' '.join(cmd)}' may have failed due to sudo permissions or other issues.[/yellow]")
            console.print(f"[dim]Return code: {result.returncode}[/dim]")
            if result.stderr:
                console.print(f"[dim]STDERR:\n{result.stderr}[/dim]")
            if result.stdout: # Tampilkan stdout juga jika ada meski error
                 console.print(f"[dim]STDOUT:\n{result.stdout}[/dim]")

        elif result.returncode == 0:
            console.print(Panel(Text(result.stdout, overflow="fold"),
                                title=f"{cmd_info} Rules", border_style="blue", expand=False))
        else: # Error non-sudo
            show_error(f"Command '{' '.join(cmd)}' failed.", result.stderr if result.stderr else result.stdout)


    except subprocess.TimeoutExpired:
        show_error(f"Command to display firewall rules timed out.")
    except FileNotFoundError:
        show_error(f"Firewall command '{cmd[0] if 'cmd' in locals() else 'utility'}' not found.")
    except Exception as e:
        show_error("An unexpected error occurred while fetching firewall rules.", e)
    Prompt.ask("[dim]Press Enter to continue...[/dim]")

def ip_menu():
    while True:
        print_header("IP Configuration Menu")
        menu_options = {
            "address print": "Show configured IP addresses",
            "route print": "Show IP routing table",
            "firewall print": "Show firewall rules (basic)",
            "back": "Return to Main Menu"
        }
        for cmd, desc in menu_options.items():
            console.print(f"  [bold cyan]{cmd:<18}[/bold cyan] - {desc}")
        console.print("-" * 50, style="dim")

        choice_str = Prompt.ask("[IP]>", default="").strip().lower()
        if not choice_str: continue

        if choice_str == "address print":
            print_ip_addresses_rich()
        elif choice_str == "route print":
            print_routing_table()
        elif choice_str == "firewall print":
            print_firewall_rules()
        elif choice_str == "back":
            break
        else:
            show_error(f"Unknown command: '{choice_str}'")

# --- Tools Menu ---
def tool_ping(host):
    print_header(f"Pinging {host}")
    if not host:
        show_error("No host specified for ping.")
        return

    count_param = '-n' if platform.system() == "Windows" else '-c'
    ping_cmd = ['ping', count_param, '4', host] # 4 pings

    console.print(f"[dim]Executing: {' '.join(ping_cmd)}[/dim]")
    output_buffer = []

    try:
        # Menggunakan Popen untuk streaming output jika diinginkan, atau Live display
        process = subprocess.Popen(ping_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, universal_newlines=True)

        with Live(console=console, refresh_per_second=4, transient=True) as live:
            live.update(Text("Pinging..."))
            for line in process.stdout:
                output_buffer.append(line.strip())
                # Update live display dengan beberapa baris terakhir atau ringkasan
                # Untuk ping, mungkin lebih baik menampilkan semua output di akhir
                live.update(Panel("\n".join(output_buffer[-10:]), title=f"Pinging {host}...", border_style="yellow")) # Tampilkan 10 baris terakhir

        process.wait(timeout=15) # Tunggu proses selesai, dengan timeout
        full_output = "\n".join(output_buffer)

        if process.returncode == 0:
            console.print(Panel(Text(full_output), title=f"[#32CD32]Ping Successful: {host}[/]", border_style="#32CD32", expand=False))
        else:
            console.print(Panel(Text(full_output), title=f"[#FF6347]Ping Failed/Partial: {host}[/]", border_style="#FF6347", expand=False))

    except subprocess.TimeoutExpired:
        process.kill() # Pastikan proses dihentikan
        full_output = "\n".join(output_buffer) + "\n\n--- PING TIMED OUT ---"
        console.print(Panel(Text(full_output), title=f"[#FF6347]Ping Timed Out: {host}[/]", border_style="#FF6347", expand=False))
    except FileNotFoundError:
        show_error(f"Command 'ping' not found. Is it installed and in PATH?")
    except Exception as e:
        show_error(f"An error occurred during ping to {host}.", e)
    Prompt.ask("[dim]Press Enter to continue...[/dim]")

def tool_traceroute(host):
    print_header(f"Traceroute to {host}")
    if not host:
        show_error("No host specified for traceroute.")
        return

    if platform.system() == "Windows":
        trace_cmd = ['tracert', '-d', host] # -d untuk tidak resolve hostname
    elif platform.system() == "Linux":
        trace_cmd = ['traceroute', '-n', host] # -n untuk tidak resolve hostname
    elif platform.system() == "Darwin": # macOS
        trace_cmd = ['traceroute', '-n', host]
    else:
        show_error(f"Traceroute command not implemented for {platform.system()}.")
        return

    console.print(f"[dim]Executing: {' '.join(trace_cmd)}[/dim]")
    output_buffer = []

    try:
        process = subprocess.Popen(trace_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, universal_newlines=True)
        with Live(console=console, refresh_per_second=2, transient=True) as live:
            live.update(Text(f"Tracing route to {host}..."))
            for i, line in enumerate(process.stdout):
                line_strip = line.strip()
                if not line_strip: continue # Abaikan baris kosong
                output_buffer.append(line_strip)
                # Membuat tampilan yang lebih sederhana untuk live update
                # karena traceroute outputnya banyak
                if i < 5: # Tampilkan beberapa baris awal saat proses
                    live.update(Panel("\n".join(output_buffer), title=f"Tracing to {host}...", border_style="yellow"))
                elif i % 5 == 0 : # Update setiap 5 baris setelah itu
                    live.update(Panel("...\n" + "\n".join(output_buffer[-5:]), title=f"Tracing to {host}...", border_style="yellow"))


        process.wait(timeout=120) # Traceroute bisa lama
        full_output = "\n".join(output_buffer)

        if process.returncode == 0:
             console.print(Panel(Text(full_output), title=f"[#32CD32]Traceroute Complete: {host}[/]", border_style="#32CD32", expand=False))
        else:
            console.print(Panel(Text(full_output), title=f"[#FF6347]Traceroute อาจมีปัญหา: {host}[/]", border_style="#FF6347", expand=False))

    except subprocess.TimeoutExpired:
        process.kill()
        full_output = "\n".join(output_buffer) + f"\n\n--- TRACEROUTE TO {host} TIMED OUT ---"
        console.print(Panel(Text(full_output), title=f"[#FF6347]Traceroute Timed Out: {host}[/]", border_style="#FF6347", expand=False))

    except FileNotFoundError:
        show_error(f"Command '{trace_cmd[0]}' not found. Is it installed and in PATH?")
    except Exception as e:
        show_error(f"An error occurred during traceroute to {host}.", e)
    Prompt.ask("[dim]Press Enter to continue...[/dim]")


def tools_menu():
    while True:
        print_header("Network Tools Menu")
        menu_options = {
            "ping": "Send ICMP ECHO_REQUEST to a host (e.g., ping google.com)",
            "trace": "Trace route to a host (e.g., trace google.com)",
            "back": "Return to Main Menu"
        }
        for cmd, desc in menu_options.items():
            console.print(f"  [bold cyan]{cmd:<10}[/bold cyan] - {desc}")
        console.print("-" * 50, style="dim")

        choice_str = Prompt.ask("[Tools]>", default="").strip().lower()
        if not choice_str: continue

        parts = choice_str.split()
        command = parts[0]
        args = parts[1:]

        if command == "ping":
            host = args[0] if args else Prompt.ask("Enter host to ping")
            if host: tool_ping(host)
        elif command == "trace": # Dulu 'traceroute', disingkat jadi 'trace'
            host = args[0] if args else Prompt.ask("Enter host to traceroute")
            if host: tool_traceroute(host)
        elif command == "back":
            break
        else:
            show_error(f"Unknown command: '{choice_str}'")

# --- Main Loop ---
def main_loop():
    check_dependencies() # Cek dependensi di awal
    Prompt.ask("[dim]Press Enter to start PyTik CLI...[/dim]")

    while True:
        print_header("Main Menu")
        menu_options = {
            "1": "Interface Management",
            "2": "IP Configuration",
            "3": "Network Tools",
            "Q": "Quit PyTik CLI"
        }
        # Menggunakan tabel untuk tampilan menu utama yang lebih rapi
        menu_table = Table(box=None, show_header=False)
        menu_table.add_column("Key", style="bold #FFD700", width=5) # Emas
        menu_table.add_column("Option")

        for key, value in menu_options.items():
            menu_table.add_row(f"[{key}]", value)
        console.print(menu_table)
        console.print("-" * 50, style="dim")

        pilihan = Prompt.ask("Select an option", choices=list(menu_options.keys()) + [k.lower() for k in menu_options.keys()], default="Q").upper()

        if pilihan == '1':
            interface_menu()
        elif pilihan == '2':
            ip_menu()
        elif pilihan == '3':
            tools_menu()
        elif pilihan == 'Q':
            if Confirm.ask("[bold #FF6347]Are you sure you want to quit PyTik CLI?[/]"): # Merah Tomat
                console.print(Panel("[bold #32CD32]Exiting PyTik CLI. Goodbye![/]", expand=False, border_style="#32CD32")) # Hijau Limau
                break
        else: # Seharusnya tidak terjadi jika menggunakan choices di Prompt.ask
            show_error("Invalid option selected.")

if __name__ == "__main__":
    main_loop()
