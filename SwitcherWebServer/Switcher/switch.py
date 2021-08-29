from json import JSONEncoder
import json


class Switch:
    ERROR_CODE = -1

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4, ensure_ascii=False)

    def __init__(self, name: str, index: int, status: int):
        self.name = name
        self.index = index
        self.status = status

    @classmethod
    # if returns -1, then state was already the one that it was changed into so
    def change_status(cls, status: bool) -> int:
        if cls.status == status:
            return -1
        else:
            cls.status = status
        return 0

    @classmethod
    def change_name(cls, name: str):
        cls.name = name
