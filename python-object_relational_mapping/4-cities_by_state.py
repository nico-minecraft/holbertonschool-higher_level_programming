#!/usr/bin/python3
"""Module that lists all cities of the database hbtn_0e_4_usa.

It takes the MySQL username, password and database name as arguments,
connects to a MySQL server on localhost at port 3306, and prints each
city with the name of its state, sorted by cities.id in ascending order.
Nothing is executed when the module is imported.
"""
import MySQLdb
import sys

if __name__ == "__main__":
    db = MySQLdb.connect(host="localhost", port=3306, user=sys.argv[1],
                         passwd=sys.argv[2], db=sys.argv[3])
    cur = db.cursor()
    cur.execute("SELECT cities.id, cities.name, states.name "
                "FROM cities JOIN states ON cities.state_id = states.id "
                "ORDER BY cities.id ASC")
    for row in cur.fetchall():
        print(row)
    cur.close()
    db.close()
