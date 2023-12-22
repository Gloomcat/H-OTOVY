from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, WordCompleter, Completion
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.document import Document


class SpaceAwareCompleter(Completer):
    """
    A custom completer that disables completion after a space is entered.

    Attributes:
        word_completer (Completer): The underlying completer used for suggestions before a space is entered.
    """

    def __init__(self, word_completer):
        """
        Initializes the SpaceAwareCompleter with a given word completer.

        Parameters:
            word_completer (Completer): The completer to use for providing suggestions.
        """
        self.word_completer = word_completer

    def get_completions(self, document, complete_event):
        """
        Overrides the get_completions method to provide completions.

        This method checks if a space is present in the input, and if so, it stops providing completions.

        Parameters:
            document (Document): The current document/input where completion is being performed.
            complete_event (CompleteEvent): The completion event triggering this method.
        """
        if ' ' in document.text_before_cursor:
            return
        yield from self.word_completer.get_completions(document, complete_event)


class AutoCompleter:
    """
    A class to facilitate auto-completion in a command-line interface with custom behavior.

    This class sets up a prompt session with a custom completer that stops suggesting completions
    after a space is entered, along with custom key bindings.

    Attributes:
        command_list (list): A list of commands for auto-completion.
        custom_completer (SpaceAwareCompleter): The custom completer instance.
        session (PromptSession): The prompt session with attached completer and key bindings.
        bindings (KeyBindings): Custom key bindings for the prompt session.
    """

    def __init__(self, command_list):
        """
        Initializes the AutoCompleter with a list of commands.

        Parameters:
            command_list (list): A list of commands to be used for auto-completion.
        """
        self.command_list = command_list
        word_completer = WordCompleter(command_list, ignore_case=True)
        self.custom_completer = SpaceAwareCompleter(word_completer)
        self.bindings = self._setup_key_bindings()
        self.session = PromptSession(completer=self.custom_completer, key_bindings=self.bindings)

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

            This function determines whether to process the input or to clear the completion state.

            Parameters:
                event: The event that triggered this handler.
            """
            buffer = event.app.current_buffer
            if buffer.complete_state:
                buffer.complete_state = None
            else:
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
