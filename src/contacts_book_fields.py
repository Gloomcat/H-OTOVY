import re
from abc import abstractmethod


class FieldError(Exception):
    pass


class _Field:
    def __init__(self, value: str):
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


class Name(_Field):
    def __init__(self, value):
        super().__init__(value.lower().capitalize())

    def validation_func(self, value):
        return re.match("^[a-zA-Z]+$", value)

    def validation_fail_msg(self):
        return "Name should contain only letters."


"""
All field subclasses have to look like:

class FieldImplementation(_Field)
    def validation_func():
        ...
    def validation_fail_msg(self):
        ...

FieldError must be processed in case of validation fail.
"""

if __name__ == "__main__":
    pass
