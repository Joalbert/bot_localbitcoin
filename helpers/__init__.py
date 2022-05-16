import json


def file_to_json(file_location):
    try:
        json_file = open(file_location)
    except FileNotFoundError:
        return None
    except Exception:
        json_file.close()
        return None
    else:
        result = json.load(json_file)
        json_file.close()
        return result