import json
import os

# Resolve path relative to this file's location so it works regardless of CWD
_HERE = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(_HERE, "..", "test_data", "user_data.json")


def read_json_file(file_path):
    """
    Reads a JSON file and returns the dictionary.
    If the file doesn't exist, raises a FileNotFoundError.
    """
    absolute_path = os.path.abspath(file_path)
    print(f"Attempting to read file from: {absolute_path}")

    if not os.path.exists(absolute_path):
        raise FileNotFoundError(f"The file '{absolute_path}' does not exist. Please check the file path.")

    with open(absolute_path, "r") as file:
        return json.load(file)


