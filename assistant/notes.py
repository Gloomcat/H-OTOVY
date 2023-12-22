from datetime import datetime
from collections import UserDict

from fields import Id
from storage import PersistantStorage
from error_handler import (
    InvalidNoteOrContactIDError,
    EmptyNotesError,
    NoResultsFoundError,
    TagIsPresentError,
    TagIsAbsentError,
    FieldValidationError,
    EmptyNoteError
)


class Note(UserDict):
    """
    A class representing a note, storing its id, timestamp, and content.

    Inherits from UserDict for dictionary-like access to note data.

    Attributes:
        data (dict): A dictionary to store the note's information.
    """

    def __init__(self, id: int, timestamp: str, content: str, tags=""):
        """
        Initializes a new Note instance.

        Parameters:
        id (int): The unique identifier for the note.
        timestamp (str): The timestamp of when the note was created.
        content (str): The content of the note.
        tags (str if loaded from storage else list[str]): The content of the note tags.
        """
        super().__init__()
        self.data["id"] = None
        self.data["timestamp"] = None
        self.data["content"] = None
        self.data["tags"] = None
        self.id = id
        self.timestamp = timestamp
        self.content = content
        self.tags = tags

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
        except FieldValidationError as e:
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

    @property
    def tags(self):
        """
        Gets the content of the note tags.
        """
        if not self.data["tags"]:
            return []
        return self.data["tags"].split(",")

    @tags.setter
    def tags(self, tags):
        """
        Sets the content of the note tags.

        Parameters:
        tags (str if loaded from storage else list[str]): The content to be set.
        """
        if isinstance(tags, str):
            self.data["tags"] = tags
            return
        self.data["tags"] = ",".join(tags)


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
        super().__init__("notes.csv", ["id", "timestamp", "content", "tags"], Note)

    def _get_available_ids(self):
        """
        Get the available note IDs.

        Returns:
        tuple: A tuple containing the available note IDs.
        """
        if not self.data:
            return ()
        return tuple(range(0, len(self.data)))

    def _update_ids(self):
        """
        Update the IDs of all notes in the storage to match their current positions.

        This function is typically called after notes have been added or deleted, ensuring
        that the IDs of the remaining notes reflect their sequential order in the storage.

        Returns:
        None
        """
        for id in range(len(self.data)):
            self.data[id].id = id

    def _check_note_ids(self, id: int = None):
        """
        Check if the provided note ID is valid.

        Parameters:
        - id (int): The note ID to be checked. Defaults to None.

        Raises:
        - EmptyNotesError: If the notes list is empty.
        - InvalidNoteOrContactIDError: If the provided note ID is invalid.
        """
        ids = self._get_available_ids()
        if not ids:
            raise EmptyNotesError("Error: Notes list is empty.")
        if id and id not in ids:
            error_msg = f"Error: Invalid note Id. Possible Ids: 0."
            if len(ids) > 1:
                error_msg = error_msg[:-1] + f"-{len(ids)-1}"
            raise InvalidNoteOrContactIDError(error_msg)

    def _check_empty_result(self, content: list):
        """
        Check if the search result is empty.

        Parameters:
        - content (list): The content to be checked.

        Raises:
        - NoResultsFoundError: If the content is empty.
        """
        if not content or content == []:
            raise NoResultsFoundError("Error: No notes found during search.")

    def _check_empty_content(self, content: str):
        """
        Check if the note contents are empty.

        Parameters:
        - content (str): The contents to be checked.

        Raises:
        - EmptyNoteError: If the note contents are empty.
        """
        if not content or content == "":
            raise EmptyNoteError("Error: Contents should not be empty.")

    def _check_tag_exists(self, id: str, tag: str, must_exist: bool):
        """
        Check if a tag exists for a given note ID.

        Parameters:
        - id (str): The note ID.
        - tag (str): The tag to be checked.
        - must_exist (bool): If True, check if the tag must exist; if False, check if the tag must not exist.

        Raises:
        - EmptyNotesError: If the notes list is empty.
        - TagIsAbsentError: If the tag is absent and must exist.
        - TagIsPresentError: If the tag is present and must not exist.
        """
        id = Id(id).value
        self._check_note_ids(id)
        tags = self.data[id].tags
        if must_exist:
            if tag not in tags:
                raise TagIsAbsentError(
                    f"Error: Tag '{tag}' is not present in the note with Id: {id}. Tags are case-sensitive."
                )
        elif tag in tags:
            raise TagIsPresentError(
                f"Error: Tag '{tag}' is already added to the note with Id: {id}."
            )

    @PersistantStorage.update
    def add_note(self, content: str):
        """
        Add a new note with the provided content.

        Parameters:
        - content (str): The content of the new note.

        Raises:
        - EmptyNoteError: If the note is empty.

        Returns:
        str: A message indicating the success of adding the note.
        """
        self._check_empty_content(content)
        id = len(self.data)
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        note = Note(id, timestamp, content)
        self.data.append(note)
        return f"Note added with Id: {id} at {note.timestamp}"

    def find_notes(self, keyword: str):
        """
        Find notes containing the specified keyword in their content.

        Parameters:
        - keyword (str): The keyword to search for.

        Raises:
        - NoResultsFoundError: If no notes are found with the specified keyword.

        Returns:
        list: A list of notes containing the specified keyword.
        """
        self._check_empty_content(keyword)
        result = list(
            filter(lambda note: keyword.lower() in note.content.lower(), self.data)
        )
        self._check_empty_result(result)
        return result

    def show_notes(self):
        """
        Show all notes.

        Raises:
        - EmptyNotesError: If the notes list is empty.

        Returns:
        list: A list containing all notes.
        """
        self._check_note_ids()
        return self.data

    @PersistantStorage.update
    def edit_note(self, id: str, new_content: str):
        """
        Edit the content of a note with the given ID.

        Parameters:
        - id (str): The unique identifier of the note to be edited.
        - new_content (str): The new content to replace the existing content of the note.

        Raises:
        - InvalidNoteOrContactIDError: If the provided note ID is invalid.

        Returns:
        str: A message indicating the success of the edit, including the new version's timestamp and content.
        """
        id = Id(id).value
        self._check_note_ids(id)
        current_note = self.data[id]
        current_note.content = new_content
        current_note.timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        return f"Note edited. New version: {current_note.timestamp}: {current_note.content}"

    @PersistantStorage.update
    def delete_note(self, id: str):
        """
        Delete a note with the given ID from the storage.

        Parameters:
        - id (str): The unique identifier of the note to be deleted.

        Raises:
        - InvalidNoteOrContactIDError: If the provided note ID is not found in the storage.

        Returns:
        str: A message indicating the success of the deletion.
        """
        id = Id(id).value
        self._check_note_ids(id)
        self.data.pop(id)
        self._update_ids()
        return f"Note with Id {id} deleted successfully."

    @PersistantStorage.update
    def add_note_tag(self, id: str, tag: str):
        """
        Add a tag to the note with the given ID.

        Parameters:
        - id (str): The unique identifier of the note.
        - tag (str): The tag to be added.

        Raises:
        - InvalidNoteOrContactIDError: If the provided note ID is not found in the storage.
        - TagIsPresentError: If the tag already exists for the note.

        Returns:
        str: A message indicating the success of adding the tag.
        """
        id = Id(id).value
        self._check_note_ids(id)
        self._check_tag_exists(id, tag, False)
        tags = self.data[id].tags
        tags.append(tag)
        self.data[id].tags = tags
        return f"Tag '{tag}' added to the note with Id: {id}"

    @PersistantStorage.update
    def delete_note_tag(self, id: str, tag: str):
        """
        Delete a tag from the note with the given ID.

        Parameters:
        - id (str): The unique identifier of the note.
        - tag (str): The tag to be deleted.

        Raises:
        - InvalidNoteOrContactIDError: If the provided note ID is not found in the storage.
        - TagIsAbsentError: If the tag does not exist for the note.

        Returns:
        str: A message indicating the success of deleting the tag.
        """
        id = Id(id).value
        self._check_note_ids(id)
        self._check_tag_exists(id, tag, True)
        tags = self.data[id].tags
        tags.remove(tag)
        self.data[id].tags = tags
        return f"Tag '{tag}' deleted from the note with Id: {id}"

    @PersistantStorage.update
    def edit_note_tag(self, id: str, tag: str, new_tag: str):
        """
        Edit a tag for the note with the given ID.

        Parameters:
        - id (str): The unique identifier of the note.
        - tag (str): The existing tag to be replaced.
        - new_tag (str): The new tag to replace the existing tag.

        Raises:
        - InvalidNoteOrContactIDError: If the provided note ID is not found in the storage.
        - TagIsAbsentError: If the existing tag does not exist for the note.

        Returns:
        str: A message indicating the success of editing the tag.
        """
        id = Id(id).value
        self._check_note_ids(id)
        self._check_tag_exists(id, tag, True)
        tags = self.data[id].tags
        tags.remove(tag)
        tags.append(new_tag)
        self.data[id].tags = tags
        return f"Tag '{tag}' replaced by '{new_tag}' in the note with Id: {id}"

    def find_notes_by_tag(self, tag: str):
        """
        Find notes that have the specified tag.

        Parameters:
        - tag (str): The tag to search for.

        Raises:
        - NoResultsFoundError: If no notes are found with the specified tag.

        Returns:
        list: A list of notes that have the specified tag.
        """
        result = []
        for note in self.data:
            for t in note.tags:
                if tag == t:
                    result.append(note)
        self._check_empty_result(result)
        return result

    # TODO:
    def sort_notes_by_tags_order(self, tags_order: list[str]):
        # {
        #     "command": "sort-notes-by-tag-order",
        #     "arguments": "<list-of-some-tags>",
        #     "description": "Sorts notebook contents by tag order provided (ex. [Reminder, Favourite]).\nFor each tag present in the note, it will be closer to start of notebook contents.",
        # },
        # tag1, tag2, tag3
        # tag1, tag2,
        # tag1, tag3
        # tag2, tag3
        # tag1
        # tag2
        # tag3
        pass
