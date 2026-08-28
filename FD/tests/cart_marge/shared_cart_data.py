import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "cart_data.json"


def save(email: str, password: str, cart_count: int):
    print(f"[INFO] Saving cart data to: {DATA_FILE.resolve()}")

    data = {
        "email": email,
        "password": password,
        "cart_count": cart_count
    }

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

    print(f"[INFO] Saved shared cart data: {data}")


def load():
    print(f"[INFO] Reading cart data from: {DATA_FILE.resolve()}")

    if not DATA_FILE.exists():
        return None

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    print(f"[INFO] Loaded shared cart data: {data}")
    return data


def update_cart_count(cart_count: int):
    print(f"[INFO] Updating cart data in: {DATA_FILE.resolve()}")

    data = load()

    if not data:
        return

    data["cart_count"] = cart_count

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

    print(f"[INFO] Updated cart count in JSON: {cart_count}")