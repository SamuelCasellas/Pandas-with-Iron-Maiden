import json

class JsonService:
    def __init__(self, file_path):
        self._file_path = file_path

    def write_dict_to_json(self, dict):
        with open(self._file_path, mode="w") as write_json:
            json.dump(dict, write_json)

    def read_json_as_dict(self):
        with open(self._file_path, mode="r") as read_json:
            return json.load(read_json)
