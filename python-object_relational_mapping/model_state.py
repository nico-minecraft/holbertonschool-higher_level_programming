#!/usr/bin/python3
"""Module that defines the State class linked to the MySQL table states.

It also creates the Base instance, which every SQLAlchemy model class of
the project inherits from. Importing the module does not connect to any
database.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class State(Base):
    """Class that maps the states table of a MySQL database.

    Attributes:
        id: auto-generated unique integer, primary key, never null.
        name: string of at most 128 characters, never null.
    """
    __tablename__ = "states"

    id = Column(Integer, primary_key=True, autoincrement=True,
                nullable=False)
    name = Column(String(128), nullable=False)
