import json
import os

MEMORY_FILE = "memory.json"


def load_memory():
    """
    Load previous conversation history.
    """

    if not os.path.exists(MEMORY_FILE):
        return []

    try:
        with open(MEMORY_FILE, "r") as file:
            return json.load(file)

    except Exception:
        return []


def save_memory(messages):
    """
    Save conversation history.
    """

    with open(MEMORY_FILE, "w") as file:
        json.dump(messages, file, indent=4)