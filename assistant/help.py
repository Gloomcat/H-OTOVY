def assistant_help():
    """
    Provides a list of available commands and their descriptions for an assistant application.

    This function returns a list of dictionaries, each containing a command, its expected arguments, and a brief description of what the command does.

    Returns:
        list: A list of dictionaries, each representing a command and its details.
    """
    return [
        {
            "command": "add-contact",
            "arguments": "",
            "description": "Runs user dialog in order to add a new contact.",
        },
        {
            "command": "edit-name",
            "arguments": "<id> <name>",
            "description": "Updates the name for the contact with the specified ID.\nName must be different from stored ones.",
        },
        {
            "command": "edit-phone",
            "arguments": "<id> <phone>",
            "description": "Updates the phone number for the contact with the specified ID.\nPhone must be different from stored ones.",
        },
        {
            "command": "edit-birthday",
            "arguments": "<id> <birthday>",
            "description": "Updates the birthday for the contact with the specified ID.\nUse the format DD.MM.YYYY.",
        },
        {
            "command": "edit-email",
            "arguments": "<id> <email>",
            "description": "Updates the email address for the contact with the specified ID.\nEmail must be different from stored ones.",
        },
        {
            "command": "edit-address",
            "arguments": "<id>",
            "description": "Runs user dialog to update the physical address for the contact with the specified ID.",
        },
        {
            "command": "delete-contact",
            "arguments": "<id>",
            "description": "Removes the contact with the specified ID from your address book.",
        },
        {
            "command": "find-contacts",
            "arguments": "<criteria> <some-value>",
            "description": "Finds and retrieves contacts based on the provided criteria and value.\nCriteria acceptable values: 'id', 'name', 'phone', 'email', 'birthday', 'address'.",
        },
        {
            "command": "show-contacts",
            "arguments": "",
            "description": "Displays all the contacts in your address book.",
        },
        {
            "command": "show-birthdays",
            "arguments": "<days-count-from-today>",
            "description": "Shows the contacts having birthdays within the specified number of days from today inclusive.",
        },
        {
            "command": "add-note",
            "arguments": "<note>",
            "description": "Creates a new note with the provided text content.",
        },
        {
            "command": "edit-note",
            "arguments": "<id>",
            "description": "Edits the note corresponding to the given ID.",
        },
        {
            "command": "find-notes",
            "arguments": "<keyword>",
            "description": "Finds notes containing the specified keyword.",
        },
        {
            "command": "delete-note",
            "arguments": "<id>",
            "description": "Deletes the note with the specified ID.",
        },
        {
            "command": "show-notes",
            "arguments": "",
            "description": "Displays all the notes in your notebook.",
        },
        {
            "command": "add-note-tag",
            "arguments": "<id> <tag>",
            "description": "Add tag to the note with the specified ID.",
        },
        {
            "command": "delete-note-tag",
            "arguments": "<id> <tag>",
            "description": "Delete tag from the note with the specified ID.",
        },
        {
            "command": "edit-note-tag",
            "arguments": "<id> <tag> <new-tag>",
            "description": "Replace tag by new one in the note with the specified ID.",
        },
        {
            "command": "find-notes-by-tag",
            "arguments": "<tag>",
            "description": "Find notes by the Tag specified.",
        },
    ]


def get_command_list():
    commands = [command["command"] for command in assistant_help()]
    additional_commands = ["close", "exit", "help"]
    commands.extend(additional_commands)
    return commands
