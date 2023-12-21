from contacts import ContactsBook
from notes import NotesManager
from help import assistant_help
from error_handler import input_error_handler, error_handler


class Assistant:
    WELCOME_MESSAGE = (
        "Welcome to the Assistant!\n"
        "I am ready to help you manage your contacts and notes.\n"
        "Type 'help' to see a list of available commands, 'exit' or 'close' to finish the session.\n"
        "How can I assist you today?"
    )

    def __init__(self, contacts: ContactsBook, notes: NotesManager):
        self.contacts = contacts
        self.notes = notes

    @input_error_handler
    def parse_input(self, user_input):
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
        return cmd, *args

    @error_handler
    def add_contact(self, args):
        name, phone_number = args
        return self.contacts.add_contact(name, phone_number)

    @error_handler
    def edit_phone(self, args):
        id, phone_number = args
        return self.contacts.edit_phone(id, phone_number)

    @error_handler
    def add_note(self, args):
        content = " ".join(args)
        return self.notes.add_note(content)

    @error_handler
    def find_notes(self, args):
        keyword = " ".join(args)
        result = self.notes.find_notes(keyword)
        return f"Search result: {result}"


def run():
    print(Assistant.WELCOME_MESSAGE)
    with ContactsBook() as contacts, NotesManager() as notes:
        assistant = Assistant(contacts, notes)
        while True:
            user_input = input("Enter a command, please: ")
            command, *args = assistant.parse_input(user_input)

            if command in ["exit", "close"]:
                print("Goodbye, have a nice day!")
                break
            # elif: add other commands and according functions
            elif command == "help":
                assistant_help()
            elif command == "add-contact":
                print(assistant.add_contact(args))
            elif command == "add-note":
                print(assistant.add_note(args))
            elif command == "edit-phone":
                print(assistant.edit_phone(args))
            elif command == "find-notes":
                print(assistant.find_notes(args))
            else:
                print("Please, provide a correct command.")


if __name__ == "__main__":
    run()
