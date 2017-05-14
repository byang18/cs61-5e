# Barry Yang and Lily Xu
# CS 61 Databases
# Lab 2 part e
# May 12, 2017


import mysql.connector                      # mysql functionality

class Database:
    def __init__(self, server, username, password, database, confidential = True, logged_in = False, userID = -1, user_type = ""):
        # initialize db connection
        self.con = mysql.connector.connect(host=server,
                                           user=username,
                                           password=password,
                                           database=database)

        #check to see if this is right
        self.server = server
        self.database = database

        # initialize a cursor
        self.cursor = self.con.cursor()

        self.logged_in = logged_in          # boolean: whether anyone is logged in
        self.user_id   = userID            # int: current user id
        self.user_type = user_type             # string: author, editor, or reviewer

        self.confidential = confidential
        # self.user_changed = []


    # def get_user_changed(self):
    #     return self.user_changed
    #
    # def change_user_changed(self, username, password):
    #     self.userchanged = [username, password]
    #     return self.

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

    def change_user_id(self, user_id):
        self.user_id = int(user_id)

    def change_user_type(self, user_type):
        self.user_type = user_type

    def log_on(self):
        self.logged_in = True

    def log_off(self):
        self.logged_in = False
        self.user_id = -1
        self.user_type = ""

    def cleanup(self):
        self.con.close()
        self.cursor.close()
