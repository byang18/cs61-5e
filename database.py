# Barry Yang and Lily Xu
# CS 61 Databases
# Lab 2 part e
# May 12, 2017


import mysql.connector                      # mysql functionality

class Database:
    def __init__(self, server, username, password, database, confidential = True):
        # initialize db connection
        self.con = mysql.connector.connect(host=server,
                                           user=username,
                                           password=password,
                                           database=database)

        # initialize a cursor
        self.cursor = self.con.cursor();

        print("Connected!")

        self.logged_in = False          # boolean: whether anyone is logged in
        self.user_id   = -1             # int: current user id
        self.user_type = ""             # string: author, editor, or reviewer

        self.confidential = confidential

    def get_con(self):
        return self.con

    def get_cursor(self):
        return self.cursor

    def is_logged_in(self):
        return self.logged_in

    def is_confidential(self):
        return self.confidential

    def get_user_id(self):
        return self.user_id

    def get_user_type(self):
        return self.user_type

    def change_user_id(self, id):
        self.user_id = int(id)

    def change_user_type(self, user_type):
        self.user_type = user_type

    def log_on(self):
        self.logged_in = True

    def log_off(self):
        self.logged_in = False

    def cleanup(self):
        self.con.close()
        self.cursor.close()

