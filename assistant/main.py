from contacts import ContactsBook
from notes import NotesManager
from help import assistant_help
from error_handler import input_error_handler, error_handler
from datetime import datetime
from output_formater import OutputFormatter


class Assistant:
    """
    A class representing an assistant for managing contacts and notes.

    Attributes:
        WELCOME_MESSAGE (str): A constant string containing the welcome message for the user.
        FAREWELL_MESSAGE (str): A constant string containing the farewell message.
        contacts (ContactsBook): An instance of ContactsBook for managing contact data.
        notes (NotesManager): An instance of NotesManager for managing note data.
    """

    WELCOME_MESSAGE = (
        "Welcome to the Assistant!\n"
        "I am ready to help you manage your contacts and notes.\n"
        "Type 'help' to see a list of available commands, 'exit' or 'close' to finish the session.\n"
        "How can I assist you today?"
    )
    FAREWELL_MESSAGE = "Goodbye, have a nice day!"

    def __init__(self, contacts: ContactsBook, notes: NotesManager):
        """
        Initializes an Assistant instance with contacts and notes management functionality.

        Parameters:
        contacts (ContactsBook): An instance of ContactsBook.
        notes (NotesManager): An instance of NotesManager.
        """
        self.contacts = contacts
        self.notes = notes

    @input_error_handler
    def parse_input(self, user_input):
        """
        Parses the user input into a command and its arguments.

        Parameters:
        user_input (str): The raw string input from the user.

        Returns:
        tuple: A tuple containing the command and its arguments.
        """
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
        return cmd, *args

    @error_handler
    def add_contact(self, args):
        """
        Adds a new contact to the contacts book.

        Parameters:
        args (list): A list containing the name and phone number for the new contact.

        Returns:
        str: A message indicating the success or failure of the operation.
        """
        name, phone_number = args
        answer = input("Would you like to add more info about the contact (Y/n)?:")
        if answer == "Y":
            birthday = input("Birthday:")
            email = input("Email:")
            zipp_code = input("Zipp code:")
            country = input("Country:")
            city = input("City:")
            street = input("Street:")
            building_number = input("Building number:")
            appartment = input("Appartment:")
            address = f"{zipp_code}, {country}, {city}, {street}, {building_number}, {appartment}"
            return self.contacts.add_contact(name, phone_number, email, address, birthday)
        return self.contacts.add_contact(name, phone_number)

    @error_handler
    def edit_phone(self, args):
        """
        Edits the phone number of an existing contact.

        Parameters:
        args (list): A list containing the ID of the contact and the new phone number.

        Returns:
        str: A message indicating the success or failure of the operation.
        """
        id, phone_number = args
        return self.contacts.edit_phone(id, phone_number)
    
    @error_handler
    def edit_email(self, args):
        id, email = args
        return self.contacts.edit_email(int(id), email)

    @error_handler
    def add_note(self, args):
        """
        Adds a new note to the notes manager.

        Parameters:
        args (list): A list containing the content of the note.

        Returns:
        str: A message indicating the success or failure of the operation.
        """
        content = " ".join(args)
        return self.notes.add_note(content)

    @error_handler
    def find_notes(self, args):
        """
        Finds notes containing the specified keyword.

        Parameters:
        args (list): A list containing the keyword to search for.

        Returns:
        list: A list of notes that match the keyword.
        """
        keyword = " ".join(args)
        result = self.notes.find_notes(keyword)
        return f"Search result: {result}"
    
    @error_handler
    def edit_birthday(self, args):
        id, birthday = args
        return self.contacts.edit_birthday(id, birthday)

    @error_handler
    def show_birthdays(self, args):
        number_of_days = args[0]
        return self.contacts.show_birthdays(number_of_days)
    
    @error_handler
    def show_notes(self):
        return self.notes.show_notes()
    
    @error_handler
    def edit_note(self, args):
        id, new_content = int(args[0]), " ".join(args[1:])
        return self.notes.edit_note(id, new_content)
    
    @error_handler
    def delete_note(self, args):
        return self.notes.delete_note(args[0])


def run():
    """
    Runs the assistant application, handling user input and responses.

    This function initializes the Assistant and handles the main loop for user interaction. It processes user commands and displays responses or errors.
    """
    formatter = OutputFormatter()
    formatter.print_greeting(Assistant.WELCOME_MESSAGE)
    with ContactsBook() as contacts, NotesManager() as notes:
        assistant = Assistant(contacts, notes)
        while True:
            formatter.print_input("Enter a command, please: ")
            user_input = input()
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
            elif command == "edit-email":
                formatter.print_info(assistant.edit_email(args))
            elif command == "find-notes":
                formatter.print_table(assistant.find_notes(args))
            elif command == "edit-birthday":
                formatter.print_info(assistant.edit_birthday(args))
            elif command == "show-birthdays":
                formatter.print_table(assistant.show_birthdays(args))
            elif command == "show-notes":
                formatter.print_table(assistant.show_notes())
            elif command == "edit-note":
                formatter.print_info(assistant.edit_note(args))
            elif command == "delete-note":
                formatter.print_table(assistant.delete_note(args))
            else:
                formatter.print_error("Please, provide a correct command.")


if __name__ == "__main__":
    run()
