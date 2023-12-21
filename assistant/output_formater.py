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
        if isinstance(error, str):
            self.console.print(f"[bold red]{error}[/bold red]")

    def print_table(self, data):
        if isinstance(data, list):
            column_colors = ["cyan", "magenta", "yellow"]
            header_color = "bold magenta"

            table = Table(show_header=True, header_style=header_color)

            headers = list(data[0].keys())

            for header, color in zip(headers, column_colors):
                table.add_column(header.capitalize(), style=color)

            for item in data:
                table.add_row(*[item.get(header, "") for header in headers])

            self.console.print(table)
