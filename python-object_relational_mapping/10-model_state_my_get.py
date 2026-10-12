#!/usr/bin/python3
"""Module that prints the id of the State matching a given name.

It takes the MySQL username, password, database name and the state name
to search as arguments, connects to a MySQL server on localhost at port
3306 using SQLAlchemy, and prints the states.id of the matching state in
hbtn_0e_6_usa, or Not found if there is none. The name is bound as a
query parameter, so it is safe from SQL injection. Nothing is executed
when the module is imported.
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
    state = session.query(State).filter(State.name == sys.argv[4]).first()
    if state is None:
        print("Not found")
    else:
        print(state.id)
    session.close()
