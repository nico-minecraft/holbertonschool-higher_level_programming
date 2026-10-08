#!/usr/bin/python3
"""Convert CSV data to JSON format."""
import csv
import json


def convert_csv_to_json(csv_filename):
    """Convert a CSV file to JSON and write it to data.json.

    Args:
        csv_filename (str): Path of the CSV file to read.

    Returns:
        bool: True if the conversion succeeded, False otherwise
        (for example, if the file does not exist).
    """
    try:
        with open(csv_filename, "r", newline="", encoding="utf-8") as f:
            data = list(csv.DictReader(f))

        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data, f)
        return True
    except (OSError, csv.Error, UnicodeDecodeError):
        return False
