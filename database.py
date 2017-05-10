# pylint: disable=C0111, C0326, W0702, C0103

from __future__ import print_function        # make print a function
import sys                                   # for misc errors
import mysql.connector                       # mysql functionality


SERVER   = "sunapee.cs.dartmouth.edu"        # db server to connect to
USERNAME = "byang"                            # user to connect as
PASSWORD = "7webster"                            # user's password
DATABASE = "byang_db"                              # db to user
QUERY    = "SELECT * FROM feedback;"       # query statement

def main():
    try:
        # initialize db connection
        con = mysql.connector.connect(host=SERVER,user=USERNAME,password=PASSWORD,
                                      database=DATABASE)
        print("Connection established.")

        # initialize a cursor
        cursor = con.cursor()

        # query db
        cursor.execute(QUERY)

        # print("Query executed: '{0}'\n\nResults:".format(QUERY))

        # print table header
        # print("".join(["{:<20}".format(col) for col in cursor.column_names]))
        # print("------------------------------------------------------------------")

        # iterate through results
        # for row in cursor
        # print("".join(["{:<20}".format(col) for col in row]))

    except mysql.connector.Error as e:        # catch SQL errors
        print("SQL Error: {0}".format(e.msg))
    except:                                   # anything else
        print("Unexpected error: {0}".format(sys.exc_info()[0]))

    raw = raw_input('--> ')

    while raw != "quit":
        print(raw)
        input_list = raw.split()
        print(input_list)

        if input_list[0] == "login":
            print("login code here")

        elif input_list[0] == "author":
            print("login code here")

        elif input_list[0] == "author":
            print("login code here")

        raw = raw_input('--> ')

    # cleanup
    con.close()
    cursor.close()

    print("\nConnection terminated.", end='')

if __name__ == "__main__":
    main()
