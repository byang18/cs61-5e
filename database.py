# Barry Yang and Lily Xu
# CS 61 Databases
# Lab 2 part e

from __future__ import print_function       # make print a function
import mysql.connector                      # mysql functionality
import sys                                  # for misc errors

from database_fxns import *

SERVER    = "sunapee.cs.dartmouth.edu"      # db server to connect to
USERNAME  = "byang"                         # user to connect as
PASSWORD  = "7webster"                      # user's password
DATABASE  = "byang_db"                      # db to user
query     = "SELECT * FROM feedback;"       # query statement
logged_in = False
user_id   = -1                              # current user id
user_type = None                            # author, editor, or reviewer

if __name__ == "__main__":
    try:
        # initialize db connection
        con = mysql.connector.connect(host=SERVER,
                                      user=USERNAME,
                                      password=PASSWORD,
                                      database=DATABASE)

        print("Connection established.\n")

        submit_query(con, query)


    except mysql.connector.Error as e:        # catch SQL errors
        print("SQL Error: {0}".format(e.msg))

    except:                                   # anything else
        print("Unexpected error: {0}".format(sys.exc_info()[0]))

    s = raw_input('--> ')

    while (s != "quit"):
        s = raw_input('--> ')
        parse_input(s)


    # cleanup
    con.close()
    cursor.close()

    print("\nConnection terminated.\n", end='')





