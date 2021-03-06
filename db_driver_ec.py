# Barry Yang and Lily Xu
# CS 61 Databases
# Lab 2 part e
# May 12, 2017


from __future__ import print_function       # make print a function
import traceback                            # for error handling
import sys                                  # for misc errors
import mysql.connector                      # mysql functionality

from database_ec import Database
from db_functions_ec import *

SERVER    = "sunapee.cs.dartmouth.edu"      # db server to connect to
USERNAME  = "byang"                         # user to connect as
PASSWORD  = "7webster"                      # user's password
DATABASE  = "byang_db"                      # db to user

if __name__ == "__main__":
    db = Database(SERVER, USERNAME, PASSWORD, DATABASE, confidential=True, logged_in=False, userID=-1, user_type="")

    print("Connection established.\n")


    # if confidentiality is set, request and store a master key
    if db.is_confidential():
        # prompt user to enter a master key
        print("Please enter the master key used for encryption:")
        key = raw_input('--> ')

        # store master key in MySQL
        query = 'SET @master_key = HEX("' + key + '");'
        get_cursor_results(db,query)


    # prompt user for request
    print("Please input your request. Use '|' to split commands.")
    print("  e.g. register|author|Lily|Xu|lily.18@dartmouth.edu|4774 Hinman Box, Hanover, NH 03755")
    print("  Type 'q' or 'quit' to exit.")
    s = raw_input('--> ')

    while (s != 'quit' and s != 'q'):
        try:
            store_info = []
            store_info = parse_input(db, s)

            if (store_info is not None):
                um = store_info[0]
                pw = store_info[1]
                user_id = store_info[2]
                user_type = store_info[3]

                db = Database(SERVER, um, pw, DATABASE, True, True, user_id, user_type)

        except mysql.connector.Error as e:        # catch SQL errors
            if str(e.msg)[-13:] != "doesn't exist":
                print("SQL Error: {0}".format(e.msg))

        except:                                   # anything else
            print("Unexpected error: {0}".format(sys.exc_info()[0]))
            traceback.print_exc()

        s = raw_input('--> ')


    # cleanup
    try:
        db.cleanup()
    except:
        print("Unexpected error: {0}".format(sys.exc_info()[0]))


    print("\nConnection terminated.\n", end='')
