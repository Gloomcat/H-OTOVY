from collections import UserDict
from datetime import datetime

from fields import Id, Name, Phone, Email, Birthday, Address
from storage import PersistantStorage
from error_handler import (
    EmptyContactsError,
    InvalidNoteOrContactIDError,
    NameIsExistError,
    PhoneIsExistError,
    EmailIsExistError,
    NoResultsFoundError,
    InvalidBirthdayDaysParameter,
    FieldValidationError,
)


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
        except FieldValidationError as e:
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
        except FieldValidationError as e:
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
        except FieldValidationError as e:
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
            self.data["email"] = Email(email)
        except FieldValidationError as e:
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
        except FieldValidationError as e:
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
            self.data["address"] = Address(address)
        except FieldValidationError as e:
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
        super().__init__(
            "contacts.csv",
            ["id", "name", "phone", "email", "birthday", "address"],
            Record,
        )

    def _get_available_ids(self):
        """
        Get the available contact IDs.

        Returns:
        tuple: A tuple containing the available contact IDs.
        """
        if not self.data:
            return ()
        return tuple(range(0, len(self.data)))

    def _update_ids(self):
        """
        Update the IDs of all contacts in the storage to match their current positions.

        This function is typically called after contacts have been added or deleted, ensuring
        that the IDs of the remaining contacts reflect their sequential order in the storage.

        Returns:
        None
        """
        for id in range(len(self.data)):
            self.data[id].id = id

    def check_phone_uniqueness(self, phone: str):
        """
        Check if a contact with the specified phone number already exists.

        Parameters:
        - phone (str): The phone number to be checked.

        Raises:
        - PhoneIsExistError: If a contact with the specified phone number already exists.
        """
        phone = Phone(phone)
        if any(str(record.phone) == str(phone.value) for record in self.data):
            raise PhoneIsExistError(
                f"Contact with the phone: {phone} already exists.")

    def check_name_uniqueness(self, name: str):
        """
        Check if a contact with the specified name already exists.

        Parameters:
        - name (str): The name to be checked.

        Raises:
        - NameIsExistError: If a contact with the specified name already exists.
        """
        name = Name(name)
        if any(str(record.name) == str(name.value) for record in self.data):
            raise NameIsExistError(
                f"Contact with the name: {name} already exists.")

    def _check_email_uniqueness(self, email: str):
        """
        Check if a contact with the specified email already exists.

        Parameters:
        - email (str): The email to be checked.

        Raises:
        - EmailIsExistError: If a contact with the specified email already exists.
        """
        email = Email(email)
        if any(str(record.email) == str(email.value) for record in self.data):
            raise EmailIsExistError(
                f"Contact with the email: {email} already exists.")

    def _check_empty_result(self, content: list):
        """
        Check if the search result is empty.

        Parameters:
        - content (list): The content to be checked.

        Raises:
        - NoResultsFoundError: If the content is empty.
        """
        if not content or content == []:
            raise NoResultsFoundError("Error: No contacts found during search.")

    def _check_days_parameter(self, days: str):
        """
        Check if the provided days parameter is a valid number.

        Parameters:
        - days (str): The days parameter to be checked.

        Raises:
        - InvalidBirthdayDaysParameter: If the days parameter is not a valid number.
        """
        if not days or not days.isnumeric():
            raise InvalidBirthdayDaysParameter(
                "Error: Days count parameter must be a valid number."
            )

    def check_contacts_ids_for(self, id: str = None):
        """
        Check if the provided contact ID is valid.

        Parameters:
        - id (str): The contact ID to be checked. Defaults to None.

        Raises:
        - EmptyContactsError: If the contacts list is empty.
        - InvalidNoteOrContactIDError: If the provided contact ID is invalid.

        Returns:
        int: The validated contact ID.
        """
        if id:
            id = Id(id).value
        ids = self._get_available_ids()
        if not ids:
            raise EmptyContactsError("Error: Contacts list is empty.")
        if id and id not in ids:
            error_msg = f"Error: Invalid contact Id. Possible Id: 0."
            if len(ids) > 1:
                error_msg = error_msg[:-1] + f"-{len(ids)-1}"
            raise InvalidNoteOrContactIDError(error_msg)
        return id

    def check_contacts_ids(self):
        """
        Check if any contact IDs are available.

        Raises:
        - EmptyContactsError: If the contacts list is empty.

        Returns:
        tuple: A tuple containing the available contact IDs.
        """
        return self.check_contacts_ids_for(None)

    def get_id_for(self, name: str):
        """
        Get the ID associated with a contact's name.

        Parameters:
        - name (str): The name of the contact for which to retrieve the ID.

        Raises:
        - NoResultsFoundError: If no contact with the specified name is found.

        Returns:
        int: The ID associated with the contact's name.
        """
        result = list(
            filter(lambda contact: str(contact.name).lower() == name.lower(), self.data)
        )
        if not result:
            raise NoResultsFoundError(f"Error: Id not found for name: {name}")
        assert len(result) == 1
        return result[0].id.value

    @PersistantStorage.update
    def add_contact(
        self,
        name: str,
        phone: str,
    ):
        """
        Add a new contact with the specified details.

        Parameters:
        - name (str): The name of the contact.
        - phone (str): The phone number of the contact.

        Returns:
        str: A message indicating the success of adding the contact.
        """
        self.check_name_uniqueness(name)
        self.check_phone_uniqueness(phone)
        id = len(self.data)
        record = Record(id, name, phone)
        self.data.append(record)
        return f"Contact added successfully with Id: {id}."

    @PersistantStorage.update
    def delete_contact(self, id: str):
        """
        Delete a contact with the specified ID.

        Parameters:
        - id (str): The ID of the contact to be deleted.

        Raises:
        - InvalidNoteOrContactIDError: If the provided contact ID is invalid.

        Returns:
        str: A message indicating the success of deleting the contact.
        """
        id = self.check_contacts_ids_for(id)
        self.data.pop(id)
        self._update_ids()
        return f"Contact with Id: {id} successfully deleted."

    def show_contacts(self):
        """
        Show all contacts.

        Raises:
        - EmptyContactsError: If the contacts list is empty.

        Returns:
        list: A list containing all contacts.
        """
        self.check_contacts_ids()
        return self.data

    def find_contacts(self, criteria, value):
        """
        Find contacts based on the specified criteria and value.

        Parameters:
        - criteria (str): The criteria for the contact search.
        - value (str): The value to search for.

        Raises:
        - EmptyContactsError: If the contacts list is empty.
        - NoResultsFoundError: If no contacts are found with the specified criteria and value.

        Returns:
        list: A list of contacts that match the search criteria.
        """
        self.check_contacts_ids()
        result = []
        if criteria in ("id", "name", "phone", "email", "birthday", "address"):
            for record in self.data:
                prop = getattr(record, criteria)
                if value in str(prop.value):
                    result.append(record)
        self._check_empty_result(result)
        return result

    @PersistantStorage.update
    def edit_name(self, id: str, name: str):
        """
        Edit the name of a contact with the specified ID.

        Parameters:
        - id (str): The ID of the contact to be edited.
        - name (str): The new name for the contact.

        Raises:
        - InvalidNoteOrContactIDError: If the provided contact ID is invalid.
        - NameIsExistError: If a contact with the new name already exists.

        Returns:
        str: A message indicating the success of editing the name.
        """
        id = self.check_contacts_ids_for(id)
        self.check_name_uniqueness(name)
        self.data[id].name = name
        return f"Name successfully updated for contact with Id: {id}"

    @PersistantStorage.update
    def edit_phone(self, id: str, phone: str):
        """
        Edit the phone number of a contact with the specified ID.

        Parameters:
        - id (str): The ID of the contact to be edited.
        - phone (str): The new phone number for the contact.

        Raises:
        - InvalidNoteOrContactIDError: If the provided contact ID is invalid.
        - PhoneIsExistError: If a contact with the new phone number already exists.

        Returns:
        str: A message indicating the success of editing the phone number.
        """
        id = self.check_contacts_ids_for(id)
        self.check_phone_uniqueness(phone)
        self.data[id].phone = phone
        return f"Phone successfully updated for contact with Id: {id}"

    @PersistantStorage.update
    def edit_email(self, id: str, email: str):
        """
        Edit the email of a contact with the specified ID.

        Parameters:
        - id (str): The ID of the contact to be edited.
        - email (str): The new email for the contact.

        Raises:
        - InvalidNoteOrContactIDError: If the provided contact ID is invalid.
        - EmailIsExistError: If a contact with the new email already exists.

        Returns:
        str: A message indicating the success of editing the email.
        """
        id = self.check_contacts_ids_for(id)
        self._check_email_uniqueness(email)
        self.data[id].email = email
        return f"Email successfully updated for contact with Id: {id}"

    @PersistantStorage.update
    def edit_address(self, id: str, address: str):
        """
        Edit the address of a contact with the specified ID.

        Parameters:
        - id (str): The ID of the contact to be edited.
        - address (str): The new address for the contact.

        Raises:
        - InvalidNoteOrContactIDError: If the provided contact ID is invalid.

        Returns:
        str: A message indicating the success of editing the address.
        """
        id = self.check_contacts_ids_for(id)
        self.data[id].address = address
        return f"Address successfully updated for contact with Id: {id}"

    @PersistantStorage.update
    def edit_birthday(self, id, birthday):
        """
        Edit the birthday of a contact with the specified ID.

        Parameters:
        - id (str): The ID of the contact to be edited.
        - birthday (str): The new birthday for the contact.

        Raises:
        - InvalidNoteOrContactIDError: If the provided contact ID is invalid.

        Returns:
        str: A message indicating the success of editing the birthday.
        """
        id = self.check_contacts_ids_for(id)
        self.data[id].birthday = birthday
        return f"Birthday successfully updated for contact with Id: {id}"

    def show_birthdays(self, number_of_days: str):
        """
        Show upcoming birthdays within the specified number of days.

        Parameters:
        - number_of_days (str): The number of days for upcoming birthdays.

        Raises:
        - EmptyContactsError: If the contacts list is empty.
        - InvalidBirthdayDaysParameter: If the provided days parameter is not a valid number.

        Returns:
        list: A list of dictionaries containing the date and names of contacts with upcoming birthdays.
        """
        self.check_contacts_ids()
        self._check_days_parameter(number_of_days)

        today = datetime.now()
        birthdays_dict = {}
        number_of_days = int(number_of_days)

        for record in self.data:
            if str(record.birthday):
                birth_date = datetime.strptime(
                    str(record.birthday), "%d.%m.%Y"
                ).replace(year=today.year)

                if birth_date.month == 2 and birth_date.day == 29:
                    if not (
                        today.year % 4 == 0
                        and (today.year % 100 != 0 or today.year % 400 == 0)
                    ):
                        birth_date = datetime(today.year, 3, 1)

                delta = (birth_date - today).days

                if 0 <= delta <= number_of_days:
                    formatted_birthday = birth_date.strftime("%d.%m.%Y")
                    if formatted_birthday in birthdays_dict:
                        birthdays_dict[formatted_birthday].append(str(record.name))
                    else:
                        birthdays_dict[formatted_birthday] = [str(record.name)]

        formatted_birthdays = [
            {"date": date, "names": ", ".join(names)}
            for date, names in birthdays_dict.items()
        ]
        self._check_empty_result(formatted_birthdays)
        return formatted_birthdays
