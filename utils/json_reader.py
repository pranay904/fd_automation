import json

file_path = "test_data/user_data.json"

def read_json_file(file_path):
    """
    Reads JSON file and returns dictionary
    """
    with open(file_path, "r") as file:
        return json.load(file)
