from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys


class AutoCompleter:
    """
    A class to facilitate auto-completion in a command-line interface, with custom key bindings.

    This class sets up a prompt session with auto-completion for a list of commands and custom key bindings.

    Attributes:
        command_list (list): A list of commands for auto-completion.
        completer (WordCompleter): The completer instance for handling auto-completion.
        session (PromptSession): The prompt session with attached completer and key bindings.
        bindings (KeyBindings): Key bindings for the prompt session.
    """

    def __init__(self, command_list):
        """
        Initializes the AutoCompleter with a list of commands.

        Parameters:
        command_list (list): A list of commands to be used for auto-completion.
        """
        self.command_list = command_list
        self.completer = WordCompleter(command_list)
        self.bindings = self._setup_key_bindings()
        self.session = PromptSession(completer=self.completer, key_bindings=self.bindings)

    def _setup_key_bindings(self):
        """
        Sets up custom key bindings for the prompt session.

        Returns:
        KeyBindings: The configured key bindings.
        """
        bindings = KeyBindings()

        @bindings.add(Keys.Enter, eager=True)
        def handle_enter(event):
            """
            Handles the Enter key press in the prompt.

            This function determines whether to complete the current input or to process it.

            Parameters:
            event: The event that triggered this handler.
            """
            buffer = event.app.current_buffer
            if buffer.complete_state:
                # Clear the completion state if it exists
                buffer.complete_state = None
            else:
                # Otherwise, validate and handle the input
                buffer.validate_and_handle()

        return bindings

    def get_user_input(self, prompt_message=''):
        """
        Gets user input from the prompt with auto-completion.

        Parameters:
        prompt_message (str): The message to display on the prompt.

        Returns:
        str: The user input from the prompt.
        """
        return self.session.prompt(prompt_message)
