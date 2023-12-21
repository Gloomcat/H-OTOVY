import re
from abc import abstractmethod
from datetime import datetime


class FieldError(Exception):
    pass


class _Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if self.validation_func and not self.validation_func(value):
            raise FieldError(self.validation_fail_msg())
        self.__value = value

    def __str__(self):
        return str(self.value)

    def __eq__(self, value):
        return self.value == value

    @abstractmethod
    def validation_func(self, value):
        return NotImplemented

    @abstractmethod
    def validation_fail_msg(self):
        return NotImplemented


class Id(_Field):
    def validation_func(self, value):
        if isinstance(value, int):
            return True
        try:
            int(value)
        except ValueError:
            return False
        return True

    def validation_fail_msg(self):
        return "Id should be number."


class Name(_Field):
    def __init__(self, value):
        super().__init__(value.lower().capitalize())

    def validation_func(self, value):
        return re.match("^[a-zA-Z]+$", value)

    def validation_fail_msg(self):
        return "Name should contain only letters."
    
    
class Birthday(_Field):
    def __init__(self, value):
        if not isinstance(value, datetime):
            raise TypeError("Birthday must be a date in format DD.MM.YYYY.")
        super().__init__(value)


class Phone(_Field):
    def validation_func(self, value):
        return re.match(r'\+\d{12}$', value)

    def validation_fail_msg(self):
        return "Phone number is invalid. Phone should start with '+' sign and contain 12 digits"
