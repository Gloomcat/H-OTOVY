from datetime import datetime
from collections import UserDict

from assistant.fields import FieldError, Id
from assistant.storage import PersistantStorage


class Note(UserDict):
    def __init__(self, id: int, timestamp: str, content: str):
        super().__init__()
        self.data["id"] = None
        self.data["timestamp"] = None
        self.data["content"] = None
        self.id = id
        self.timestamp = timestamp
        self.content = content

    @property
    def id(self):
        return self.data["id"]

    @id.setter
    def id(self, id: int):
        try:
            self.data["id"] = Id(id)
        except FieldError as e:
            raise e

    @property
    def timestamp(self):
        return self.data["timestamp"]

    @timestamp.setter
    def timestamp(self, timestamp: str):
        self.data["timestamp"] = timestamp

    @property
    def content(self):
        return self.data["content"]

    @content.setter
    def content(self, content: str):
        self.data["content"] = content


class NotesManager(PersistantStorage):
    def __init__(self):
        super().__init__("notes.csv", ["id", "timestamp", "content"], Note)

    @PersistantStorage.update
    def add_note(self, content: str):
        if not content:
            return "Error: Can't add empty note."
        id = len(self.data)
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        note = Note(id, timestamp, content)
        self.data.append(note)
        return f"Note added with Id: {id} at {note.timestamp}"

    def find_notes(self, keyword: str):
        result = list(
            filter(lambda note: keyword.lower()
                   in note.content.lower(), self.data)
        )
        # raise according Error from error_handler.py in case the result is empty
        return result


if __name__ == "__main__":
    pass
