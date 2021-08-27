
class Switch:
    name = "default_name"
    index = -1
    status = False

    def __init__(self, name: str, index: int, status: bool):
        self.name = name
        self.index = index
        self.status = status

