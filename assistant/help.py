def assistant_help():
    return [
        {
            "command": "add-contact",
            "arguments": "<name> <phone>",
            "description": "Adds a new contact with the specified name and phone number."
        },
        {
            "command": "edit-phone",
            "arguments": "<id> <phone>",
            "description": "Updates the phone number for the contact with the specified ID."
        },
        {
            "command": "edit-birthday",
            "arguments": "<id> <birthday>",
            "description": "Updates the birthday for the contact with the specified ID. Use the format YYYY-MM-DD."
        },
        {
            "command": "edit-email",
            "arguments": "<id> <email>",
            "description": "Updates the email address for the contact with the specified ID."
        },
        {
            "command": "edit-address",
            "arguments": "<id> <address>",
            "description": "Updates the physical address for the contact with the specified ID."
        },
        {
            "command": "delete-contact",
            "arguments": "<id>",
            "description": "Removes the contact with the specified ID from your address book."
        },
        {
            "command": "find-contacts",
            "arguments": "<some-value>",
            "description": "Searches for contacts that match the given value in any of their details."
        },
        {
            "command": "show-contacts",
            "arguments": "",
            "description": "Displays all the contacts in your address book."
        },
        {
            "command": "show-birthdays",
            "arguments": "<days-count-from-today>",
            "description": "Shows the contacts having birthdays within the specified number of days from today."
        },
        {
            "command": "add-note",
            "arguments": "<note>",
            "description": "Creates a new note with the provided text content."
        },
        {
            "command": "edit-note",
            "arguments": "<id>",
            "description": "Edits the note corresponding to the given ID."
        },
        {
            "command": "find-notes",
            "arguments": "<keyword>",
            "description": "Finds notes containing the specified keyword."
        },
        {
            "command": "delete-note",
            "arguments": "<id>",
            "description": "Deletes the note with the specified ID."
        },
        {
            "command": "show-notes",
            "arguments": "<id>",
            "description": "Displays the content of the note with the specified ID."
        }
    ]

def get_command_list():
    commands = [command["command"] for command in assistant_help()]
    additional_commands = ['close', 'exit', 'help']
    commands.extend(additional_commands)
    return commands