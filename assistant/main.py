from contacts import ContactsBook
from notes import NotesManager
from help import assistant_help, get_command_list
from error_handler import input_error_handler, error_handler
from output_formater import OutputFormatter
from autocomplete import AutoCompleter


class Assistant:
    WELCOME_MESSAGE = (
        "Welcome to the Assistant!\n"
        "I am ready to help you manage your contacts and notes.\n"
        "Type 'help' to see a list of available commands, 'exit' or 'close' to finish the session.\n"
        "How can I assist you today?"
    )
    FAREWELL_MESSAGE = "Goodbye, have a nice day!"

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
        return result


def run():
    auto_completer = AutoCompleter(get_command_list())
    formatter = OutputFormatter()
    formatter.print_greeting(Assistant.WELCOME_MESSAGE)

    with ContactsBook() as contacts, NotesManager() as notes:
        assistant = Assistant(contacts, notes)

        while True:
            formatter.print_input("Enter a command, please: ")
            user_input = auto_completer.get_user_input()
            command, *args = assistant.parse_input(user_input)

            if command in ["exit", "close"]:
                formatter.print_greeting(Assistant.FAREWELL_MESSAGE)
                break
            elif command == "help":
                formatter.print_table(assistant_help())
            elif command == "add-contact":
                formatter.print_info(assistant.add_contact(args))
            elif command == "add-note":
                formatter.print_info(assistant.add_note(args))
            elif command == "edit-phone":
                formatter.print_info(assistant.edit_phone(args))
            elif command == "find-notes":
                formatter.print_table(assistant.find_notes(args))
            else:
                formatter.print_error("Please, provide a correct command.")


if __name__ == "__main__":
    run()
