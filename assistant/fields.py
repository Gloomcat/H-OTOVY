import re
from abc import abstractmethod
from datetime import datetime

from assistant.error_handler import FieldValidationError


class _Field:
    """
    A base class for different types of fields in a record.

    This class defines a generic field with validation logic.

    Attributes:
        __value: Private variable to hold the value of the field.
    """

    def __init__(self, value):
        """
        Initializes a new _Field instance.

        Parameters:
        value: The initial value to be set for the field.
        """
        self.__value = None
        self.value = value

    @property
    def value(self):
        """
        Returns the value of the field.
        """
        return self.__value

    @value.setter
    def value(self, value):
        """
        Sets the value of the field with validation.

        Parameters:
        value: The value to be set for the field.

        Raises:
        FieldError: If the value does not pass the validation.
        """
        if self.validation_func and not self.validation_func(value):
            raise FieldValidationError(self.validation_fail_msg())
        self.__value = value

    def __str__(self):
        return str(self.value)

    def __eq__(self, value):
        return self.value == value

    @abstractmethod
    def validation_func(self, value):
        """
        The validation function to be implemented in subclasses.

        Parameters:
        value: The value to be validated.

        Returns:
        bool: True if validation passes, False otherwise.
        """
        return NotImplemented

    @abstractmethod
    def validation_fail_msg(self):
        """
        The validation failure message to be implemented in subclasses.

        Returns:
        str: A message describing the reason for validation failure.
        """
        return NotImplemented


class Id(_Field):
    """
    A field representing an Id, extending _Field.
    """

    def __init__(self, value: (int, str)):
        """
        Initializes a new Id instance with the provided value.

        Parameters:
        value (str, int): The initial Id value, which will be converted to 'int' if needed.
        """
        try:
            value = int(value) if isinstance(value, str) else value
            super().__init__(value)
        except ValueError:
            raise FieldValidationError(self.validation_fail_msg())

    def validation_func(self, value: (int, str)):
        """
        Validates whether the value is an integer.

        Parameters:
        value: The value to be validated.

        Returns:
        bool: True if the value is an integer, False otherwise.
        """
        if isinstance(value, int):
            return True
        try:
            int(value)
        except ValueError:
            return False
        return True

    def validation_fail_msg(self):
        """
        Provides a failure message for Id validation.

        Returns:
        str: A message indicating that the Id should be a number.
        """
        return "Id should be a number."


class Name(_Field):
    """
    A field representing a Name, extending _Field.
    """

    def __init__(self, value: str):
        """
        Initializes a new Name instance with the provided value.

        Parameters:
        value (str): The initial name value, which will be capitalized.
        """
        super().__init__(" ".join([v.lower().capitalize() for v in value.split(" ")]))

    def validation_func(self, value: str):
        """
        Validates whether the value contains only letters.

        Parameters:
        value: The value to be validated.

        Returns:
        bool: True if the value contains only letters or spaces, False otherwise.
        """
        return re.match("^[a-zA-Z ]+$", value)

    def validation_fail_msg(self):
        """
        Provides a failure message for Name validation.

        Returns:
        str: A message indicating that the name should contain only letters.
        """
        return "Name should contain only letters and spaces."


class Birthday(_Field):
    """
    A field representing the birthday of a contact.

    Inherits from _Field class.

    Methods:
    - validation_func(value: str) -> bool: Validate the provided birthday value.
    - validation_fail_msg() -> str: Get the validation failure message.

    Attributes:
    - value (str): The value of the birthday field.
    """

    def validation_func(self, value: str) -> bool:
        """
        Validate the provided birthday value.

        Parameters:
        - value (str): The birthday value to be validated.

        Returns:
        bool: True if the validation succeeds, False otherwise.
        """
        if value == "":
            return True
        try:
            value = datetime.strptime(value, "%d.%m.%Y")
        except Exception:
            return False
        if value > datetime.today():
            return False
        return True

    def validation_fail_msg(self) -> str:
        """
        Get the validation failure message.

        Returns:
        str: The validation failure message.
        """
        return "Invalid birthday date. Format should be DD.MM.YYYY, date should be in the past."


class Email(_Field):
    """
    A field representing the email address of a contact.

    Inherits from _Field class.

    Methods:
    - validation_func(value: str) -> bool: Validate the provided email value.
    - validation_fail_msg() -> str: Get the validation failure message.

    Attributes:
    - value (str): The value of the email field.
    """

    def __init__(self, value: str):
        """
        Initialize an Email object.

        Parameters:
        - value (str): The initial value of the email field.
        """
        super().__init__(value.lower())

    def validation_func(self, value: str) -> bool:
        """
        Validate the provided email value.

        Parameters:
        - value (str): The email value to be validated.

        Returns:
        bool: True if the validation succeeds, False otherwise.
        """
        if value == "":
            return True
        return re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", value)

    def validation_fail_msg(self) -> str:
        """
        Get the validation failure message.

        Returns:
        str: The validation failure message.
        """
        return "Email is invalid. Please follow the format: Any.Name.or.Full.name@sub.domain."


class Phone(_Field):
    """
    A field representing a Phone number, extending _Field.
    """

    def validation_func(self, value: str):
        """
        Validates whether the value is a valid phone number.

        Parameters:
        value: The value to be validated.

        Returns:
        bool: True if the value is a valid phone number, False otherwise.
        """
        return re.match(r"\+\d{12}$", value)

    def validation_fail_msg(self):
        """
        Provides a failure message for Phone number validation.

        Returns:
        str: A message indicating the format for a valid phone number.
        """
        return "Phone number is invalid. Phone should start with '+' sign and contain 12 digits."


class Address(_Field):
    def __init__(self, value: str):
        """
        Initializes an Address object.

        Parameters:
        value (str): The input address value.

        Note:
        The address is formatted by capitalizing the first letter of each word after splitting by commas.
        """
        super().__init__(", ".join([v.lower().capitalize() for v in value.split(", ")]))

    def validation_func(self, value: str):
        """
        Validates the provided address value.

        Parameters:
        value (str): The address value to be validated.

        Returns:
        bool: True if the address is valid or an empty string, False otherwise.
        """
        if value == "":
            return True
        self.pattern = re.compile(r"^[A-Za-z0-9\.\-\s\,]+$")
        return self.pattern.match(value)

    def validation_fail_msg(self):
        """
        Returns an error message for address validation failure.

        Returns:
        str: Error message indicating the correct format for the address.
        """
        return 'Address is incorect, please, try again, use letters, numbers and ".", "/", "-", ".".'
