#!/usr/bin/python3
"""Module that safely lists all states matching a name given as argument.

It takes the MySQL username, password, database name and the state name
to search as arguments, connects to a MySQL server on localhost at port
3306, and prints each matching row of the states table sorted by
states.id in ascending order. The state name is passed to MySQLdb as a
query parameter, so it is safe from SQL injection. Nothing is executed
when the module is imported.
"""
import MySQLdb
import sys

if __name__ == "__main__":
    db = MySQLdb.connect(host="localhost", port=3306, user=sys.argv[1],
                         passwd=sys.argv[2], db=sys.argv[3])
    cur = db.cursor()
    cur.execute("SELECT * FROM states WHERE name = %s ORDER BY id ASC",
                (sys.argv[4],))
    for row in cur.fetchall():
        print(row)
    cur.close()
    db.close()
