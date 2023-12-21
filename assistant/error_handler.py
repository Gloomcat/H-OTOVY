from output_formater import OutputFormatter


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
    """
    A decorator function used to handle errors raised by the decorated function.

    It captures specific exceptions raised by the decorated function and formats error messages using an instance of OutputFormatter.

    Parameters:
    func (function): The function to be decorated.

    Returns:
    function: The inner function that handles exceptions and returns the result of the decorated function.
    """
    formatter = OutputFormatter()

    def inner(*args, **kwargs):
        """
        Inner function that executes the decorated function and handles specific exceptions.

        Parameters:
        *args: Variable length argument list for the decorated function.
        **kwargs: Arbitrary keyword arguments for the decorated function.

        Returns:
        Varies: The result of the decorated function or None if an exception is caught.
        """
        try:
            return func(*args, **kwargs)
        except ContactNotFoundError:
            formatter.print_error("Error: Contact not found.")
        except InvalidFormatError:
            formatter.print_error("Error: Invalid format. Please check your input format.")
        except InvalidCommandArgumentError:
            formatter.print_error("Error: Invalid command argument. Please provide a valid argument.")
        except PhoneIsExistError:
            formatter.print_error("Error: Phone number already exists. Please use a different phone number.")
        except InputOutputError:
            formatter.print_error("Error: Input/output error. There was a problem with input or output operations.")
        except IncorrectInputError:
            formatter.print_error("Error: Incorrect input. Please check your input data.")
        except InsufficientContactArgumentsError:
            formatter.print_error(
                "Error: Insufficient arguments in adding contact. Please provide all required information.")
        except ContactExistsError:
            formatter.print_error("Error: Contact already exists. Please use a different name or ID.")
        except InsufficientEditContactArgumentsError:
            formatter.print_error(
                "Error: Insufficient arguments in editing contact. Please provide all required information.")
        except InvalidContactIDError:
            formatter.print_error("Error: Invalid contact ID. Please provide a valid contact ID.")
        except InsufficientDeleteContactArgumentsError:
            formatter.print_error(
                "Error: Insufficient arguments in deleting contact. Please provide all required information.")
        except InsufficientNoteArgumentsError:
            formatter.print_error(
                "Error: Insufficient arguments in note operations. Please provide all required information.")
        except InvalidNoteIDError:
            formatter.print_error("Error: Invalid note ID. Please provide a valid note ID.")
        except InsufficientSearchCriteriaError:
            formatter.print_error("Error: Insufficient search criteria. Please provide more criteria.")
        except InvalidSearchCriteriaError:
            formatter.print_error("Error: Invalid search criteria. Please use valid search criteria.")
        except InsufficientTagArgumentsError:
            formatter.print_error(
                "Error: Insufficient arguments for adding tags. Please provide all required information.")
        except InvalidNoteOrContactIDError:
            formatter.print_error("Error: Invalid note or contact ID for tagging. Please use valid IDs.")
        except TagAdditionError:
            formatter.print_error("Error: Error during tag addition. Please try again.")
        except InsufficientTagSearchArgumentsError:
            formatter.print_error("Error: Insufficient tag search arguments. Please provide more criteria.")
        except InvalidTagError:
            formatter.print_error("Error: Invalid tags for search. Please use valid tags.")
        except TagSearchError:
            formatter.print_error("Error: Error during tag search. Please try again.")
        except InvalidDaysFormatError:
            formatter.print_error("Error: Invalid days format for upcoming birthdays. Please provide a valid format.")
        except UpcomingBirthdaysError:
            formatter.print_error("Error: Error during calculation of upcoming birthdays. Please try again.")
        except Exception as e:
            formatter.print_error(f"An unexpected error occurred: {e}")

    return inner


def input_error_handler(func):
    """
    A decorator function used to handle errors raised by the decorated function.

    It captures specific exceptions raised by the decorated function and formats error messages using an instance of OutputFormatter.

    Parameters:
    func (function): The function to be decorated.

    Returns:
    function: The inner function that handles exceptions and returns the result of the decorated function.
    """
    formatter = OutputFormatter()

    def inner(*args, **kwargs):
        """
        Inner function that executes the decorated function and handles specific exceptions.

        Parameters:
        *args: Variable length argument list for the decorated function.
        **kwargs: Arbitrary keyword arguments for the decorated function.

        Returns:
        Varies: The result of the decorated function or None if an exception is caught.
        """
        try:
            return func(*args, **kwargs)
        except IndexError:
            formatter.print_error("No command provided. Please enter a command.")
        except ValueError as e:
            formatter.print_error(f"Error in command: {e}")
        except Exception as e:
            formatter.print_error(f"An unexpected error occurred: {e}")

    return inner
