#!/usr/bin/python3
"""Module that changes the name of the State with id 2 to New Mexico.

It takes the MySQL username, password and database name as arguments,
connects to a MySQL server on localhost at port 3306 using SQLAlchemy,
and updates the name of the state whose states.id is 2 in hbtn_0e_6_usa.
Nothing is executed when the module is imported.
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
    state = session.query(State).filter(State.id == 2).first()
    if state is not None:
        state.name = "New Mexico"
        session.commit()
    session.close()
