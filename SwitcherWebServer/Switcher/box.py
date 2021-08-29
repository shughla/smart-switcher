from SwitcherWebServer.Switcher.switch import Switch
from json import JSONEncoder
import json


class Box:
    switch_array = []

    def __init__(self, description: str, switch_array=None):
        self.description = description
        if switch_array is not None:
            self.switch_array = switch_array
        else:
            self.switch_array = []

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4, ensure_ascii=False)

    @classmethod
    def get_switches(cls):
        return cls.switch_array

    @classmethod
    def update_switches(cls, switch_array: list[Switch]):
        cls.switch_array = switch_array

    @classmethod
    def change_status(cls, index: int, status: bool) -> list[Switch]:
        switch = cls.switch_array[index]
        val = switch.change_status(status)
        if val == Switch.ERROR_CODE:
            return list()  # empty list
        return cls.switch_array
