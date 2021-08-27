class DataStore:
    data_file_path = None

    info_dict = {
        0: "ადგილი",
        1: "ნომერი",
        2: "აღწერა",
        3: "მდგომარეობა",
        4: ""
    }
    main_dict = dict("სართული 1", {1,0,0,1,1,1,0}) # probably something like ლოკაცია -> {სვიჩი-1, სვიჩი-2, სვიჩი-3}

    # this needs ../data to exist
    def __init__(self, data_file_path="../Data/data.txt"):
        self.data_file_path = data_file_path
        default_message = self.init_default_message()
        try:
            f = open(data_file_path, "r+")
        except FileNotFoundError:
            f = open(data_file_path, "w")
            f.write(default_message)
        else:
            f.close()


    @classmethod
    def get_file(cls) -> dict:

        return info

    def is_comment(self, line: str) -> bool:
        return line.startswith(self.comment)


if __name__ == "__main__":
    store = DataStore()
