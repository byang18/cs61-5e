# Barry Yang and Lily Xu
# CS 61 Databases
# Lab 2 part e

from __future__ import print_function       # make print a function
import mysql.connector                      # mysql functionality
import sys                                  # for misc errors

SERVER    = "sunapee.cs.dartmouth.edu"      # db server to connect to
USERNAME  = "byang"                         # user to connect as
PASSWORD  = "7webster"                      # user's password
DATABASE  = "byang_db"                      # db to user
query     = "SELECT * FROM feedback;"       # query statement
logged_in = False
user_id   = -1                              # current user id

if __name__ == "__main__":
    try:
        # initialize db connection
        con = mysql.connector.connect(host=SERVER,
                                      user=USERNAME,
                                      password=PASSWORD,
                                      database=DATABASE)

        print("Connection established.")

        # initialize a cursor
        cursor = con.cursor()

        # query db
        cursor.execute(query)

        print("Query executed: '{0}'\n\nResults:".format(query))

        # print table header
        print("".join(["{:<20}".format(col) for col in cursor.column_names]))
        print("-" * 170)

        # iterate through results
        for row in cursor:
            print("".join(["{:<20}".format(col) for col in row]))

        print("\n")


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


def parse_input(string):
    tokens = string.strip().split(" ");
    if len(tokens) == 0:
        print("Invalid input.")
        return

    if tokens[0] == "login":
        login(id)
    elif tokens[0] == "register":
        register(tokens)
    else:
        print("Invalid input.")
        return


def login(id):
    # execute login
    # find corresponding id
    user_id = int(id)


def register(tokens):
    if tokens[1] == "editor":
        register_editor(tokens[2], tokens[3])
    elif tokens[1] == "reviewer":
        register_reviewer(tokens[2], tokens[3])
    elif tokens[1] == "author":
        register_author(tokens[2], tokens[3])


def register_editor(fname, lname):
    query = "INSERT INTO editor VALUES (NULL, fname, lname);"


def register_author(fname, lname, email, address):
    query = "INSERT INTO author VALUES (NULL, fname, lname, email, address);"


def register_reviewer(fname, lname, ricode1, ricode2, ricode3):
    query = "INSERT INTO reviewer VALUES (NULL, fname, lname, ricode1, ricode2, ricode3);"


