import re
from abc import abstractmethod


class FieldError(Exception):
    """
    Exception raised for errors in the Field input.

    Attributes:
        message (str): Explanation of the error.
    """
    pass


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
            raise FieldError(self.validation_fail_msg())
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

    def validation_func(self, value):
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

    def __init__(self, value):
        """
        Initializes a new Name instance with the provided value.

        Parameters:
        value (str): The initial name value, which will be capitalized.
        """
        super().__init__(value.lower().capitalize())

    def validation_func(self, value):
        """
        Validates whether the value contains only letters.

        Parameters:
        value: The value to be validated.

        Returns:
        bool: True if the value contains only letters, False otherwise.
        """
        return re.match("^[a-zA-Z]+$", value)

    def validation_fail_msg(self):
        """
        Provides a failure message for Name validation.

        Returns:
        str: A message indicating that the name should contain only letters.
        """
        return "Name should contain only letters."


class Phone(_Field):
    """
    A field representing a Phone number, extending _Field.
    """

    def validation_func(self, value):
        """
        Validates whether the value is a valid phone number.

        Parameters:
        value: The value to be validated.

        Returns:
        bool: True if the value is a valid phone number, False otherwise.
        """
        return re.match(r'\+\d{12}$', value)

    def validation_fail_msg(self):
        """
        Provides a failure message for Phone number validation.

        Returns:
        str: A message indicating the format for a valid phone number.
        """
        return "Phone number is invalid. Phone should start with '+' sign and contain 12 digits."

