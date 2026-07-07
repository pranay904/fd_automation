import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "cart_data.json"


def save(email: str, password: str, cart_count: int):
    data = {
        "email": email,
        "password": password,
        "cart_count": cart_count
    }

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

    print(f"[INFO] Saved shared cart data: {data}")


def load():
    if not DATA_FILE.exists():
        return None

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    print(f"[INFO] Loaded shared cart data: {data}")
    return data


def update_cart_count(cart_count: int):
    data = load()

    if not data:
        return

    data["cart_count"] = cart_count

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

    print(f"[INFO] Updated cart count in JSON: {cart_count}")