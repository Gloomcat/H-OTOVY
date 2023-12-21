from rich.console import Console
from rich.table import Table


def assistant_help():
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")

    table.add_column("Command", style="bold cyan", width=30)
    table.add_column("Arguments", style="magenta", width=25)
    table.add_column("Description", style="yellow", width=60)

    commands = {
        "add-contact": {
            "args": "<name> <phone>",
            "desc": "Adds a new contact with the specified name and phone number."
        },
        "edit-phone": {
            "args": "<id> <phone>",
            "desc": "Updates the phone number for the contact with the specified ID."
        },
        "edit-birthday": {
            "args": "<id> <birthday>",
            "desc": "Updates the birthday for the contact with the specified ID. Use the format DD.MM.YYYY."
        },
        "edit-email": {
            "args": "<id> <email>",
            "desc": "Updates the email address for the contact with the specified ID."
        },
        "edit-address": {
            "args": "<id> <address>",
            "desc": "Updates the physical address for the contact with the specified ID."
        },
        "delete-contact": {
            "args": "<id>",
            "desc": "Removes the contact with the specified ID from your address book."
        },
        "find-contacts": {
            "args": "<some-value>",
            "desc": "Searches for contacts that match the given value in any of their details."
        },
        "show-contacts": {
            "args": "",
            "desc": "Displays all the contacts in your address book."
        },
        "show-birthdays": {
            "args": "<days-count-from-today>",
            "desc": "Shows the contacts having birthdays within the specified number of days from today."
        },
        "add-note": {
            "args": "<note>",
            "desc": "Creates a new note with the provided text content."
        },
        "edit-note": {
            "args": "<id>",
            "desc": "Edits the note corresponding to the given ID."
        },
        "find-notes": {
            "args": "<keyword>",
            "desc": "Finds notes containing the specified keyword."
        },
        "delete-note": {
            "args": "<id>",
            "desc": "Deletes the note with the specified ID."
        },
        "show-notes": {
            "args": "<id>",
            "desc": "Displays the content of the note with the specified ID."
        }
    }

    for command, info in commands.items():
        table.add_row(command, info["args"], info["desc"])

    console.print(table)
