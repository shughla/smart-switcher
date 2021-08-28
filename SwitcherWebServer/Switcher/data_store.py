import json

from SwitcherWebServer.Switcher.switch import Switch
from SwitcherWebServer.Switcher.box import Box


class DataStore:
    DEFAULT_FILE_PATH = "../Data/data.json"
    data_file_path = None
    # probably something like ლოკაცია -> {სვიჩი-1, სვიჩი-2, სვიჩი-3}
    main_data = dict()  # type: dict[str : list[Switch]]

    # this needs ../data to exist
    def __init__(self, data_file_path=DEFAULT_FILE_PATH):
        self.data_file_path = data_file_path
        try:
            self.deserialize_json(data_file_path)
        except FileNotFoundError:
            # empty dictionary
            self.main_data = dict()  # type: dict[str : list[Switch]]
            raise Exception("File with name: \"" + data_file_path + "\" doesn't exist.")

    @classmethod
    def deserialize_json(cls, data_file_path=DEFAULT_FILE_PATH):
        with open(data_file_path, "r") as f:
            cls.main_data = json.load(f)

    @classmethod
    def serialize_json(cls, obj=None, data_file_path=DEFAULT_FILE_PATH):
        if obj is None:
            obj = cls.main_data
        with open(data_file_path, "w") as f:
            json.dump(obj, f)

    @classmethod
    def update_data(cls, data: dict[str, list[Switch]], data_file_path=DEFAULT_FILE_PATH):
        cls.serialize_json(data, data_file_path)


if __name__ == "__main__":
    store = DataStore()
