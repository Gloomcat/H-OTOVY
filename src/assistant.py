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

    def add_note(self, args):
        content = " ".join(args)
        return self.notes_manager.add_note(content)

    def run(self):
        while True:
            user_input = input("Enter a command, please: ")
            command, *args = self._parse_input(user_input)

            if command in ["exit", "close"]:
                print("Goodbye, have a nice day :)")
                break
            # elif: add other commands and according functions
            elif command == "add-note":
                print(self.add_note(args))
            else:
                print("Please, provide a correct command.")


if __name__ == "__main__":
    pass
