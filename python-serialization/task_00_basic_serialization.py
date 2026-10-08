#!/usr/bin/python3
"""Basic serialization module: save a dict to JSON and load it back."""
import json


def serialize_and_save_to_file(data, filename):
    """Serialize a Python dictionary to a JSON file.

    Args:
        data (dict): The dictionary to serialize.
        filename (str): Output JSON file. Replaced if it already exists.
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f)


def load_and_deserialize(filename):
    """Load a JSON file and return its contents as a Python dictionary.

    Args:
        filename (str): The JSON file to read.

    Returns:
        dict: The deserialized data.
    """
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)
