#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

import argparse
from rich.console import Console
from rich.table import Table
from rich import box

from banner import show_banner, VERSION
from identifier import identify, get_strength
from cracker import wordlist_attack, brute_force_attack
from generator import generate, supported_types

console = Console()

# ─── Argument Parser ──────────────────────────────────────────
parser = argparse.ArgumentParser(
    prog="hashshield",
    description="HashShield — Hash Identifier, Cracker & Generator",
    epilog="Example: hashshield --identify 5f4dcc3b5aa765d61d8327deb882cf99"
)

parser.add_argument("-v", "--version", action="version", version=f"HashShield v{VERSION}")

subparsers = parser.add_subparsers(dest="command")

# identify
id_parser = subparsers.add_parser("identify", help="Identify hash type")
id_parser.add_argument("hash", help="Hash string to identify")

# crack
crack_parser = subparsers.add_parser("crack", help="Crack a hash")
crack_parser.add_argument("hash", help="Hash to crack")
crack_parser.add_argument("-w", "--wordlist", help="Path to wordlist file")
crack_parser.add_argument("-b", "--brute", action="store_true", help="Use brute force")
crack_parser.add_argument("--max", type=int, default=4, help="Max brute force length (default: 4)")
crack_parser.add_argument("-t", "--type", help="Force hash type (e.g. md5, sha1)")

# generate
gen_parser = subparsers.add_parser("generate", help="Generate hash from text")
gen_parser.add_argument("text", help="Text to hash")
gen_parser.add_argument("-t", "--type", default="md5", help=f"Hash type ({', '.join(supported_types())})")

args = parser.parse_args()

# ─── Banner ───────────────────────────────────────────────────
show_banner()

# ─── No command ───────────────────────────────────────────────
if not args.command:
    parser.print_help()
    exit(0)

# ═══════════════════════════════════════════════════════════════
#  IDENTIFY
# ═══════════════════════════════════════════════════════════════
if args.command == "identify":
    results = identify(args.hash)

    table = Table(
        title="🔍 Hash Identification",
        box=box.DOUBLE_EDGE,
        style="cyan",
        title_style="bold cyan",
        header_style="bold magenta",
        show_lines=True
    )
    table.add_column("Type", style="bold white", width=15)
    table.add_column("Length", width=8)
    table.add_column("Strength", width=15)
    table.add_column("Crackable", width=12)

    for r in results:
        strength = get_strength(r["name"])
        crackable = "Yes ✅" if r["crackable"] else "No ❌"
        table.add_row(r["name"], str(r["length"]), strength, crackable)

    console.print(table)

# ═══════════════════════════════════════════════════════════════
#  CRACK
# ═══════════════════════════════════════════════════════════════
elif args.command == "crack":

    # Identify hash type
    if args.type:
        hashlib_name = args.type.lower()
        hash_name = args.type.upper()
    else:
        results = identify(args.hash)
        if not results or results[0]["name"] == "Unknown":
            console.print("[red]❌ Could not identify hash type. Use -t to force type.[/red]")
            exit(1)

        # Pick first crackable
        crackable = [r for r in results if r["crackable"] and r["hashlib"]]
        if not crackable:
            console.print("[red]❌ Hash type is not crackable (e.g. bcrypt needs special tools).[/red]")
            exit(1)

        best = crackable[0]
        hashlib_name = best["hashlib"]
        hash_name = best["name"]

    console.print(f"[cyan]Hash Type : [bold]{hash_name}[/bold][/cyan]")
    console.print(f"[cyan]Hash      : [bold]{args.hash}[/bold][/cyan]\n")

    result = None

    if args.wordlist:
        console.print(f"[yellow]⚔️  Wordlist attack: {args.wordlist}[/yellow]")
        result = wordlist_attack(args.hash, hashlib_name, args.wordlist)

    elif args.brute:
        console.print(f"[yellow]⚔️  Brute force attack (max length: {args.max})[/yellow]")
        result = brute_force_attack(args.hash, hashlib_name, max_length=args.max)

    else:
        console.print("[red]❌ Specify -w <wordlist> or -b for brute force[/red]")
        exit(1)

    if result:
        table = Table(
            title="🔓 Hash Cracked!",
            box=box.DOUBLE_EDGE,
            style="green",
            title_style="bold green",
            show_lines=True
        )
        table.add_column("Property", style="bold white", width=15)
        table.add_column("Value", style="green", width=30)
        table.add_row("Hash", args.hash)
        table.add_row("Password", f"[bold red]{result['password']}[/bold red]")
        table.add_row("Attempts", str(result["tried"]))
        table.add_row("Time", f"{result['time']}s")
        console.print()
        console.print(table)
    else:
        console.print("\n[red]❌ Hash could not be cracked.[/red]")

# ═══════════════════════════════════════════════════════════════
#  GENERATE
# ═══════════════════════════════════════════════════════════════
elif args.command == "generate":
    result = generate(args.text, args.type)

    if not result:
        console.print(f"[red]❌ Unsupported type. Choose: {', '.join(supported_types())}[/red]")
        exit(1)

    table = Table(
        title="⚙️  Hash Generated",
        box=box.DOUBLE_EDGE,
        style="cyan",
        title_style="bold cyan",
        show_lines=True
    )
    table.add_column("Property", style="bold white", width=12)
    table.add_column("Value", style="green", width=70)
    table.add_row("Text", args.text)
    table.add_row("Type", args.type.upper())
    table.add_row("Hash", result)
    console.print(table)
