def pretty_print_error(error: Exception) -> None:
    """Pretty print errors using rich if available, else fallback to plain text"""
    try:
        from rich.console import Console

        console = Console()
        console.print(f"[bold red]Error:[/bold red] {error}")
    except ImportError:
        print(f"Error: {error}")
