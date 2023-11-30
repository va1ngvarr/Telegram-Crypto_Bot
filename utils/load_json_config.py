import json


def load_json_config(path_to_file="bot/text-values-config.json"):
    with open(path_to_file, "r") as json_file:
        data = json.load(json_file)

    return data
