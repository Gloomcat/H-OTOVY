from output_formater import OutputFormatter


class _AssistantError(Exception):
    """Common base class for Assistant project errors"""
    pass


class ContactNotFoundError(_AssistantError):
    """Raised when a contact is not found."""
    pass


class InvalidFormatError(_AssistantError):
    """Raised for general invalid format errors."""
    pass


class InvalidCommandArgumentError(_AssistantError):
    """Raised for invalid command argument errors."""
    pass


class PhoneIsExistError(_AssistantError):
    """Raised when a phone number already exists."""
    pass


class InputOutputError(_AssistantError):
    """Raised for input/output errors."""
    pass


class IncorrectInputError(_AssistantError):
    """Raised for general incorrect input."""
    pass


# Add contacts
class InsufficientContactArgumentsError(_AssistantError):
    """Raised for insufficient arguments in adding contact."""
    pass


class ContactExistsError(_AssistantError):
    """Raised when a contact already exists."""
    pass


# Edit contact
class InsufficientEditContactArgumentsError(_AssistantError):
    """Raised for insufficient arguments in editing contact."""
    pass


# Delete contact
class InsufficientDeleteContactArgumentsError(_AssistantError):
    """Raised for insufficient arguments in deleting contact."""
    pass


# Upcoming birthdays
class InvalidDaysFormatError(_AssistantError):
    """Exception raised for errors due to invalid days format for upcoming birthdays."""
    pass


class UpcomingBirthdaysError(_AssistantError):
    """Exception raised for general errors during calculation of upcoming birthdays."""
    pass


class EmptyNotesError(_AssistantError):
    """Raised for empty notes list."""
    pass


class InvalidNoteOrContactIDError(_AssistantError):
    """Raised for invalid note or contact ID."""
    pass


class NoResultsFoundError(_AssistantError):
    """Exception raised for errors due to search process fail."""
    pass


class TagIsAbsentError(_AssistantError):
    """Raised for tag absense if it must be present."""
    pass


class TagIsPresentError(_AssistantError):
    """Raised for tag presense if it must be absent."""
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
        except InsufficientDeleteContactArgumentsError:
            formatter.print_error(
                "Error: Insufficient arguments in deleting contact. Please provide all required information.")
        except InvalidDaysFormatError:
            formatter.print_error("Error: Invalid days format for upcoming birthdays. Please provide a valid format.")
        except UpcomingBirthdaysError:
            formatter.print_error("Error: Error during calculation of upcoming birthdays. Please try again.")
        except (InvalidNoteOrContactIDError, EmptyNotesError, NoResultsFoundError, TagIsPresentError, TagIsAbsentError) as e:
            formatter.print_error(e)
        except Exception as e:
            formatter.print_error(f"An unexpected error occurred: {e}")
            raise e

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
            formatter.print_error(f"An unexpected input error occurred: {e}")
            raise e

    return inner
