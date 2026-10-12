#!/usr/bin/python3
"""Module that lists all State objects from the database hbtn_0e_6_usa.

It takes the MySQL username, password and database name as arguments,
connects to a MySQL server on localhost at port 3306 using SQLAlchemy,
and prints every state as "id: name" sorted by states.id in ascending
order. Nothing is executed when the module is imported.
"""
import sys
from model_state import Base, State
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

if __name__ == "__main__":
    engine = create_engine("mysql+mysqldb://{}:{}@localhost:3306/{}".format(
        sys.argv[1], sys.argv[2], sys.argv[3]), pool_pre_ping=True)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    for state in session.query(State).order_by(State.id).all():
        print("{}: {}".format(state.id, state.name))
    session.close()
