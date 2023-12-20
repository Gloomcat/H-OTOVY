from datetime import datetime


class Note:
    def __init__(self, number, content):
        self.number = number
        self.content = content
        self.timestamp = datetime.now()


class NotesManager:
    def __init__(self):
        self.data = {}
        self.note_counter = 1

    def add_note(self, content):
        new_note = Note(self.note_counter, content)
        self.data[self.note_counter] = new_note
        self.note_counter += 1
        return f"Note added with number {new_note.number} at {new_note.timestamp.strftime('%d.%m.%Y %H:%M:%S')[:-3]}"


if __name__ == "__main__":
    pass
