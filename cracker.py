import hashlib
import itertools
import string
import time
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn

console = Console()

# ═══════════════════════════════════════════════════════════════
#  HASH FUNCTION
# ═══════════════════════════════════════════════════════════════

def compute_hash(word, hashlib_name):
    try:
        h = hashlib.new(hashlib_name)
        h.update(word.encode("utf-8", errors="ignore"))
        return h.hexdigest()
    except Exception:
        return None


# ═══════════════════════════════════════════════════════════════
#  WORDLIST ATTACK
# ═══════════════════════════════════════════════════════════════

def wordlist_attack(hash_str, hashlib_name, wordlist_path):
    """
    Try to crack hash using a wordlist file.
    Returns the cracked password or None.
    """
    hash_str = hash_str.strip().lower()

    try:
        with open(wordlist_path, "r", errors="ignore") as f:
            lines = f.readlines()
    except FileNotFoundError:
        console.print(f"[red]❌ Wordlist not found: {wordlist_path}[/red]")
        return None

    total = len(lines)
    start = time.time()
    tried = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]Cracking..."),
        BarColumn(),
        TextColumn("[green]{task.completed}/{task.total}"),
        TimeElapsedColumn(),
        console=console
    ) as progress:
        task = progress.add_task("wordlist", total=total)

        for line in lines:
            word = line.strip()
            if not word:
                progress.advance(task)
                continue

            candidate = compute_hash(word, hashlib_name)
            tried += 1

            if candidate == hash_str:
                elapsed = round(time.time() - start, 2)
                progress.stop()
                return {
                    "password": word,
                    "tried": tried,
                    "time": elapsed
                }

            progress.advance(task)

    return None


# ═══════════════════════════════════════════════════════════════
#  BRUTE FORCE ATTACK
# ═══════════════════════════════════════════════════════════════

def brute_force_attack(hash_str, hashlib_name, max_length=4, charset=None):
    """
    Try all combinations up to max_length characters.
    Returns the cracked password or None.
    """
    hash_str = hash_str.strip().lower()

    if charset is None:
        charset = string.ascii_lowercase + string.digits

    start = time.time()
    tried = 0

    console.print(f"[cyan]Brute forcing up to {max_length} chars with charset: {charset[:20]}...[/cyan]\n")

    for length in range(1, max_length + 1):
        console.print(f"[dim]Trying length {length}...[/dim]")
        for combo in itertools.product(charset, repeat=length):
            word = "".join(combo)
            candidate = compute_hash(word, hashlib_name)
            tried += 1

            if candidate == hash_str:
                elapsed = round(time.time() - start, 2)
                return {
                    "password": word,
                    "tried": tried,
                    "time": elapsed
                }

    return None
