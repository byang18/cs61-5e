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
user_type = None                            # author, editor, or reviewer

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

    # TODO: check if user_id is valid?
    user_id = int(id)
    logged_in = True
    user_type = "author" # or "editor" or "reviewer"

    if user_type == "author":
        print "fname, lname, address\n"
        status_author()
    elif user_type == "editor":
        print "fname, lname"
        status_editor()
    elif user_type == "reviewer":
        print "Welcome back, fname, lname!"
        status_reviewer() # limited to manuscripts assigned to that reviewer


def register(tokens):
    if tokens[1] == "editor":
        register_editor(tokens[2], tokens[3])
    elif tokens[1] == "reviewer":
        register_reviewer(tokens[2], tokens[3])
    elif tokens[1] == "author":
        register_author(tokens[2], tokens[3])



def register_author(fname, lname, email, address):
    query = "INSERT INTO author VALUES (NULL, fname, lname, email, address);"


def register_editor(fname, lname):
    query = "INSERT INTO editor VALUES (NULL, fname, lname);"


def register_reviewer(fname, lname, ricode1, ricode2, ricode3):
    query = "INSERT INTO reviewer VALUES (NULL, fname, lname, ricode1, ricode2, ricode3);"


def process_author(tokens):
    command = tokens[0]

    if command == "status":
        status_author()
    elif command == "submit":
        title = tokens[1]
        affiliation = tokens[2]
        RICode = tokens[3]
        author2 = tokens[4]
        author3 = tokens[5]
        author4 = tokens[6]
        filename = tokens[7]
        # TODO: submit manuscript into system
    elif command == "retract":
        manuscript_num = tokens[1]
        # TODO: prompt: are you sure?
        # TODO: if yes, immediately remove manuscript regardless of status



def process_editor(tokens):
    command = tokens[0]

    if command == "status":
        status_editor()
    elif command == "assign":
        manuscript_num = tokens[1]
        reviewer_id = tokens[2]
        # TODO: assign manuscript to a reviewer 
    elif command == "reject":
        manuscript_num = tokens[1]
        # TODO: set manuscript status to rejected and add timestamp
    elif command == "accept":
        manuscript_num = tokens[1]
        # TODO: set manuscript status to accepted and add timestamp
    elif command == "typeset":
        manuscript_num = tokens[1]
        pp = tokens[2]
        # TODO: set manuscript status to typeset and store num pages
    elif command == "schedule":
        manuscript_num = tokens[1]
        issue = tokens[2]
        # TODO: set manuscript status to scheduled and add issue page
        # TODO: if addition of manuscript would cause issue to exceed 100 pages, schedule request should fail
    elif command == "publish":
        issue = tokens[2]
        # TODO: for all manuscripts in issue, set status as published and record timestamp


def process_reviewer(tokens):
    command = tokens[0]

    if command == "status":
        status_reviewer()
    elif command == "resign":
        # prompt to enter unique ID
        print "Thank you for our service!"
        # TODO: remove user from system (invoke trigger)
    elif command == "reject":
        manuscript_num = tokens[1]
        appropriateness = tokens[2]
        clarity = tokens[3]
        methodology = tokens[4]
        contribution = tokens[5]
        # TODO: add info; mark rejected; timestamp
    elif command == "accept":
        manuscript_num = tokens[1]
        appropriateness = tokens[2]
        clarity = tokens[3]
        methodology = tokens[4]
        contribution = tokens[5]
        # TODO: add info; mark accepted; timestamp
    # TODO: if attempt to act on manuscript not assigned to reviewer, display appropriate fail message




def status_author():
    x = 5

    print("{} submitted".format(x))
    print("{} under review".format(x))
    print("{} rejected".format(x))
    print("{} accepted".format(x))
    print("{} in typesetting".format(x))
    print("{} scheduled for publication".format(x))
    print("{} published".format(x))


def status_editor():
    x = 5

    print("{} submitted".format(x))
    print("{} under review".format(x))
    print("{} rejected".format(x))
    print("{} accepted".format(x))
    print("{} in typesetting".format(x))
    print("{} scheduled for publication".format(x))
    print("{} published".format(x))


def status_reviewer():
    x = 5

    print("{} submitted".format(x))
    print("{} under review".format(x))
    print("{} rejected".format(x))
    print("{} accepted".format(x))
    print("{} typesetting".format(x))
    print("{} scheduled for publication".format(x))
    print("{} published".format(x))



