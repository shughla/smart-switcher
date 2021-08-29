import json


from SwitcherWebServer.Switcher.switch import Switch
from SwitcherWebServer.Switcher.box import Box


class DataStore:
    main_data = list() # type: list[Box]
    DEFAULT_FILE_PATH = "Data/data.json"

    # this needs ../data to exist
    def __init__(self, data_file_path=DEFAULT_FILE_PATH):
        self.data_file_path = data_file_path
        try:
            self.deserialize_json(data_file_path)  # sets main data
        except FileNotFoundError:
            # empty dictionary
            print("File with name: \"" + data_file_path + "\" doesn't exist.")

    @classmethod
    def deserialize_json(cls, data_file_path=DEFAULT_FILE_PATH):
        with open(data_file_path,"r") as f:
            if f.readline().strip(" \n") == "":
                return
        with open(data_file_path, "r") as f:
            data = json.load(f)
            cls.convert_to_boxes(data)


    @classmethod
    def get_switches(cls, box_index):
        return cls.main_data[box_index].switch_array

    @classmethod
    def convert_to_boxes(cls, data: str):
        main_data = list()
        data = json.loads(data)
        data = data["boxes"]
        for box in data:
            for element in box:
                if element == "description":
                    main_data.append(Box(box[element]))
                elif element == "switch_array":
                    for switch in box[element]:
                        switch = Switch(switch["name"], switch["index"], switch["status"])
                        main_data[-1].switch_array.append(switch)
        cls.main_data = main_data

    @classmethod
    def serialize_json(cls, boxes: list[Box], data_file_path=DEFAULT_FILE_PATH):
        with open(data_file_path, "w", encoding='utf8') as f:
            json_string = "{ \"boxes\": ["
            for box in boxes:
                json_string += box.toJSON()
                if boxes[-1] is not box:
                    json_string += ","
            json_string += "]}"
            json.dump(json_string, f, ensure_ascii=False)

    @classmethod
    def update_data(cls, data: list[Box], data_file_path=DEFAULT_FILE_PATH):
        cls.serialize_json(data, data_file_path)


if __name__ == "__main__":
    store = DataStore()
