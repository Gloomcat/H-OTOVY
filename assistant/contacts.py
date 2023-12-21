from collections import UserDict

from fields import FieldError, Id, Name, Phone
from storage import PersistantStorage


class Record(UserDict):
    """
    A class representing a record of an individual, storing personal information.

    Attributes:
    data (dict): A dictionary to store the individual's information.
    id (int): The unique identifier of the individual.
    name (str): The name of the individual.
    phone (str): The phone number of the individual.
    email (str): The email address of the individual.
    birthday (str): The birthday of the individual.
    address (str): The home address of the individual.
    """

    def __init__(
        self,
        id: int,
        name: str,
        phone: str,
        email: str = "",
        birthday: str = "",
        address: str = "",
    ):
        """
        Initializes a new Record instance.

        Parameters:
        id (int): The unique identifier for the record.
        name (str): The name of the individual.
        phone (str): The phone number of the individual.
        email (str, optional): The email address of the individual. Defaults to an empty string.
        birthday (str, optional): The birthday of the individual. Defaults to an empty string.
        address (str, optional): The address of the individual. Defaults to an empty string.
        """
        super().__init__()
        self.data["id"] = None
        self.data["name"] = ""
        self.data["phone"] = ""
        self.data["email"] = ""
        self.data["birthday"] = ""
        self.data["address"] = ""
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email
        self.birthday = birthday
        self.address = address

    @property
    def id(self):
        """
        Gets or sets the unique identifier of the individual.

        Returns:
        int: The unique identifier of the individual.
        """
        return self.data["id"]

    @id.setter
    def id(self, id: int):
        """
        Sets the unique identifier of the individual.

        Parameters:
        id (int): The unique identifier to be set.
        """
        try:
            self.data["id"] = Id(id)
        except FieldError as e:
            raise e

    @property
    def name(self):
        """
        Gets or sets the name of the individual.

        Returns:
        str: The name of the individual.
        """
        return self.data["name"]

    @name.setter
    def name(self, name: str):
        """
        Sets the name of the individual.

        Parameters:
        name (str): The name to be set.
        """
        try:
            self.data["name"] = Name(name)
        except FieldError as e:
            raise e

    @property
    def phone(self):
        """
        Gets or sets the phone number of the individual.

        Returns:
        str: The phone number of the individual.
        """
        return self.data["phone"]

    @phone.setter
    def phone(self, phone: str):
        """
        Sets the phone number of the individual.

        Parameters:
        phone (str): The phone number to be set.
        """
        try:
            self.data["phone"] = Phone(phone)
        except FieldError as e:
            raise e

    @property
    def email(self):
        """
        Gets or sets the email address of the individual.

        Returns:
        str: The email address of the individual.
        """
        return self.data["email"]

    @email.setter
    def email(self, email: str):
        """
        Sets the email address of the individual.

        Parameters:
        email (str): The email address to be set.
        """
        try:
            self.data["email"] = email  # Email(email)
        except FieldError as e:
            raise e

    @property
    def birthday(self):
        """
        Gets or sets the birthday of the individual.

        Returns:
        str: The birthday of the individual.
        """
        return self.data["birthday"]

    @birthday.setter
    def birthday(self, birthday: str):
        """
        Sets the birthday of the individual.

        Parameters:
        birthday (str): The birthday to be set.
        """
        try:
            self.data["birthday"] = birthday  # Birthday(birthday)
        except FieldError as e:
            raise e

    @property
    def address(self):
        """
        Gets or sets the address of the individual.

        Returns:
        str: The address of the individual.
        """
        return self.data["address"]

    @address.setter
    def address(self, address: str):
        """
        Sets the address of the individual.

        Parameters:
        address (str): The address to be set.
        """
        try:
            self.data["address"] = address  # Address(address)
        except FieldError as e:
            raise e


class ContactsBook(PersistantStorage):
    """
    A class representing a contacts book, storing and managing a collection of contacts.

    Inherits from PersistentStorage for CSV file operations.

    Attributes:
        data (list): A list to store the contact records.
    """

    def __init__(self):
        """
        Initializes a new ContactsBook instance with specified column headers and record type.
        """
        super().__init__("contacts.csv", [
            "id", "name", "phone", "email", "birthday", "address"], Record)

    @PersistantStorage.update
    def add_contact(self, name, phone):
        """
        Adds a new contact to the contacts book.

        Parameters:
        name (str): The name of the contact to be added.
        phone (str): The phone number of the contact to be added.

        Returns:
        str: A message indicating the success or failure of the operation.
        """
        if any(record.phone == phone for record in self.data):
            # raise according Error from error_handler.py in case the phone already exists
            return "Contact with the phone already exists."
        if any(record.name == name for record in self.data):
            # raise according Error from error_handler.py in case the name already exists
            return "Contact with the name already exists."
        id = len(self.data)
        record = Record(id, name, phone)
        self.data.append(record)
        return "Contact added successfully."

    def edit_phone(self, id, phone):
        """
        Edits the phone number of an existing contact in the contacts book.

        Parameters:
        id (int): The id of the contact whose phone number needs to be updated.
        phone (str): The new phone number to be set for the contact.

        Returns:
        str: A message indicating the success or failure of the operation.
        """
        records = list(filter(lambda record: record["id"] == id, self.data))
        if not records:
            return "Contact with Id doesn't exist"
        if len(records) > 1:
            return "Error: duplicate id found"
        records[0].phone = phone
        return f"Phone update for contact with Id: {id}"
