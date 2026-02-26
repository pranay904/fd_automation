import json
import os

file_path = "FD/test_data/user_data.json"


def read_json_file(file_path):
    """
    Reads a JSON file and returns the dictionary.
    If the file doesn't exist, raises a FileNotFoundError.
    """
    # Get the absolute path for better debugging
    absolute_path = os.path.abspath(file_path)
    print(f"Attempting to read file from: {absolute_path}")

    # Check if the file exists before opening
    if not os.path.exists(absolute_path):
        raise FileNotFoundError(f"The file '{absolute_path}' does not exist. Please check the file path.")

    with open(absolute_path, "r") as file:
        return json.load(file)


