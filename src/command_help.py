from rich.console import Console
from rich.table import Table


def command_help():
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")

    table.add_column("Command", style="bold cyan", width=30)
    table.add_column("Arguments", style="magenta", width=20)
    table.add_column("Description", style="yellow", width=60)

    greeting = "Welcome to your Personal Assistant! Here are the available commands:"

    commands = {
        "add_contact": {"args": "", "desc": "Add a new contact with name, address, phone number, email, and birthday."},
        "search_contacts": {"args": "<criteria>", "desc": "Search for contacts by specified criteria (e.g., name)."},
        "edit_contact": {"args": "<contact_id>", "desc": "Edit an existing contact."},
        "delete_contact": {"args": "<contact_id>", "desc": "Delete a contact."},
        "add_note": {"args": "<contact_id> <text>", "desc": "Add a new text note."},
        "search_notes": {"args": "<criteria>", "desc": "Search for notes by specified criteria."},
        "edit_note": {"args": "<contact_id>", "desc": "Edit an existing note."},
        "delete_note": {"args": "<contact_id>", "desc": "Delete a note."},
        "add_tags": {"args": "<contact_id> <tags>", "desc": "Add tags to a note."},
        "search_notes_by_tags": {"args": "<tag>", "desc": "Search and sort notes by tags."},
        "upcoming_birthdays": {"args": "<days>",
                               "desc": "Show contacts with birthdays in the specified number of days."}
    }

    for command, info in commands.items():
        table.add_row(command, info["args"], info["desc"])

    console.print(greeting)
    console.print(table)
