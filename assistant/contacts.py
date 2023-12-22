from collections import UserDict, defaultdict
from datetime import datetime
import calendar

from fields import FieldError, Id, Name, Phone
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
        super().__init__("contacts.csv", [
            "id", "name", "phone", "email", "birthday", "address"], Record)

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
        return f"Contact added successfully with Id: {id}."

    def edit_phone(self, id, phone):
        id = Id(id)
        records = list(filter(lambda record: record["id"] == id, self.data))
        if not records:
            return "Contact with Id doesn't exist"
        if len(records) > 1:
            return "Error: duplicate id found"
        records[0].phone = phone
        return f"Phone update for contact with Id: {id}"
    
    def edit_birthday(self, id, birthday):
        id = Id(id)
        records = list(filter(lambda record: record["id"] == id, self.data))

        if not records:
            return "Contact with Id doesn't exist"
        if len(records) > 1:
            return "Error: duplicate id found"

        # Check if the birthday string is in the correct format 'DD.MM.YYYY'
        try:
            birthday = datetime.strptime(birthday, '%d.%m.%Y')
        except ValueError:
            return "Invalid date format. Use DD.MM.YYYY."
        
        records[0].birthday = birthday
        return f"Birthday update for contact with Id: {id}"
    
    def show_birthdays(self, number_of_days):
        today = datetime.now()
        upcoming_birthdays = []

        for record in self.data.values():
            if record['birthday']:
                try:
                    # Parse the birthday string to a datetime object
                    birth_date = datetime.strptime(record['birthday'], '%d.%m.%Y').replace(year=today.year)

                    # Adjust for leap years
                    if birth_date.month == 2 and birth_date.day == 29:
                        if not (today.year % 4 == 0 and (today.year % 100 != 0 or today.year % 400 == 0)):
                            # Adjust the birthday to Mar 1 in non-leap years
                            birth_date = datetime(today.year, 3, 1)

                    # Calculate the number of days until the birthday
                    delta = (birth_date - today).days

                    # Check if the birthday is within the specified number of days
                    if 0 <= delta <= number_of_days:
                        formatted_birthday = birth_date.strftime('%d.%m.%Y')
                        upcoming_birthdays.append(f"{formatted_birthday}: {record['name']}")
                except ValueError:
                    # Обробка невірного формату дати
                    continue

        return upcoming_birthdays
    
    # def show_birthdays(self, number_of_days):
    #     records = []
    #     for record in self.data:
    #         # if datetime.date(record.birthday) <= number_of_days:
    #             records.append(record.birthday)
    #     return records
