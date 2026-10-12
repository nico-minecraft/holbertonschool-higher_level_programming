#!/usr/bin/python3
"""Module that deletes all State objects containing the letter a.

It takes the MySQL username, password and database name as arguments,
connects to a MySQL server on localhost at port 3306 using SQLAlchemy,
and deletes every state of hbtn_0e_6_usa whose name contains the letter
a. Nothing is executed when the module is imported.
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
    for state in session.query(State).filter(State.name.like("%a%")).all():
        session.delete(state)
    session.commit()
    session.close()
