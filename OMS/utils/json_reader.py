import json
import os

# Get folder of this script
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # go up 1 level from utils/
FILE_PATH = os.path.join(BASE_DIR, "test_data", "user_data.json")

def read_json(file_path=FILE_PATH):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"JSON file not found: {file_path}")
    with open(file_path, "r") as f:
        return json.load(f)

def get_login_user():
    """Return login_user dictionary from JSON"""
    data = read_json()
    return data.get("login_user", {})
