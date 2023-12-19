from contacts_book import ContactsBook
from notes_manager import NotesManager


class Assistant:
    def __init__(self):
        self.contacts = ContactsBook()
        self.notes = NotesManager()

    def _parse_input(self, user_input):
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
        return cmd, *args

    def add_contact(self, args):
        name, phone_number, email, address, birthday = args
        self.contacts.add_contact(name, phone_number, email, address, birthday)

    def run(self):
        while True:
            user_input = input("Enter a command, please: ")
            command, *args = self._parse_input(user_input)

            if command in ["exit", "close"]:
                print("Goodbye, have a nice day :)")
                break
            # elif: add other commands and according functions
            elif command == "add_contact":
                print(self.add_contact(args))
            else:
                print("Please, provide a correct command.")


if __name__ == "__main__":
    pass
