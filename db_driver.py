# Barry Yang and Lily Xu
# CS 61 Databases
# Lab 2 part e
# May 12, 2017


from __future__ import print_function       # make print a function
import sys                                  # for misc errors
import traceback                            # for error handling
import mysql.connector                      # mysql functionality

from database import Database
from db_functions import *

SERVER    = "sunapee.cs.dartmouth.edu"      # db server to connect to
USERNAME  = "byang"                         # user to connect as
PASSWORD  = "7webster"                      # user's password
DATABASE  = "byang_db"                      # db to user

if __name__ == "__main__":
    db = Database(SERVER, USERNAME, PASSWORD, DATABASE)
    # db.connect(SERVER, USERNAME, PASSWORD, DATABASE)

    try:
        print("Connection established.\n")

        # query = "SELECT * FROM feedback;"

        # submit_query(db, query)

        # print(submit_query_return(db, query))
        # submit_query_return(db, query)

        print("Please input your request. Use '|' to split commands.")
        print("  e.g. register|author|Lily|Xu|lily.18@dartmouth.edu|4774 Hinman Box, Hanover, NH 03755")
        print("  Type 'q' or 'quit' to exit.")
        s = raw_input('--> ')

        while (s != 'quit' and s != 'q'):
            parse_input(db, s)
            s = raw_input('--> ')

        db.cursor.close()
        db.con.close()


    except mysql.connector.Error as e:        # catch SQL errors
        print("SQL Error: {0}".format(e.msg))

    except:                                   # anything else
        print("Unexpected error: {0}".format(sys.exc_info()[0]))
        traceback.print_exc()


    # cleanup
    try:
        db.cleanup()
    except:
        print("Unexpected error: {0}".format(sys.exc_info()[0]))


    print("\nConnection terminated.\n", end='')
