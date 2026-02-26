import typer
from rich.console import Console
from .bot import GmailBot

app = typer.Typer(help="Gmail Account Creator Bot")
console = Console()

@app.command()
def create(count: int = 1):
    """Start creating Gmail accounts."""
    console.print(f"[bold green]Starting Gmail Bot... Target: {count} accounts[/bold green]")
    bot = GmailBot()
    try:
        for i in range(count):
            console.print(f"Creating account {i+1}/{count}...")
            # Note: Full automation often requires SMS bypass which is out of scope for a basic script
            # This will open the browser and navigate to the signup page.
            bot.start_signup()
            console.print("[yellow]Please complete any manual verification steps (like SMS) if prompted.[/yellow]")
    finally:
        bot.quit()

if __name__ == "__main__":
    app()
