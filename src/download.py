class Download:
    def __init__(self, download):
        self.__source_path = download["source_path"]
        self.__destination_path = download["destination_path"]
        self.__diff_files_destination_path = download["diff_files_destination_path"]
        self.__flags = download["flags"]
        self.__days = download["days"]

    @property
    def source_path(self):
        return self.__source_path

    @property
    def destination_path(self):
        return self.__destination_path

    @property
    def diff_files_destination_path(self):
        return self.__diff_files_destination_path

    @property
    def flags(self):
        return self.__flags

    @property
    def days(self):
        return self.__days
