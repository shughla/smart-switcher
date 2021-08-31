import datetime


class Logger:
    filepath = "SwitcherWebServer/logs/log"

    # default path is logs/log file
    def __init__(self, filepath=None):
        if filepath is not None:
            self.filepath = filepath

    # appends value, which is of type str
    @classmethod
    def append(cls, value: str):
        with open(cls.filepath, 'a+') as f:
            f.write(value + "\n")  # \n might be useless

    @classmethod
    def set_filepath(cls, filepath: str):
        cls.filepath = filepath

    @classmethod
    def get_filepath(cls) -> str:
        return cls.filepath

    @classmethod
    def get_time(cls) -> str:
        t = datetime.datetime.now()
        return t.strftime("[%d.%m.%y] Time: %H:%M:%S") + " - "


if __name__ == '__main__':
    # ეს არის main-ისავით, მარტო მაშინ ეშვება თუ ხელით გაუშვებ, ისე არა
    logger = Logger
    logger.append("test")
    # log_append(path + file_name)
