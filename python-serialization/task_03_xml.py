#!/usr/bin/python3
"""Serialize and deserialize a Python dictionary using XML."""
import xml.etree.ElementTree as ET


def serialize_to_xml(dictionary, filename):
    """Serialize a dictionary to an XML file.

    Args:
        dictionary (dict): The data to serialize.
        filename (str): The XML file to write.

    Returns:
        bool: True on success, False if the file could not be written.
    """
    root = ET.Element("data")
    for key, value in dictionary.items():
        child = ET.SubElement(root, str(key))
        child.text = str(value)

    try:
        ET.ElementTree(root).write(filename, encoding="utf-8",
                                   xml_declaration=True)
        return True
    except OSError:
        return False


def deserialize_from_xml(filename):
    """Read an XML file and rebuild the dictionary.

    Args:
        filename (str): The XML file to read.

    Returns:
        dict: The deserialized data, or None if the file is missing or
        malformed.
    """
    try:
        root = ET.parse(filename).getroot()
    except (OSError, ET.ParseError):
        return None

    return {child.tag: child.text for child in root}
