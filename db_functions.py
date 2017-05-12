# Barry Yang and Lily Xu
# CS 61 Databases
# Lab 2 part e
# May 12, 2017

# helper functions for database execution


import datetime         # get current date
import random


def submit_query(db, query):

    cursor = db.get_cursor()

    # query db
    cursor.execute(query)

    # print("Query executed: '{0}'\n\nResults:".format(query))
    #
    # # display table header
    # print(''.join(['{:<20}'.format(col) for col in cursor.column_names]))
    # print('-' * 120)
    #
    # # display results
    # for row in cursor:
    #     print(''.join(['{:<20}'.format(str(col)) for col in row]))
    #
    # print('\n')


def get_cursor_results(db, query):
    cursor = db.get_cursor()
    cursor.execute(query)

    return cursor

def get_single_query(db, query):
    cursor = db.get_cursor()
    cursor.execute(query)

    # getDate = "SELECT dateReceived FROM manuscript WHERE manuscriptID = " + str(manuscript_num) + ';'
    # results = get_cursor_results(db, getDate)

    to_return = None
    for row in cursor:
        for col in row:
            to_return = col
            print to_return

    return to_return

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
            process_author(db, tokens)
        elif db.get_user_type() == 'editor':
            process_editor(db, tokens)
        elif db.get_user_type() == 'reviewer':
            process_reviewer(db, tokens)
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


    # execute login
    db.change_user_id(int(user_id))
    db.change_user_type('reviewer') # or 'editor' or 'reviewer'
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

        # this coudl probably be made into a function, but I can do that later
        query = "SELECT DISTINCT fname, lname FROM editorNames WHERE personID = " +  str(user_id) + ';'
        results = get_cursor_results(db, query)

        for (fname, lname) in results:
            print("\nHello {} {}".format(fname, lname))

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

        if(len(tokens) == 5):
            register_reviewer(db, tokens[2], tokens[3])
        elif(len(tokens) == 6):
            register_reviewer(db, tokens[2], tokens[3], tokens[4], tokens[5])
        elif(len(tokens) == 7):
            register_reviewer(db, tokens[2], tokens[3], tokens[4], tokens[5], tokens[6])


def register_person(db, fname, lname):

    cursor = db.get_cursor()
    con = db.get_con()

    add_person = ("INSERT INTO person (fname,lname) VALUES (%s, %s);")

    data_add = (fname, lname)

    cursor.execute(add_person, data_add)
    personID = cursor.lastrowid
    print("{} {} is registed with ID {} ".format(fname, lname, str(personID)))
    con.commit()

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
    con = db.get_con()
    cursor.execute(add_author, data_author)
    con.commit()


def register_editor(db, fname, lname):
    personID = register_person(db, fname, lname)

    add_editor = ("INSERT INTO editor "
                  "(personID) "
                  "VALUES (%(personID)s)")

    data_editor = {
        'personID': personID
    }

    cursor = db.get_cursor()
    con = db.get_con()
    cursor.execute(add_editor, data_editor)
    con.commit()


def register_reviewer(db, fname, lname, *ricode):

    ricode1 = None
    ricode2 = None
    ricode3 = None
    print fname, lname

    if(len(ricode == 1)):
        ricode1 = ricode[0]

    # personID = register_person(db, fname, lname)
    #
    # # TODO: get affiliation and email??
    # query = 'INSERT INTO reviewer (personID,affiliation,email) VALUES (' + \
    #          personID  + ',"' + affiliation + '","' + email + '");'
    # # TODO: submit reviewer_has_RICodes???
    # # ',' + ricode1 + ',' + ricode2 + ',' + ricode3 + ');'
    # submit_query(db, query)

def insert_secondaryAuthors(manuscript_id, name, order):
    names = name.split()

    add_SA = ("INSERT INTO secondaryAuthor "
              "(manuscriptID, authorOrder, fname, lname) "
              "VALUES (%s, %s, %s, %s)")

    data_SA = (manuscript_id, order, names[0], names[1])

    return add_SA, data_SA

def process_author(db, tokens):
    command = tokens[0]

    con = db.get_con()
    cursor = db.get_cursor()

    if command == 'status':
        print ("Manuscript Statuses for User ID {}: \n".format(db.user_id))
        status_author(db, db.user_id)

    # submit manuscript to system
    elif command == 'submit':

        now = datetime.datetime.now()

        title = tokens[1]
        affiliation = tokens[2]
        RICode = tokens[3]
        # author2 = None
        # author3 = None
        # author4 = None

        query = ("SELECT personID FROM editor;")
        cursor.execute(query)

        editors_array = []

        for row in cursor:
            for col in row:
                if(col > 0):
                    editors_array.append(col)

        editor_id = random.choice(editors_array)


        add_manuscript = ("INSERT INTO manuscript "
                          "(author_personID,editor_personID,title,status,ricodeID,numPages,startingPage,issueOrder,dateReceived,dateSentForReview,dateAccepted,issue_publicationYear,issue_periodNumber) "
                          "VALUES (%(author_personID)s, %(editor_personID)s, %(title)s, %(status)s, %(ricodeID)s, NULL, NULL, NULL, NOW(), NULL, NULL, NULL, NULL)")

        data_author = {
            'author_personID': db.user_id,
            'editor_personID': editor_id,
            'title': title,
            'status': 'received',
            'ricodeID': RICode,
        }

        cursor.execute(add_manuscript, data_author)
        manuscript_id = cursor.lastrowid

        update_affiliation = ("UPDATE author SET affiliation = %s WHERE personID = %s;")
        cursor.execute(update_affiliation, (affiliation, db.user_id))

        print ("Submitted and Updated:\n"
               "Manuscript ID is " + str(manuscript_id) + "\n"
               "Manuscript SUBMITTED on " + now.strftime("%Y-%m-%d") + " \n")

        if (len(tokens) >= 5):

            # NEED TO VALIDATE ONLY TWO NAMES PER SECONDARY AUTHOR

            add_SA, data_SA = insert_secondaryAuthors(manuscript_id, tokens[4], 1)
            cursor.execute(add_SA, data_SA)

        if (len(tokens) >= 6):
            add_SA, data_SA = insert_secondaryAuthors(manuscript_id, tokens[5], 2)
            cursor.execute(add_SA, data_SA)

        if (len(tokens) == 7):
            add_SA, data_SA = insert_secondaryAuthors(manuscript_id, tokens[6], 3)
            cursor.execute(add_SA, data_SA)

        con.commit()


        # TODO: select editor to input? anything else needed when submitting manuscript to system?



        # query = "INSERT INTO manuscript (manuscriptID,author_personID,editor_personID," + \
        #         "title,`status`,ricodeID,numPages,startingPage,issueOrder,dateReceived," + \
        #         "dateSentForReview,dateAccepted,issue_publicationYear,issue_periodNumber) " + \
        #         "VALUES (NULL," + db.user_id + ',' + "300" + ',' + title + ",received," + RICode + ',' + \
        #         "NULL,NULL,NULL," + datetime.date.today() + ",NULL,NULL,NULL,NULL);"
        # submit_query(db, query)

    # immediately remove manuscript, regardless of status
    elif command == 'retract':
        manuscript_num = tokens[1]
        query = "SELECT manuscriptID, author_personID FROM manuscript WHERE author_personID = " +  str(db.user_id) + " AND manuscriptID = " + str(manuscript_num) + ';'
        cursor.execute(query)

        if(cursor.fetchone()):
            s = raw_input('Are you sure? (y/n): ')
            if s.lower() == 'y':
                query = "DELETE FROM manuscript WHERE manuscriptID = " + str(manuscript_num) + ';'
                submit_query(db, query)

                query = "DELETE FROM feedback WHERE manuscriptID = " + str(manuscript_num) + ';'
                submit_query(db, query)

                print "Manuscript {} has been deleted".format(manuscript_num)

                con.commit()

            else:
                print("No action taken.")
        else:
            print "Sorry, you are not the author of this manuscript."

    else:
        print("Invalid input. Command '" + command + "' not recognized.")



def process_editor(db, tokens):
    command = tokens[0]


    now = datetime.datetime.now()

    con = db.get_con()
    cursor = db.get_cursor()

    if command == 'status':
        status_editor(db, db.user_id)
    elif command == 'assign' and len(tokens) == 3:

        #update editorID to

        manuscript_num = tokens[1]
        reviewer_id = tokens[2]

        # should check to make sure that RICode matches
        getManuscriptRICode = "SELECT ricodeID FROM manuscript WHERE manuscriptID = " + str(manuscript_num) + ';'
        manuscriptRICode = get_single_query(db, getManuscriptRICode)

        getReviewerRICodes = "SELECT RICode_RICodeID  from reviewer_has_RICode WHERE reviewer_personID = " + str(reviewer_id) + ';'
        cursor.execute(getReviewerRICodes)

        reviewerRICodes = []

        for row in cursor:
            for col in row:
                if(col > 0):
                    reviewerRICodes.append(col)

        print "ReviewerRICodes are " + str(reviewerRICodes)
        print "manuscript RICode is " + str(manuscriptRICode)

        if(manuscriptRICode in reviewerRICodes):

            getDate = "SELECT dateReceived FROM manuscript WHERE manuscriptID = " + str(manuscript_num) + ';'
            # results = get_cursor_results(db, getDate)
            #
            # date = None
            # for row in results:
            #     for (dateReceived) in row:
            #         date = dateReceived
            #         print date

            date = get_single_query(db, getDate)

            add_feedback = ("INSERT INTO feedback "
                            "(manuscriptID,reviewer_personID,appropriateness,clarity,methodology,contribution,recommendation,dateReceived) "
                            "VALUES (%(manuscriptID)s, %(reviewer_personID)s, NULL, NULL, NULL, NULL, NULL, %(dateReceived)s)")

            data_feedback = {
                'manuscriptID': manuscript_num,
                'reviewer_personID': reviewer_id,
                'dateReceived': date,
            }

            cursor.execute(add_feedback, data_feedback)

            query = "UPDATE manuscript SET status = 'underReview', dateSentForReview = NOW() WHERE manuscriptID = " + str(manuscript_num) + ';'
            cursor.execute(query)
            # date received?
            # insert_feedback = ""
            print("Manuscript ID {} assigned to reviewer {}. Manuscript status set to 'underReview'".format(manuscript_num, reviewer_id))


            con.commit()
        else:
            print "Invalid entry. This reviewer does not have the appropriate RICode"

    elif command == 'reject' and len(tokens) == 2:
        manuscript_num  = tokens[1]
        #date rejected
        query = "UPDATE manuscript SET status = 'rejected' WHERE manuscriptID = " + str(manuscript_num) + ';'
        cursor.execute(query)
        con.commit()
        print("Manuscript {} rejected on {}").format(manuscript_num, now.strftime("%Y-%m-%d"))

    elif command == 'accept' and len(tokens) == 2:
        manuscript_num  = tokens[1]
        query = "UPDATE manuscript SET status = 'accepted', dateAccepted = NOW() WHERE manuscriptID = " + str(manuscript_num) + ';'
        cursor.execute(query)
        con.commit()
        print("Manuscript {} accepted on {}").format(manuscript_num, now.strftime("%Y-%m-%d"))

    elif command == 'typeset' and len(tokens) == 3:
        manuscript_num  = tokens[1]
        pp              = tokens[2]
        query = "UPDATE manuscript SET status = 'typeset', numPages = {} WHERE manuscriptID = {};".format(pp, manuscript_num)
        cursor.execute(query)
        con.commit()
        print("Manuscript {} status set to 'typeset' on {}. {} pages logged").format(manuscript_num, now.strftime("%Y-%m-%d"), pp)

    elif command == 'schedule' and len(tokens) == 4:
        manuscript_num  = tokens[1]
        issueYear       = tokens[2]
        issuePeriod     = tokens[3]

        # select manuscriptID, numPages, issue_publicationYear, issue_periodNumber from manuscript WHERE issue_publicationYear = 2017 AND issue_periodNumber = 4;
        getNumPages = "SELECT numPages FROM manuscript WHERE issue_publicationYear = {} AND issue_periodNumber = {};".format(issueYear, issuePeriod)
        cursor.execute(getNumPages)

        page_sum = 0

        for row in cursor:
            for col in row:
                if(col > 0):
                    page_sum += int(col)

        getNumManuscriptPage = "SELECT numPages FROM manuscript WHERE manuscriptID = {}".format(manuscript_num)
        page = get_single_query(db, getNumManuscriptPage)

        if ((page is not None) and (page + page_sum <= 100)):
            query = "UPDATE manuscript SET status = 'scheduled', issue_publicationYear = {}, issue_periodNumber = {} WHERE manuscriptID = {};".format(issueYear, issuePeriod, manuscript_num)
            cursor.execute(query)
            con.commit()
            print("Manuscript {} scheduled for issue year {}, period {}").format(manuscript_num, issueYear, issuePeriod)
        else:
            print "Invalid entry. Check if manuscript {} has a valid number of pages or number of pages in issue does not have any errors.".format(manuscript_num)


    elif command == 'publish' and len(tokens) == 3:
        issueYear       = tokens[1]
        issuePeriod     = tokens[2]

        query = "UPDATE manuscript SET status = 'published' WHERE issue_publicationYear = {} AND issue_periodNumber = {};".format(issueYear, issuePeriod)
        cursor.execute(query)

        query = "UPDATE issue SET datePrinted = NOW() WHERE publicationYear = {} AND periodNumber = {};".format(issueYear, issuePeriod)
        cursor.execute(query)

        con.commit()
        print("Issue year {}, period {} printed on {}. Status of all corresponding manuscripts changed to 'published'").format(issueYear, issuePeriod, now.strftime("%Y-%m-%d"))
    else:
        print("Invalid input. Command '" + command + "' not recognized, or corresponding arguments are not correct")

    # db.cleanup()

def process_reviewer(db, tokens):
    command = tokens[0]

    if command == 'status':
        status_reviewer(db, db.user_id)
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
    print("{} manuscripts published\n".format(status_query_return(db, query)))


def status_editor(db, editor_id):

    print "Here are your current manuscripts: "

    cursor = db.get_cursor()
    # query = "SELECT status, manuscriptID, title FROM manuscript WHERE editor_personID = {} ORDER BY status, manuscriptID".format(editor_id)
    query = "SELECT status, manuscriptID, title FROM manuscript ORDER BY status, manuscriptID"
    cursor.execute(query)

    if(cursor.fetchone()):
        for (status, manuscriptID, title) in cursor:
            print("ID {} -- status: {}: '{}' ".format(manuscriptID, status, title))
    else:
        print "You have no manuscripts at this time"

    # print("{} submitted".format(x))
    # print("{} under review".format(x))
    # print("{} rejected".format(x))
    # print("{} accepted".format(x))
    # print("{} in typesetting".format(x))
    # print("{} scheduled for publication".format(x))
    # print("{} published".format(x))


def status_reviewer(db, reviewer_id):
    x = 5

    print("{} submitted".format(x))
    print("{} under review".format(x))
    print("{} rejected".format(x))
    print("{} accepted".format(x))
    print("{} typesetting".format(x))
    print("{} scheduled for publication".format(x))
    print("{} published".format(x))
