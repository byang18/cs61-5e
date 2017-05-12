# Barry Yang and Lily Xu
# CS 61 Databases
# Lab 2 part e
# May 12, 2017


from __future__ import print_function       # make print a function
import traceback                            # for error handling
import sys                                  # for misc errors
import mysql.connector                      # mysql functionality
import binascii

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

        if db.is_confidential():
            print("Please enter the master key used for encryption:")
            key   = raw_input('--> ')
            # key = binascii.a2b_hqx(key)
            # key = binascii.hexlify(key)
            # db.set_key(key)

            # query = 'SELECT CONVERT(object USING utf8) FROM UNHEX("' + key + '");'
            query = 'SET @key_str = HEX("' + key + '");'

            get_cursor_results(db,query)

            # con    = db.get_con()
            # cursor = db.get_cursor()

            # cursor.execute(query)
            # con.commit()

            # query = 'INSERT INTO credential (personID, pword) VALUES (' + str(1000) + ', AES_ENCRYPT("hey","' + db.get_key() + '"));'

            # cursor.execute(query)
            # con.commit()

            # query = "SELECT * FROM user_variables_by_thread;"
            # print(submit_query_return(db, query))

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





