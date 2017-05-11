# Barry Yang and Lily Xu
# CS 61 Databases
# Lab 2 part e
# May 12, 2017

# helper functions for database execution


import datetime         # get current date


def submit_query(db, query):
    cursor = db.get_cursor()

    # query db
    cursor.execute(query)

    print("Query executed: '{0}'\n\nResults:".format(query))

    # display table header
    print(''.join(['{:<20}'.format(col) for col in cursor.column_names]))
    print('-' * 120)

    # display results
    for row in cursor:
        print(''.join(['{:<20}'.format(str(col)) for col in row]))

    print('\n')


def get_cursor_results(db, query):
    cursor = db.get_cursor()
    cursor.execute(query)

    return cursor

# process query, but instead of displaying to user,
# return output to the caller
# NOTE: each column is delimited by a pipe '|'
#       each row is delimited by a newline '\n'
def submit_query_return(db, query):
    cursor = db.get_cursor()
    cursor.execute(query)

    output = ''

    # display results
    for row in cursor:
        for col in row:
            output += str(col) + '|'
        output += '\n'

    # print("output is " + str(output) + "\n")

    return output



# parse input from user
# process command if 'login' or 'register'
# call appropriate function to process command for author, editor, or reviewer
def parse_input(db, string):
    tokens = string.strip().split('|')
    # print ("tokens are " + str(tokens))

    if len(tokens) == 0:
        print("Invalid input. Query cannot be blank")
        return

    # log in user
    if tokens[0] == 'login' and len(tokens) > 1:
        user_id = tokens[1]
        login(db, user_id)
    # register new user
    elif tokens[0] == 'register' and len(tokens) > 1:
        register(db, tokens)
    # logged in, so process according to current user
    elif db.is_logged_in():
        if db.get_user_type() == 'author':
            process_author()
        elif db.get_user_type() == 'editor':
            process_editor()
        elif db.get_user_type() == 'reviewer':
            process_reviewer()
    # if not logged in, must either login or register
    else:
        print("Invalid input. Please login or register.")


def login(db, user_id):
    user_id = int(user_id)

    # check if user_id is valid
    query = "SELECT personID FROM person WHERE personID = " + str(user_id) + ';'
    results = submit_query_return(db, query)

    if results == "":
        print('ERROR: No user exists corresponding to ID ' + str(user_id) + '.')
        return


    # exeute login
    db.change_user_id(int(user_id))
    db.change_user_type('author') # or 'editor' or 'reviewer'
    db.log_on()

    # display greeting
    if db.get_user_type() == 'author':
        # TODO: get user author data

        query = "SELECT DISTINCT fname, lname FROM LeadAuthorManuscripts WHERE personID = " +  str(user_id) + ';'
        results = get_cursor_results(db, query)
        # print ("results here are " + str(results))

        for (fname, lname) in results:
            print("\nHello {} {}".format(fname, lname))

        print "Here are your present manuscripts:\n"
        #print("Hello {} {}".format(fname, lname))
        status_author(db, user_id)

    elif db.get_user_type() == 'editor':
        # TODO: get user data
        print("fname, lname")
        status_editor(db, user_id)
    elif db.get_user_type() == 'reviewer':
        # TODO: get user data
        print("Welcome back, fname, lname!")
        status_reviewer(db, user_id) # limited to manuscripts assigned to that reviewer


def register(db, tokens):
    if tokens[1] == 'author':
        register_author(db, tokens[2], tokens[3], tokens[4], tokens[5])
    elif tokens[1] == 'editor':
        register_editor(db, tokens[2], tokens[3])
    elif tokens[1] == 'reviewer':
        register_reviewer(db, tokens[2], tokens[3])


def register_person(db, fname, lname):

    cursor = db.get_cursor()

    add_person = ("INSERT INTO person "
                  "(fname,lname) "
                  "VALUES (%s, %s)")

    data_add = (fname, lname)

    cursor.execute(add_person, data_add)
    personID = cursor.lastrowid
    print("personID is " + str(personID))

    return personID


def register_author(db, fname, lname, email, address):
    personID = register_person(db, fname, lname)

    add_author = ("INSERT INTO author "
                  "(personID,email,address,affiliation) "
                  "VALUES (%(personID)s, %(email)s, %(address)s, NULL)")

    data_author = {
        'personID': personID,
        'email': email,
        'address': address,
    }

    cursor = db.get_cursor()
    cursor.execute(add_author, data_author)


def register_editor(db, fname, lname):
    personID = register_person(db, fname, lname)

    query = 'INSERT INTO editor (personID) VALUES (' + personID + ');'
    submit_query(db, query)


def register_reviewer(db, fname, lname, ricode1, ricode2, ricode3):
    personID = register_person(db, fname, lname)

    # TODO: get affiliation and email??
    query = 'INSERT INTO reviewer (personID,affiliation,email) VALUES (' + \
             personID  + ',"' + affiliation + '","' + email + '");'
    # TODO: submit reviewer_has_RICodes???
    # ',' + ricode1 + ',' + ricode2 + ',' + ricode3 + ');'
    submit_query(db, query)


def process_author(db, tokens):
    command = tokens[0]

    if command == 'status':
        status_author()

    # submit manuscript to system
    elif command == 'submit':
        title       = tokens[1]
        affiliation = tokens[2]
        RICode      = tokens[3]
        author2     = tokens[4]
        author3     = tokens[5]
        author4     = tokens[6]
        filename    = tokens[7]

        # TODO: select editor to input? anything else needed when submitting manuscript to system?
        query = "INSERT INTO manuscript (manuscriptID,author_personID,editor_personID," + \
                "title,`status`,ricodeID,numPages,startingPage,issueOrder,dateReceived," + \
                "dateSentForReview,dateAccepted,issue_publicationYear,issue_periodNumber) " + \
                "VALUES (NULL," + db.user_id + ',' + "300" + ',' + title + ",received," + RICode + ',' + \
                "NULL,NULL,NULL," + datetime.date.today() + ",NULL,NULL,NULL,NULL);"
        submit_query(db, query)

    # immediately remove manuscript, regardless of status
    elif command == 'retract':
        manuscript_num = tokens[1]

        s = raw_input('Are you sure? (y/n): ')
        if s.lower() == 'y':
            query = "DELETE FROM manuscript WHERE manuscriptID = " + str(manuscript_num) + ';'
            submit_query(db, query)
        else:
            print("No action taken.")

    else:
        print("Invalid input. Command '" + command + "' not recognized.")



def process_editor(db, tokens):
    command = tokens[0]

    if command == 'status':
        status_editor()
    elif command == 'assign':
        manuscript_num  = tokens[1]
        reviewer_id     = tokens[2]
        # TODO: assign manuscript to a reviewer
    elif command == 'reject':
        manuscript_num  = tokens[1]
        # TODO: set manuscript status to rejected and add timestamp
    elif command == 'accept':
        manuscript_num  = tokens[1]
        # TODO: set manuscript status to accepted and add timestamp
    elif command == 'typeset':
        manuscript_num  = tokens[1]
        pp              = tokens[2]
        # TODO: set manuscript status to typeset and store num pages
    elif command == 'schedule':
        manuscript_num  = tokens[1]
        issue           = tokens[2]
        # TODO: set manuscript status to scheduled and add issue page
        # TODO: if addition of manuscript would cause issue to exceed 100 pages, schedule request should fail
    elif command == 'publish':
        issue           = tokens[2]
        # TODO: for all manuscripts in issue, set status as published and record timestamp
    else:
        print("Invalid input. Command '" + command + "' not recognized.")


def process_reviewer(db, tokens):
    command = tokens[0]

    if command == 'status':
        status_reviewer()
    elif command == 'resign':
        # prompt to enter unique ID
        print("Thank you for our service!")
        # TODO: remove user from system (invoke trigger)
    elif command == 'reject':
        manuscript_num  = tokens[1]
        appropriateness = tokens[2]
        clarity         = tokens[3]
        methodology     = tokens[4]
        contribution    = tokens[5]
        # TODO: add info; mark rejected; timestamp
    elif command == 'accept':
        manuscript_num  = tokens[1]
        appropriateness = tokens[2]
        clarity         = tokens[3]
        methodology     = tokens[4]
        contribution    = tokens[5]
        # TODO: add info; mark accepted; timestamp
    # TODO: if attempt to act on manuscript not assigned to reviewer, display appropriate fail message
    else:
        print("Invalid input. Command '" + command + "' not recognized.")

def status_query_return(db, query):
    cursor = db.get_cursor()
    cursor.execute(query)

    # display results
    for row in cursor:
        for col in row:
            if(col > 0):
                return col

    return 0

def status_author(db, author_id):

    # INTERPRET AS LIST MANUSCRIPT: STATUS?

    query = "SELECT count FROM authorNumSubmitted WHERE personID = " +  str(author_id) + ';'
    print("{} manuscripts submitted".format(status_query_return(db, query)))

    query = "SELECT count FROM authorNumUnderReview WHERE personID = " +  str(author_id) + ';'
    print("{} manuscripts under review".format(status_query_return(db, query)))

    query = "SELECT count FROM authorNumRejected WHERE personID = " +  str(author_id) + ';'
    print("{} manuscripts rejected".format(status_query_return(db, query)))

    query = "SELECT count FROM authorNumAccepted WHERE personID = " +  str(author_id) + ';'
    print("{} manuscripts accepted".format(status_query_return(db, query)))

    # typesetting

    query = "SELECT count FROM authorNumScheduled WHERE personID = " +  str(author_id) + ';'
    print("{} manuscripts scheduled".format(status_query_return(db, query)))

    query = "SELECT count FROM authorNumPublished WHERE personID = " +  str(author_id) + ';'
    print("{} manuscripts published".format(status_query_return(db, query)))


def status_editor(db, editor_id):
    x = 5

    print("{} submitted".format(x))
    print("{} under review".format(x))
    print("{} rejected".format(x))
    print("{} accepted".format(x))
    print("{} in typesetting".format(x))
    print("{} scheduled for publication".format(x))
    print("{} published".format(x))


def status_reviewer(db, reviewer_id):
    x = 5

    print("{} submitted".format(x))
    print("{} under review".format(x))
    print("{} rejected".format(x))
    print("{} accepted".format(x))
    print("{} typesetting".format(x))
    print("{} scheduled for publication".format(x))
    print("{} published".format(x))
