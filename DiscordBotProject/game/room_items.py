import json
from pathlib import Path

from game.map import ROOMS

room_items = {
    room_id: []
    for room_id in ROOMS
}

ROOM_ITEMS_FILE = Path(__file__).resolve().parent.parent / "data" / "room_items.json"


def save_room_items():
    ROOM_ITEMS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with ROOM_ITEMS_FILE.open("w", encoding="utf-8") as file:
        json.dump(room_items, file, indent=4)


def load_room_items():
    if not ROOM_ITEMS_FILE.exists():
        save_room_items()
        return

    try:
        with ROOM_ITEMS_FILE.open("r", encoding="utf-8") as file:
            saved_room_items = json.load(file)
    except (json.JSONDecodeError, OSError) as error:
        print(f"Couldn't load room items: {error}")
        return

    if not isinstance(saved_room_items, dict):
        print("Couldn't load room items: the save file must contain an object.")
        return

    for room_id, items in saved_room_items.items():
        if room_id in room_items and isinstance(items, list):
            room_items[room_id] = [
                item
                for item in items
                if isinstance(item, dict) and isinstance(item.get("id"), str)
            ]
