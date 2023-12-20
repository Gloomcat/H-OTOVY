from rich.console import Console
from rich.table import Table


class OutputFormatter:
    def __init__(self):
        self.console = Console()

    def print_greeting(self, text):
        if isinstance(text, str):
            self.console.print(f"[bold blue]{text}[/bold blue]")

    def print_info(self, text):
        if isinstance(text, str):
            self.console.print(f"[bold green]{text}[/bold green]")

    def print_error(self, error):
        self.console.print(f"[bold red]{error}[/bold red]")

    def print_list(self, arr):
        for item in arr:
            self.console.print(f"[yellow]{item}[/yellow]")

    def print_table(self, headers, data):
        column_colors = ["cyan", "magenta", "yellow"]
        header_color = "bold magenta"
        table = Table(show_header=True, header_style=header_color)

        for (header, width), color in zip(headers.items(), column_colors):
            table.add_column(header, style=color, width=width)

        for row in data:
            table.add_row(*row)

        self.console.print(table)
