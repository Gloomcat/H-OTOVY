import csv
from collections import UserList
from pathlib import Path


class PersistantStorage(UserList):
    def __init__(self, filename: str, fields: list[str], load_type):
        super().__init__()
        self.filename = filename
        self.fields = fields
        self.load_type = load_type
        self.__dict_file_handle = None

    def __open_file(self, modes: str):
        data_dir = Path(__file__).resolve().parent / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        file_path = data_dir / self.filename
        return open(file_path, modes)

    def __enter__(self):
        try:
            self.__dict_file_handle = self.__open_file("r+")
            self.__csv_processor = csv.DictReader(self.__dict_file_handle)
            for row in self.__csv_processor:
                self.data.append(self.load_type(*(row[field] for field in self.fields)))

        except FileNotFoundError:
            self.__dict_file_handle = self.__open_file("w")
        return self

    def __exit__(self, *_):
        # For now we ignore possible errors on this step
        self.__dict_file_handle.close()

    def update(data_change_func):
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
