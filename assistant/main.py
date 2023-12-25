import re

from contacts import ContactsBook
from notes import NotesManager
from help import assistant_help, get_command_list
from error_handler import input_error_handler, error_handler
from output_formater import OutputFormatter
from autocomplete import AutoCompleter


class Assistant:
    """
    A class representing an assistant for managing contacts and notes.

    Attributes:
        WELCOME_MESSAGE (str): A constant string containing the welcome message for the user.
        FAREWELL_MESSAGE (str): A constant string containing the farewell message.
        contacts (ContactsBook): An instance of ContactsBook for managing contact data.
        notes (NotesManager): An instance of NotesManager for managing note data.
        formatter (OutputFormatter): An instance of OutputFormatter for managing prompts and output messages
    """

    WELCOME_MESSAGE = (
        "Welcome to the Assistant!\n"
        "I am ready to help you manage your contacts and notes.\n"
        "Type 'help' to see a list of available commands, 'exit' or 'close' to finish the session."
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
        self.formatter = OutputFormatter()

    @error_handler
    def _get_value_request(self, prompt):
        """
        Get user input for a specific value based on the provided prompt.

        Parameters:
        - prompt (str): The prompt indicating the type of value to be entered.

        Returns:
        str: The user-entered value.
        """
        while True:
            self.formatter.print_input(f"Enter a {prompt}: ")
            try:
                value_input = input()
            except KeyboardInterrupt:
                self.formatter.print_error(
                    "Error: Ctrl + C is not supported on current step."
                )
                continue
            return value_input

    @error_handler
    def _get_address_request(self):
        """
        Get user input for an address by prompting for ZIP code, country, city, and street.

        Returns:
        str: The formatted address string.
        """
        values = []
        for prompt in (
            "ZIP code",
            "country",
            "city",
            "street (optional: building number, appartment)",
        ):
            values.append(self._get_value_request(prompt))
        values = list(filter(lambda v: v != "", values))
        return ", ".join(values)

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
    def add_contact(self):
        """
        Adds a new contact to the contacts book.

        Returns:
        str: A message indicating the success or failure of the operation.
        """
        name = self._get_value_request(
            "name (should contain only letters and spaces)")
        self.contacts.check_name_uniqueness(name)
        phone = self._get_value_request("phone (should be like +380501234567)")
        self.contacts.check_phone_uniqueness(phone)
        result = self.contacts.add_contact(name, phone)
        self.formatter.print_info(result)

        self.formatter.print_input(
            "Would you like to add more info about the contact (email, birthday, address) (Y/n)?:"
        )
        answer = input()
        if answer == "Y":
            id = self.contacts.get_id_for(name)
            self.formatter.print_info(
                self.contacts.edit_email(
                    id,
                    self._get_value_request(
                        "email (should be like abc.def@gmail.com)"),
                )
            )
            self.formatter.print_info(
                self.contacts.edit_birthday(
                    id, self._get_value_request(
                        "birthday in a format DD.MM.YYYY")
                )
            )
            self.formatter.print_info(
                self.contacts.edit_address(id, self._get_address_request())
            )

    @error_handler
    def find_contacts(self, args):
        """
        Finds and retrieves contacts based on the provided criteria and value.

        Parameters:
        args (list): A list containing the criteria and value to search for.
                    The first element is the criteria (e.g., "id", "name"), and the second element is the value to search for.

        Returns:
        list: A list containing the contacts that match the specified criteria and value.
        """
        criteria, value = args
        return self.contacts.find_contacts(criteria, value)

    @error_handler
    def delete_contact(self, args):
        """
        Deletes a contact based on the provided ID.

        Parameters:
        args (list): A list containing the ID of the contact to be deleted.

        Returns:
        str: A message indicating the success or failure of the deletion operation.
        """
        id = args[0]
        return self.contacts.delete_contact(id)

    @error_handler
    def show_contacts(self):
        """
        Retrieves and displays the list of contacts.

        Returns:
        str: A message indicating the success or failure of the operation.
        """
        return self.contacts.show_contacts()

    @error_handler
    def show_notes(self):
        """
        Retrieves and displays the list of notes.

        Returns:
        str: A message indicating the success or failure of the operation.
        """
        return self.notes.show_notes()

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
    def find_contacts(self, args):
        """
        Find contacts based on the specified criteria and value.

        Parameters:
        - args (tuple): A tuple containing the criteria and value for the contact search.

        Returns:
        list: A list of contacts that match the search criteria.
        """
        criteria, value = args
        return self.contacts.find_contacts(criteria, value)

    @error_handler
    def edit_name(self, args):
        """
        Edit the name of a contact with the specified ID.

        Parameters:
        - args (tuple): A tuple containing the contact ID and the new name.

        Returns:
        str: A message indicating the success of the name edit.
        """
        id, name = args
        return self.contacts.edit_name(id, name)

    @error_handler
    def edit_email(self, args):
        """
        Edit the email of a contact with the specified ID.

        Parameters:
        - args (tuple): A tuple containing the contact ID and the new email.

        Returns:
        str: A message indicating the success of the email edit.
        """
        id, email = args
        return self.contacts.edit_email(id, email)

    @error_handler
    def edit_birthday(self, args):
        """
        Edit the birthday of a contact with the specified ID.

        Parameters:
        - args (tuple): A tuple containing the contact ID and the new birthday.

        Returns:
        str: A message indicating the success of the birthday edit.
        """
        id, birthday = args
        return self.contacts.edit_birthday(id, birthday)

    @error_handler
    def edit_address(self, args):
        """
        Edit the address of a contact with the specified ID.

        Parameters:
        - args (tuple): A tuple containing the contact ID.

        Returns:
        str: A message indicating the success of the address edit.
        """
        id = args[0]
        self.contacts.check_contacts_ids_for(id)
        address = self._get_address_request()
        return self.contacts.edit_address(id, address)

    @error_handler
    def show_birthdays(self, args):
        """
        Show upcoming birthdays within the specified number of days.

        Parameters:
        - args (tuple): A tuple containing the number of days for upcoming birthdays.

        Returns:
        list: A list of contacts with upcoming birthdays.
        """
        number_of_days = args[0]
        return self.contacts.show_birthdays(number_of_days)

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
        return self.notes.find_notes(keyword)

    @error_handler
    def edit_note(self, args):
        """
        Edit the content of a note with the specified ID.

        Parameters:
        - args (list): A list containing the note ID and the new content.

        Returns:
        str: A message indicating the success of the note edit.
        """
        id, new_content = args[0], " ".join(args[1:])
        return self.notes.edit_note(id, new_content)

    @error_handler
    def delete_note(self, args):
        """
        Delete a note with the specified ID.

        Parameters:
        - args (list): A list containing the note ID.

        Returns:
        str: A message indicating the success of the note deletion.
        """
        return self.notes.delete_note(args[0])

    @error_handler
    def add_note_tag(self, args):
        """
        Add a tag to a note with the specified ID.

        Parameters:
        - args (list): A list containing the note ID and the tag to be added.

        Returns:
        str: A message indicating the success of adding the tag to the note.
        """
        id, tag = args
        return self.notes.add_note_tag(id, tag)

    @error_handler
    def delete_note_tag(self, args):
        """
        Delete a tag from a note with the specified ID.

        Parameters:
        - args (list): A list containing the note ID and the tag to be deleted.

        Returns:
        str: A message indicating the success of deleting the tag from the note.
        """
        id, tag = args
        return self.notes.delete_note_tag(id, tag)

    @error_handler
    def edit_note_tag(self, args):
        """
        Edit a tag for a note with the specified ID.

        Parameters:
        - args (list): A list containing the note ID, the existing tag, and the new tag.

        Returns:
        str: A message indicating the success of editing the tag for the note.
        """
        id, tag, new_tag = args
        return self.notes.edit_note_tag(id, tag, new_tag)

    @error_handler
    def find_notes_by_tag(self, args):
        """
        Find notes that have the specified tag.

        Parameters:
        - args (list): A list containing the tag to search for.

        Returns:
        list: A list of notes that have the specified tag.
        """
        return self.notes.find_notes_by_tag(args[0])


def run():
    """
    Runs the assistant application, handling user input and responses.

    This function initializes the Assistant and handles the main loop for user interaction. It processes user commands and displays responses or errors.
    """
    auto_completer = AutoCompleter(get_command_list())
    formatter = OutputFormatter()
    formatter.print_greeting(Assistant.WELCOME_MESSAGE)

    with ContactsBook() as contacts, NotesManager() as notes:
        assistant = Assistant(contacts, notes)

        while True:
            try:
                formatter.print_input("Enter a command, please: ")
                user_input = auto_completer.get_user_input()
            except KeyboardInterrupt:
                formatter.print_error(
                    "Error: Ctrl + C is not supported. Use 'close' or 'exit'."
                )
                continue
            try:
                command, *args = assistant.parse_input(user_input)
            except TypeError:
                # raised only when exception was handled in @input_error_handler
                continue

            if command in ["exit", "close"]:
                formatter.print_greeting(Assistant.FAREWELL_MESSAGE)
                break
            elif command == "help":
                formatter.print_table(assistant_help())
            elif command == "add-contact":
                assistant.add_contact()
            elif command == "delete-contact":
                formatter.print_info(assistant.delete_contact(args))
            elif command == "show-contacts":
                formatter.print_table(assistant.show_contacts())
            elif command == "find-contacts":
                formatter.print_table(assistant.find_contacts(args))
            elif command == "add-note":
                formatter.print_info(assistant.add_note(args))
            elif command == "edit-name":
                formatter.print_info(assistant.edit_name(args))
            elif command == "edit-phone":
                formatter.print_info(assistant.edit_phone(args))
            elif command == "edit-email":
                formatter.print_info(assistant.edit_email(args))
            elif command == "edit-address":
                formatter.print_info(assistant.edit_address(args))
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
                formatter.print_info(assistant.delete_note(args))
            elif command == "add-note-tag":
                formatter.print_info(assistant.add_note_tag(args))
            elif command == "delete-note-tag":
                formatter.print_info(assistant.delete_note_tag(args))
            elif command == "edit-note-tag":
                formatter.print_info(assistant.edit_note_tag(args))
            elif command == "find-notes-by-tag":
                formatter.print_table(assistant.find_notes_by_tag(args))
            else:
                formatter.print_error("Please, provide a correct command.")


if __name__ == "__main__":
    run()
