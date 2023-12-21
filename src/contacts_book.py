from collections import UserDict, defaultdict
from datetime import datetime
import calendar

from fields import FieldError, Id, Name
from persistant_storage import PersistantStorage


class Record(UserDict):
    def __init__(
        self,
        id: int,
        name: str,
        phone: str,
        email: str = "",
        birthday: str = "",
        address: str = "",
    ):
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
        return self.data["id"]

    @id.setter
    def id(self, id: int):
        try:
            self.data["id"] = Id(id)
        except FieldError as e:
            raise e

    @property
    def name(self):
        return self.data["name"]

    @name.setter
    def name(self, name: str):
        try:
            self.data["name"] = Name(name)
        except FieldError as e:
            raise e

    @property
    def phone(self):
        return self.data["phone"]

    @phone.setter
    def phone(self, phone: str):
        try:
            self.data["phone"] = phone  # Phone(phone)
        except FieldError as e:
            raise e

    @property
    def email(self):
        return self.data["email"]

    @email.setter
    def email(self, email: str):
        try:
            self.data["email"] = email  # Email(email)
        except FieldError as e:
            raise e

    @property
    def birthday(self):
        return self.data["birthday"]

    @birthday.setter
    def birthday(self, birthday: str):
        try:
            self.data["birthday"] = birthday  # Birthday(birthday)
        except FieldError as e:
            raise e

    @property
    def address(self):
        return self.data["address"]

    @address.setter
    def address(self, address: str):
        try:
            self.data["address"] = address  # Address(address)
        except FieldError as e:
            raise e


class ContactsBook(PersistantStorage):
    def __init__(self):
        super().__init__("contacts.csv", ["id", "name", "phone", "email", "birthday", "address"], Record)

    @PersistantStorage.update
    def add_contact(self, name, phone):
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

    def show_birthdays(self, until_date: datetime.date):
        records = []
        for record in self.data:
            if datetime.date(record.birthday) <= until_date:
                records.append(record)
        return records

if __name__ == "__main__":
    pass
