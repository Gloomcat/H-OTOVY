from contacts_book_fields import Name


class ContactsBook:
    def __init__(self):
        self.data = {}

    def add_contact(self, name, phone_number, email, address, birthday):
        if name in self.data.keys():
            return "Contact already exists."
        self.data[name] = {
            "phone": phone_number,
            "email": email,
            "address": address,
            "birthday": birthday,
        }
        return "Contact added successfully."


if __name__ == "__main__":
    pass
