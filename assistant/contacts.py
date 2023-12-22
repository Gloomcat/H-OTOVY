from collections import UserDict, defaultdict
from datetime import datetime
import calendar

from fields import FieldError, Id, Name, Phone, Email, Birthday
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
            self.data["email"] = Email(email) if email else ""
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
            self.data["birthday"] = Birthday(birthday)
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

    def __repr__(self):
         return f"{self.id} {self.name} {self.phone} {self.email} {self.address} {self.birthday}"
    
    
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
    def add_contact(self, name, phone, email="", address="", birthday=""):
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
        if email and address and birthday:
            record = Record(id, name, phone, email, birthday, address)
        else:
            record = Record(id, name, phone)
        self.data.append(record)
        return "Contact added successfully."
    
    @PersistantStorage.update
    def delete_contact(self, id):
        """
        Deletes a contact based on the provided ID.

        Parameters:
        id (int): The ID of the contact to be deleted.

        Returns:
        str: A message indicating the success or failure of the deletion operation.
        """
        records = list(filter(lambda record: record["id"] == id, self.data))
        if not records:
            return "Contact with Id doesn't exist!"
        self.data.remove(records[0])
        return "Contact was deleted."

    def show_contacts(self):
        """
        Retrieves and returns the list of contacts.

        Returns:
        list: A list containing the contacts.
        """
        return self.data

    @PersistantStorage.update
    def edit_phone(self, id, phone):
        id = Id(id)
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
    
    @PersistantStorage.update
    def edit_birthday(self, id, birthday):
        id = Id(id)
        records = list(filter(lambda record: record["id"] == id, self.data))

        if not records:
            return "Contact with Id doesn't exist"
        if len(records) > 1:
            return "Error: duplicate id found"

        records[0].birthday = birthday

        return f"Birthday update for contact with Id: {id}"
    
    def show_birthdays(self, number_of_days):
        today = datetime.now()
        birthdays_dict = {}
        number_of_days = int(number_of_days)

        for record in self.data:
            if record.birthday:
                try:
                    birth_date = datetime.strptime(str(record.birthday), '%d.%m.%Y').replace(year=today.year)

                    if birth_date.month == 2 and birth_date.day == 29:
                        if not (today.year % 4 == 0 and (today.year % 100 != 0 or today.year % 400 == 0)):
                            birth_date = datetime(today.year, 3, 1)

                    delta = (birth_date - today).days

                    if 0 <= delta <= number_of_days:
                        formatted_birthday = birth_date.strftime('%d.%m.%Y')
                        if formatted_birthday in birthdays_dict:
                            birthdays_dict[formatted_birthday].append(str(record.name))
                        else:
                            birthdays_dict[formatted_birthday] = [str(record.name)]
                except ValueError:
                    continue  

        formatted_birthdays = [{"date": date, "names": ', '.join(names)} for date, names in birthdays_dict.items()]
        return formatted_birthdays

    def edit_email(self, id: int, new_email: str):
        if isinstance(id, int) and isinstance(new_email, str):
            records = list(filter(lambda record: int(record.id.value) == id, self.data))
            if not records:
                return "Contact with Id doesn't exist!"
            if len(records) > 1:
                return "Error: duplicate id found"
            records[0].email = new_email
            return f"Email updated for contact with Id: {id}"
        else:
            return "Id should be number and new_email should be string."
        