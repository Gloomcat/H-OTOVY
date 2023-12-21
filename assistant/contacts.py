from collections import UserDict

from fields import FieldError, Id, Name, Phone, Email
from storage import PersistantStorage


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
            self.data["phone"] = Phone(phone)
        except FieldError as e:
            raise e

    @property
    def email(self):
        return self.data["email"]

    @email.setter
    def email(self, email: str):
        try:
            self.data["email"] = Email(email) if email else ""
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

    def __repr__(self):
         return f"{self.id} {self.name} {self.phone} {self.email} {self.address} {self.birthday}"
    
    
class ContactsBook(PersistantStorage):
    def __init__(self):
        super().__init__("contacts.csv", [
            "id", "name", "phone", "email", "birthday", "address"], Record)

    @PersistantStorage.update
    def add_contact(self, name, phone, email="", address="", birthday=""):
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

    def edit_phone(self, id, phone):
        records = list(filter(lambda record: record["id"] == id, self.data))
        if not records:
            return "Contact with Id doesn't exist"
        if len(records) > 1:
            return "Error: duplicate id found"
        records[0].phone = phone
        return f"Phone update for contact with Id: {id}"
    
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

