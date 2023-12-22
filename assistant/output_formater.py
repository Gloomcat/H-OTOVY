from rich.console import Console
from rich.table import Table


class OutputFormatter:
    """
    A class for formatting and displaying output in the console using the 'rich' library.

    This class provides methods to print various types of messages (input prompts, greetings, information, errors) and tables with custom styles.

    Attributes:
        console (Console): An instance of the Console class from the 'rich' library for formatted console output.
    """

    def __init__(self):
        """
        Initializes an OutputFormatter instance with a Console object.
        """
        self.console = Console()

    def print_input(self, text):
        """
        Prints an input prompt in yellow color.

        Parameters:
        text (str): The text to be printed as an input prompt.
        """
        if isinstance(text, str):
            self.console.print(f"[yellow]{text}[/yellow]")

    def print_greeting(self, text):
        """
        Prints a greeting message in bold blue color.

        Parameters:
        text (str): The text to be printed as a greeting message.
        """
        if isinstance(text, str):
            self.console.print(f"[bold cyan]{text}[/bold cyan]")

    def print_info(self, text):
        """
        Prints an informational message in bold green color.

        Parameters:
        text (str): The text to be printed as an informational message.
        """
        if isinstance(text, str):
            self.console.print(f"[bold green]{text}[/bold green]")

    def print_error(self, error):
        """
        Prints an error message in bold red color.

        Parameters:
        error (str): The text to be printed as an error message.
        """
        if isinstance(error, (str, Exception)):
            self.console.print(f"[bold red]{error}[/bold red]")

    def print_table(self, data):
        """
        Prints a table with the provided data.

        Parameters:
        data (list): A list of dictionaries, where each dictionary represents a row in the table.
        """
        if isinstance(data, list):
            column_colors = ["cyan" for _ in range(len(data[0].keys()))]
            header_color = "bold green"

            table = Table(show_header=True, header_style=header_color)

            headers = list(data[0].keys())

            for header, color in zip(headers, column_colors):
                table.add_column(header.capitalize(), style=color)

            for item in data:
                table.add_row(*[str(item.get(header, "")) for header in headers])

            self.console.print(table)
