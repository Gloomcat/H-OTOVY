from datetime import datetime
from collections import UserDict

from fields import FieldError, Id
from storage import PersistantStorage


class Note(UserDict):
    """
    A class representing a note, storing its id, timestamp, and content.

    Inherits from UserDict for dictionary-like access to note data.

    Attributes:
        data (dict): A dictionary to store the note's information.
    """

    def __init__(self, id: int, timestamp: str, content: str):
        """
        Initializes a new Note instance.

        Parameters:
        id (int): The unique identifier for the note.
        timestamp (str): The timestamp of when the note was created.
        content (str): The content of the note.
        """
        super().__init__()
        self.data["id"] = None
        self.data["timestamp"] = None
        self.data["content"] = None
        self.id = id
        self.timestamp = timestamp
        self.content = content

    @property
    def id(self):
        """
        Gets the unique identifier of the note.
        """
        return self.data["id"]

    @id.setter
    def id(self, id: int):
        """
        Sets the unique identifier of the note.

        Parameters:
        id (int): The unique identifier to be set.
        """
        try:
            self.data["id"] = Id(id)
        except FieldError as e:
            raise e

    @property
    def timestamp(self):
        """
        Gets the timestamp of the note.
        """
        return self.data["timestamp"]

    @timestamp.setter
    def timestamp(self, timestamp: str):
        """
        Sets the timestamp of the note.

        Parameters:
        timestamp (str): The timestamp to be set.
        """
        self.data["timestamp"] = timestamp

    @property
    def content(self):
        """
        Gets the content of the note.
        """
        return self.data["content"]

    @content.setter
    def content(self, content: str):
        """
        Sets the content of the note.

        Parameters:
        content (str): The content to be set.
        """
        self.data["content"] = content


class NotesManager(PersistantStorage):
    """
    A class for managing a collection of notes.

    Inherits from PersistentStorage for CSV file operations.

    Attributes:
        data (list): A list to store the note records.
    """

    def __init__(self):
        """
        Initializes a new NotesManager instance with specified column headers and note type.
        """
        super().__init__("notes.csv", ["id", "timestamp", "content"], Note)

    @PersistantStorage.update
    def add_note(self, content: str):
        """
        Adds a new note to the notes manager.

        Parameters:
        content (str): The content of the note to be added.

        Returns:
        str: A message indicating the success or failure of the operation.
        """
        if not content:
            return "Error: Can't add empty note."
        id = len(self.data)
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        note = Note(id, timestamp, content)
        self.data.append(note)
        return f"Note added with Id: {id} at {note.timestamp}"

    def find_notes(self, keyword: str):
        """
        Finds notes containing the specified keyword.

        Parameters:
        keyword (str): The keyword to search for in the notes.

        Returns:
        list: A list of notes that contain the keyword.
        """
        result = list(
            filter(lambda note: keyword.lower()
                   in note.content.lower(), self.data)
        )
        # raise according Error from error_handler.py in case the result is empty
        return result


if __name__ == "__main__":
    pass
