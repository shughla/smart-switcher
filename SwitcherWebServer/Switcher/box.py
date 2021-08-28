from SwitcherWebServer.Switcher.switch import Switch


class Box:
    description = "default description"
    switch_array = []  # type:list[Switch]

    def __init__(self, description: str, switch_array: list[Switch]):
        self.description = description
        self.switch_array = switch_array

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
