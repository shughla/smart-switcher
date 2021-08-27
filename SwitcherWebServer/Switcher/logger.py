import time


class Logger:
    path = ""
    filename = "" # უნდა გადავაკეთო ეს რო ერთი path გადაეცეს მარტო

    # default path is logs/log file
    def __init__(self, path="../logs", filename="log"):
        self.path = path
        self.file_name = filename

    # appends value, which is of type str
    @classmethod
    def append(cls, value: str):
        with open(cls.path + "/" + cls.filename, 'a+') as f:
            f.write(value + "\n")  # \n might be useless

    # without extra '/'
    @classmethod
    def set_path(cls, path: str):
        cls.path = path

    # without extra '/'
    @classmethod
    def set_filename(cls, filename: str):
        cls.filename = filename

    @classmethod
    def get_path(cls) -> str:
        return cls.path

    @classmethod
    def get_file_name(cls) -> str:
        return cls.filename

    @classmethod
    def get_time(cls) -> str:
        return time.ctime() + " - "


if __name__ == '__main__':
    # ეს არის main-ისავით, მარტო მაშინ ეშვება თუ ხელით გაუშვებ, ისე არა
    logger = Logger
    print(logger.path)
    logger.append("test")
    # log_append(path + file_name)
