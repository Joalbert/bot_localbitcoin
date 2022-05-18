import json


def file_to_json(file_location):
    try:
        with open(file_location) as json_file:
            result = json.load(json_file)
    except FileNotFoundError:
        return None
    except Exception:
        return None
    else:
        return result