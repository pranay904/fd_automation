import os
import yaml

def load_yaml(path):
    """
    Load a YAML file with a path relative to the project root.
    """
    # Determine project root (assumes this file is in utils/)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(project_root, path)

    if not os.path.exists(full_path):
        raise FileNotFoundError(f"YAML file not found: {full_path}")

    with open(full_path, encoding="utf-8") as f:
        return yaml.safe_load(f)
