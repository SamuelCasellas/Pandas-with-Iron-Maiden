import json

path = "json-practice.json"

some_dict = {
    "a":"b",
    "c": "d"
}

with open(path, mode="w") as file_w:
    json.dump(some_dict, file_w)
