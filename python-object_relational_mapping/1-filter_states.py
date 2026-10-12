#!/usr/bin/python3
"""Module that lists all states whose name starts with an uppercase N.

It takes the MySQL username, password and database name as arguments,
connects to a MySQL server on localhost at port 3306, and prints each
matching row of the states table sorted by states.id in ascending order.
Nothing is executed when the module is imported.
"""
import MySQLdb
import sys

if __name__ == "__main__":
    db = MySQLdb.connect(host="localhost", port=3306, user=sys.argv[1],
                         passwd=sys.argv[2], db=sys.argv[3])
    cur = db.cursor()
    cur.execute("SELECT * FROM states WHERE name LIKE BINARY 'N%' "
                "ORDER BY id ASC")
    for row in cur.fetchall():
        print(row)
    cur.close()
    db.close()
