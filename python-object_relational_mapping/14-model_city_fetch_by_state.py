#!/usr/bin/python3
"""Module that prints all City objects of the database hbtn_0e_14_usa.

It takes the MySQL username, password and database name as arguments,
connects to a MySQL server on localhost at port 3306 using SQLAlchemy,
and prints every city as "<state name>: (<city id>) <city name>" sorted
by cities.id in ascending order. Nothing is executed when the module is
imported.
"""
import sys
from model_city import City
from model_state import Base, State
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

if __name__ == "__main__":
    engine = create_engine("mysql+mysqldb://{}:{}@localhost:3306/{}".format(
        sys.argv[1], sys.argv[2], sys.argv[3]), pool_pre_ping=True)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    rows = session.query(State, City).filter(
        State.id == City.state_id).order_by(City.id).all()
    for state, city in rows:
        print("{}: ({}) {}".format(state.name, city.id, city.name))
    session.close()
