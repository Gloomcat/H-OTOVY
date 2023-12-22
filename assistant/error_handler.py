from output_formater import OutputFormatter


class KeyboardInputError(Exception):
    """
    Exception raised for special keyboard shortcuts during user input.
    """

    pass


class _AssistantError(Exception):
    """Common base class for Assistant project errors"""

    pass


class FieldValidationError(_AssistantError):
    """
    Exception raised for errors during the validation of Field input.
    """

    pass


class EmailIsExistError(_AssistantError):
    """Raised when a contact with the email already exists."""

    pass


class NameIsExistError(_AssistantError):
    """Raised when a contact with the name already exists."""

    pass


class PhoneIsExistError(_AssistantError):
    """Raised when a phone number already exists."""

    pass


class EmptyContactsError(_AssistantError):
    """Raised for empty contacts list."""

    pass


class InvalidBirthdayDaysParameter(_AssistantError):
    """Raised invalid days parameter in show birthdays processing."""

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
        except _AssistantError as e:
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
