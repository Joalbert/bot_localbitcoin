import json


def file_to_json(file_location):
    with open(file_location) as json_file:
            result = json.load(json_file)
    return result