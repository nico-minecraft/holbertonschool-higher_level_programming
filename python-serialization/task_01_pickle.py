#!/usr/bin/python3
"""Custom class with pickle-based serialization."""
import pickle


class CustomObject:
    """A simple object that can be saved to and loaded from a pickle file."""

    def __init__(self, name, age, is_student):
        """Initialize the object.

        Args:
            name (str): The person's name.
            age (int): The person's age.
            is_student (bool): Whether the person is a student.
        """
        self.name = name
        self.age = age
        self.is_student = is_student

    def display(self):
        """Print the object's attributes."""
        print("Name: {}".format(self.name))
        print("Age: {}".format(self.age))
        print("Is Student: {}".format(self.is_student))

    def serialize(self, filename):
        """Serialize this instance to a file using pickle.

        Args:
            filename (str): The file to write to.

        Returns:
            None. On any error, nothing is raised.
        """
        try:
            with open(filename, "wb") as f:
                pickle.dump(self, f)
        except (OSError, pickle.PicklingError):
            return None

    @classmethod
    def deserialize(cls, filename):
        """Load an instance from a pickle file.

        Args:
            filename (str): The file to read from.

        Returns:
            CustomObject: The loaded instance, or None if the file is
            missing or malformed.
        """
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except (OSError, pickle.UnpicklingError, EOFError,
                AttributeError, ImportError, IndexError):
            return None
