from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys

bindings = KeyBindings()


@bindings.add(Keys.Enter, eager=True)
def handle_enter(event):
    buffer = event.app.current_buffer
    if buffer.complete_state:
        buffer.complete_state = None
    else:
        buffer.validate_and_handle()


class AutoCompleter:
    def __init__(self, command_list):
        self.command_list = command_list
        self.completer = WordCompleter(command_list)
        self.session = PromptSession(completer=self.completer, key_bindings=bindings)

    def get_user_input(self, prompt_message=''):
        return self.session.prompt(prompt_message)
