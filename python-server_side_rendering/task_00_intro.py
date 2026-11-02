#!/usr/bin/python3
"""Generate personalized invitation files from a template."""
import logging
import os

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

PLACEHOLDERS = ("name", "event_title", "event_date", "event_location")


def generate_invitations(template, attendees):
    """Create one output_X.txt file per attendee from the template.

    Args:
        template (str): text containing {name}, {event_title},
            {event_date} and {event_location} placeholders.
        attendees (list): list of dictionaries with the values to insert.
            Missing or None values are replaced with "N/A".
    """
    if not isinstance(template, str):
        logging.error(
            "Invalid input type: template must be a string, got %s.",
            type(template).__name__)
        return

    if not isinstance(attendees, list):
        logging.error(
            "Invalid input type: attendees must be a list of dictionaries, "
            "got %s.", type(attendees).__name__)
        return

    if not all(isinstance(item, dict) for item in attendees):
        logging.error(
            "Invalid input type: attendees must be a list of dictionaries.")
        return

    if not template.strip():
        logging.error("Template is empty, no output files generated.")
        return

    if not attendees:
        logging.error("No data provided, no output files generated.")
        return

    for index, attendee in enumerate(attendees, start=1):
        content = template
        for key in PLACEHOLDERS:
            value = attendee.get(key)
            if value is None:
                value = "N/A"
            content = content.replace("{" + key + "}", str(value))

        filename = "output_{}.txt".format(index)
        if os.path.exists(filename):
            logging.warning("%s already exists and will be overwritten.",
                            filename)

        try:
            with open(filename, "w") as file:
                file.write(content)
        except OSError as error:
            logging.error("Could not write %s: %s", filename, error)
