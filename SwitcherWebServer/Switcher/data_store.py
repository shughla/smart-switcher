class DataStore:
    data_file_path = None
    comment = "//"
    # to self: ეს გაასწორე ისე რო ერთი ადგილი იყოს, 1 აღწერა და ბევრი ნომერი და მდგომარეობა
    # ახლა მეზარება ხვალ გადახედე, და ისიც შეცვალე დეფაულტ მესიჯი
    info_dict = {
        0: "ადგილი",
        1: "ნომერი",
        2: "აღწერა",
        3: "მდგომარეობა",
        4: ""
    }
    main_dict = dict() # probably something like ლოკაცია -> {

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

    def init_default_message(self) -> str:
        dict_len = len(self.info_dict)
        default_message = self.comment + " ფაილის თითო ბლოკი შედგება " + str(dict_len) + " ხაზისგან.\n"
        default_message += self.comment + " ყველა ხაზი რომელიც იწყება \"" + self.comment + "\"-ით დაიგნორდება.\n"
        for i in range(dict_len):
            default_message += self.comment + " ხაზი #" + str(i) + ": " + self.info_dict.get(i) + "\n"
        return default_message

    @classmethod
    def get_file(cls) -> dict:
        info = dict()
        with open(cls.data_file_path, "r") as f:
            line = f.readline()
            # if not cls.is_comment(line):

                # for i in range(1, len(cls.info_dict)):

        return info

    def is_comment(self, line: str) -> bool:
        return line.startswith(self.comment)


if __name__ == "__main__":
    store = DataStore()
