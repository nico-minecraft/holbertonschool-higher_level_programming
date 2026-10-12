#!/usr/bin/python3
"""Module that lists all cities of a given state from hbtn_0e_4_usa.

It takes the MySQL username, password, database name and a state name
as arguments, connects to a MySQL server on localhost at port 3306, and
prints the cities of that state sorted by cities.id, separated by commas.
The state name is passed as a query parameter, so it is safe from SQL
injection. Nothing is executed when the module is imported.
"""
import MySQLdb
import sys

if __name__ == "__main__":
    db = MySQLdb.connect(host="localhost", port=3306, user=sys.argv[1],
                         passwd=sys.argv[2], db=sys.argv[3])
    cur = db.cursor()
    cur.execute("SELECT cities.name FROM cities "
                "JOIN states ON cities.state_id = states.id "
                "WHERE states.name = %s ORDER BY cities.id ASC",
                (sys.argv[4],))
    print(", ".join([row[0] for row in cur.fetchall()]))
    cur.close()
    db.close()
