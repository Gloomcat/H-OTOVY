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

    def __init__(self):
        self.contacts = ContactsBook()
        self.notes = NotesManager()

    def _parse_input(self, user_input):
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
        return cmd, *args

    def run(self):
        print(self.WELCOME_MESSAGE)

        while True:
            user_input = input("Enter a command, please: ")
            command, *args = self._parse_input(user_input)

            if command in ["exit", "close"]:
                print("Goodbye, have a nice day :)")
                break
            # elif: add other commands and according functions
            elif command == "help":
                assistant_help()
            else:
                print("Please, provide a correct command.")


if __name__ == "__main__":
    assistant_help()
