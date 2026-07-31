from rich.console import Console

console = Console()

VERSION = "1.0.0"

def show_banner():
    console.print(r"""[bold cyan]
 _   _           _     ____  _     _      _     _ 
| | | | __ _ ___| |__ / ___|| |__ (_) ___| | __| |
| |_| |/ _` / __| '_ \\___ \| '_ \| |/ _ \ |/ _` |
|  _  | (_| \__ \ | | |___) | | | | |  __/ | (_| |
|_| |_|\__,_|___/_| |_|____/|_| |_|_|\___|_|\__,_|
[/bold cyan]""")
    console.print(f"[bold green]HashShield v{VERSION}[/bold green]")
    console.print("[yellow]Identify • Crack • Generate[/yellow]")
    console.print("[dim]Developed by Youssef Mediouni[/dim]\n")
