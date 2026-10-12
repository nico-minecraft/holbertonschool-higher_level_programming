#!/usr/bin/python3
"""Module that defines the City class linked to the MySQL table cities.

The City class inherits from the Base instance defined in model_state.
Importing the module does not connect to any database.
"""
from model_state import Base
from sqlalchemy import Column, ForeignKey, Integer, String


class City(Base):
    """Class that maps the cities table of a MySQL database.

    Attributes:
        id: auto-generated unique integer, primary key, never null.
        name: string of at most 128 characters, never null.
        state_id: integer foreign key to states.id, never null.
    """
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, autoincrement=True,
                nullable=False)
    name = Column(String(128), nullable=False)
    state_id = Column(Integer, ForeignKey("states.id"), nullable=False)
