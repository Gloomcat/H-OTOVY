class ContactNotFoundError(Exception):
    """Raised when a contact is not found."""
    pass


class InvalidFormatError(Exception):
    """Raised for general invalid format errors."""
    pass


class InvalidCommandArgumentError(Exception):
    """Raised for invalid command argument errors."""
    pass


class PhoneIsExistError(Exception):
    """Raised when a phone number already exists."""
    pass


class InputOutputError(Exception):
    """Raised for input/output errors."""
    pass


class IncorrectInputError(Exception):
    """Raised for general incorrect input."""
    pass


# Add contacts
class InsufficientContactArgumentsError(Exception):
    """Raised for insufficient arguments in adding contact."""
    pass


class ContactExistsError(Exception):
    """Raised when a contact already exists."""
    pass


# Edit contact
class InsufficientEditContactArgumentsError(Exception):
    """Raised for insufficient arguments in editing contact."""
    pass


class InvalidContactIDError(Exception):
    """Raised for invalid contact ID."""
    pass


# Delete contact
class InsufficientDeleteContactArgumentsError(Exception):
    """Raised for insufficient arguments in deleting contact."""
    pass


# Notes (Add, Edit, Delete)
class InsufficientNoteArgumentsError(Exception):
    """Raised for insufficient arguments in note operations."""
    pass


class InvalidNoteIDError(Exception):
    """Raised for invalid note ID."""
    pass


# Search (Contacts and Notes)
class InsufficientSearchCriteriaError(Exception):
    """Raised for insufficient search criteria."""
    pass


class InvalidSearchCriteriaError(Exception):
    """Raised for invalid search criteria."""
    pass


# Add tags
class InsufficientTagArgumentsError(Exception):
    """Exception raised for errors due to insufficient arguments for adding tags."""
    pass


class InvalidNoteOrContactIDError(Exception):
    """Exception raised for errors due to an invalid note or contact ID for tagging."""
    pass


class TagAdditionError(Exception):
    """Exception raised for general errors during tag addition."""
    pass


# Search notes by tags
class InsufficientTagSearchArgumentsError(Exception):
    """Exception raised for errors due to insufficient tag search arguments."""
    pass


class InvalidTagError(Exception):
    """Exception raised for errors due to invalid tags for search."""
    pass


class TagSearchError(Exception):
    """Exception raised for general errors during searching by tags."""
    pass


# Upcoming birthdays
class InvalidDaysFormatError(Exception):
    """Exception raised for errors due to invalid days format for upcoming birthdays."""
    pass


class UpcomingBirthdaysError(Exception):
    """Exception raised for general errors during calculation of upcoming birthdays."""
    pass


def error_handler(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ContactNotFoundError:
            print("Error: Contact not found.")
        except InvalidFormatError:
            print("Error: Invalid format. Please check your input format.")
        except InvalidCommandArgumentError:
            print("Error: Invalid command argument. Please provide a valid argument.")
        except PhoneIsExistError:
            print("Error: Phone number already exists. Please use a different phone number.")
        except InputOutputError:
            print("Error: Input/output error. There was a problem with input or output operations.")
        except IncorrectInputError:
            print("Error: Incorrect input. Please check your input data.")
        except InsufficientContactArgumentsError:
            print("Error: Insufficient arguments in adding contact. Please provide all required information.")
        except ContactExistsError:
            print("Error: Contact already exists. Please use a different name or ID.")
        except InsufficientEditContactArgumentsError:
            print("Error: Insufficient arguments in editing contact. Please provide all required information.")
        except InvalidContactIDError:
            print("Error: Invalid contact ID. Please provide a valid contact ID.")
        except InsufficientDeleteContactArgumentsError:
            print("Error: Insufficient arguments in deleting contact. Please provide all required information.")
        except InsufficientNoteArgumentsError:
            print("Error: Insufficient arguments in note operations. Please provide all required information.")
        except InvalidNoteIDError:
            print("Error: Invalid note ID. Please provide a valid note ID.")
        except InsufficientSearchCriteriaError:
            print("Error: Insufficient search criteria. Please provide more criteria.")
        except InvalidSearchCriteriaError:
            print("Error: Invalid search criteria. Please use valid search criteria.")
        except InsufficientTagArgumentsError:
            print("Error: Insufficient arguments for adding tags. Please provide all required information.")
        except InvalidNoteOrContactIDError:
            print("Error: Invalid note or contact ID for tagging. Please use valid IDs.")
        except TagAdditionError:
            print("Error: Error during tag addition. Please try again.")
        except InsufficientTagSearchArgumentsError:
            print("Error: Insufficient tag search arguments. Please provide more criteria.")
        except InvalidTagError:
            print("Error: Invalid tags for search. Please use valid tags.")
        except TagSearchError:
            print("Error: Error during tag search. Please try again.")
        except InvalidDaysFormatError:
            print("Error: Invalid days format for upcoming birthdays. Please provide a valid format.")
        except UpcomingBirthdaysError:
            print("Error: Error during calculation of upcoming birthdays. Please try again.")
        except Exception as e:
            return f"An unexpected error occurred: {e}"

    return inner


def input_error_handler(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "No command provided. Please enter a command."
        except ValueError as e:
            return f"Error in command: {e}"
        except Exception as e:
            return f"An unexpected error occurred: {e}"

    return inner
