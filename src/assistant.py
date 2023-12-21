from contacts_book import ContactsBook
from notes_manager import NotesManager
from assistant_help import assistant_help


class Assistant:
    WELCOME_MESSAGE = (
        "Welcome to the Console Assistant!\n"
        "I am ready to help you manage your contacts and notes.\n"
        "Type 'help' to see a list of available commands, 'exit' or 'close' to finish the session.\n"
        "How can I assist you today?"
    )

    def __init__(self, contacts: ContactsBook, notes: NotesManager):
        self.contacts = contacts
        self.notes = notes

    def _parse_input(self, user_input):
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
        return cmd, *args

    def add_contact(self, args):
        name, phone_number = args
        return self.contacts.add_contact(name, phone_number)

    def add_note(self, args):
        content = " ".join(args)
        return self.notes.add_note(content)

    def find_notes(self, args):
        keyword = " ".join(args)
        result = self.notes.find_notes(keyword)
        return f"Search result: {result}"
    
    def show_birthdays(self, args):
        until_date = args
        return self.contacts_book.show_birthdays(until_date)

    def run(self):
        print(self.WELCOME_MESSAGE)

        while True:
            user_input = input("Enter a command, please: ")
            command, *args = self._parse_input(user_input)

            if command in ["exit", "close"]:
                print("Goodbye, have a nice day!")
                break
            # elif: add other commands and according functions
            elif command == "help":
                assistant_help()
            elif command == "add-contact":
                print(self.add_contact(args))
            elif command == "add-note":
                print(self.add_note(args))
            elif command == "find-notes":
                print(self.find_notes(args))
            else:
                print("Please, provide a correct command.")


if __name__ == "__main__":
    pass
