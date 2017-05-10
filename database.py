import mysql.connector                      # mysql functionality
import sys                                  # for misc errors

class Database:
    def __init__(self, server, username, password, database):
    # def __init__(self):
        # initialize db connection
        self.con = mysql.connector.connect(host=server,
                                           user=username,
                                           password=password,
                                           database=database)

        # initialize a cursor
        self.cursor = self.con.cursor();

        print("Connected!")

        self.logged_in = False
        self.user_id   = -1             # current user id
        self.user_type = None           # author, editor, or reviewer

    # def connect(self, server, username, password, database):
    #     self.con = mysql.connector.connect(host=server,
    #                                        user=username,
    #                                        password=password,
    #                                        database=database)

    #     self.cursor = self.con.cursor();

    #     print("Connected!")

    def get_con(self):
        return self.con

    def get_cursor(self):
        return self.cursor

    def get_user_id(self):
        return self.user_id

    def get_user_type(self):
        return self.user_type

    def change_user_id(self, id):
        self.user_id = int(id)

    def change_user_type(self, type):
        self.user_type = type

    def log_on(self):
        self.logged_in = True

    def log_off(self):
        self.logged_in = False
