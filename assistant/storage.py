import csv
from collections import UserList
from pathlib import Path


class PersistantStorage(UserList):
    """
    A class for persistent storage of data in a CSV file format.

    This class manages reading from and writing to a CSV file to ensure data persistence across sessions. It uses UserList for easy manipulation of data as a list.

    Attributes:
        filename (str): The name of the file where data is stored.
        fields (list[str]): The fields (columns) in the CSV file.
        load_type (type): The type to which the loaded data will be converted.
        __dict_file_handle: Internal handle for the opened file.
    """

    def __init__(self, filename: str, fields: list[str], load_type):
        """
        Initializes a new PersistentStorage instance.

        Parameters:
        filename (str): The name of the file to use for storing data.
        fields (list[str]): A list of strings representing the fields in the CSV file.
        load_type (type): The type of object to be created for each row in the CSV file.
        """
        super().__init__()
        self.filename = filename
        self.fields = fields
        self.load_type = load_type
        self.__dict_file_handle = None

    def __open_file(self, modes: str):
        """
        Opens the file with the specified mode.

        Parameters:
        modes (str): The file opening mode (e.g., 'r+', 'w').

        Returns:
        file: The file object opened in the specified mode.
        """
        data_dir = Path.home().resolve() / ".assistant"
        data_dir.mkdir(parents=True, exist_ok=True)
        file_path = data_dir / self.filename
        return open(file_path, modes)

    def __enter__(self):
        """
        Enters the runtime context related to this object.

        Opens the file for reading and writing, and loads existing data into the list.

        Returns:
        PersistentStorage: The instance itself.
        """
        try:
            self.__dict_file_handle = self.__open_file("r+")
            self.__csv_processor = csv.DictReader(self.__dict_file_handle)
            for row in self.__csv_processor:
                self.data.append(self.load_type(*(row[field] for field in self.fields)))

        except FileNotFoundError:
            self.__dict_file_handle = self.__open_file("w")
        return self

    def __exit__(self, *_):
        """
        Exits the runtime context related to this object.

        Closes the file handle opened for reading and writing.
        """
        # For now we ignore possible errors on this step
        self.__dict_file_handle.close()

    def update(data_change_func):
        """
        A decorator for updating the CSV file after a data change.

        This decorator ensures that any changes made to the data are reflected in the CSV file.

        Parameters:
        data_change_func (function): The function that changes the data.
        """

        def wrapper(self, *args):
            result = data_change_func(self, *args)
            if self.__dict_file_handle and self.data:
                self.__dict_file_handle.truncate(0)
                self.__dict_file_handle.seek(0)
                self.__csv_processor = csv.DictWriter(
                    self.__dict_file_handle, fieldnames=self.fields
                )
                self.__csv_processor.writeheader()
                for element in self.data:
                    self.__csv_processor.writerow(element.data)
            return result

        return wrapper


if __name__ == "__main__":
    pass
