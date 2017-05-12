# Barry Yang and Lily Xu
# CS 61 Databases
# Lab 2 part e
# May 12, 2017

# helper functions for database execution


import datetime         # get current date
import random


def get_cursor_results(db, query):
    cursor = db.get_cursor()
    cursor.execute(query)

    return cursor

def get_single_query(db, query):
    cursor = db.get_cursor()
    cursor.execute(query)

    to_return = None
    for row in cursor:
        for col in row:
            to_return = col

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

    return output



# parse input from user
# process command if 'login' or 'register'
# call appropriate function to process command for author, editor, or reviewer
def parse_input(db, string):
    tokens = string.strip().split('|')

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


# check if user_id is valid
# if so, determine user type and act accordingly
# if not, print an error message
def login(db, user_id):
    user_id = int(user_id)

    # is the user an author?
    query = "SELECT fname, lname, address FROM author JOIN person ON author.personID " + \
            "= person.personID WHERE author.personID = " + str(user_id) + ';'

    results = submit_query_return(db, query)

    if results != "":
        results = submit_query_return(db, query)
        results = results.strip().split('|')

        print("Welcome back, author " + str(user_id) + "! Here's what we have stored about you:")
        print("  First name: " + results[0])
        print("  Last name:  " + results[1])
        print("  Address:    " + results[2])

        # execute login
        db.change_user_id(int(user_id))
        db.change_user_type('author')
        db.log_on()

        status_author(db, user_id)

        return

    # is the user an editor?
    query = "SELECT fname, lname FROM editor JOIN person ON editor.personID " + \
            "= person.personID WHERE editor.personID = " + str(user_id) + ';'

    results = submit_query_return(db, query)

    if results != "":
        results = submit_query_return(db, query)
        results = results.strip().split('|')

        print("Welcome back, editor " + str(user_id) + "! Here's what we have stored about you:")
        print("  First name: " + results[0])
        print("  Last name:  " + results[1])

        # execute login
        db.change_user_id(int(user_id))
        db.change_user_type('editor')
        db.log_on()

        status_editor(db, user_id)

        return

    # is the user a reviewer?
    query = "SELECT fname, lname FROM reviewer JOIN person ON reviewer.personID " + \
            "= person.personID WHERE reviewer.personID = "+ str(user_id) + ';'

    results = submit_query_return(db, query)

    if results != "":
        results = submit_query_return(db, query)
        results = results.strip().split('|')

        print("Welcome back, reviewer " + str(user_id) + "! Here's what we have stored about you:")
        print("  First name: " + results[0])
        print("  Last name:  " + results[1])

        # execute login
        db.change_user_id(int(user_id))
        db.change_user_type('reviewer')
        db.log_on()

        # TODO: everything should be limited to manuscripts assigned to that reviewer
        status_reviewer(db, user_id)

        return

    # no user corresponds to given id
    print('ERROR: No user exists corresponding to ID ' + str(user_id) + '.')


def register(db, tokens):
    if tokens[1] == 'author':
        register_author(db, tokens[2], tokens[3], tokens[4], tokens[5])
    elif tokens[1] == 'editor':
        register_editor(db, tokens[2], tokens[3])
    elif tokens[1] == 'reviewer':

        if(len(tokens) == 7):
            register_reviewer(db, tokens[2], tokens[3], tokens[4], tokens[5], tokens[6])
        elif(len(tokens) == 8):
            register_reviewer(db, tokens[2], tokens[3], tokens[4], tokens[5], tokens[6], tokens[7])
        elif(len(tokens) == 9):
            register_reviewer(db, tokens[2], tokens[3], tokens[4], tokens[5], tokens[6], tokens[7], tokens[8])
        else:
            print("Invalid input. Too many arguments.")


def register_person(db, fname, lname):

    cursor = db.get_cursor()
    con = db.get_con()

    add_person = ('INSERT INTO person (fname,lname) VALUES (%s, %s);')

    data_add = (fname, lname)

    cursor.execute(add_person, data_add)
    personID = cursor.lastrowid
    print("{} {} is registered with ID {} ".format(fname, lname, str(personID)))
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


def register_reviewer(db, fname, lname, email, affiliation, *ricodes):

    personID = register_person(db, fname, lname)

    cursor = db.get_cursor()
    con = db.get_con()

    # ricode1 = None
    # ricode2 = None
    # ricode3 = None
    #
    # print ricode
    # print len(ricode)
    # print ricode[0]
    #
    # if(len(ricode) >= 1):
    #     ricode1 = ricode[0]
    # if(len(ricode) >= 1):
    #     ricode2 = ricode[1]
    # if(len(ricode) >= 1):
    #     ricode3 = ricode[2]

    # print fname, lname, email, affiliation, ricode1, ricode2, ricode3

    add_reviewer = ("INSERT INTO reviewer "
                    "(personID,affiliation,email) "
                    "VALUES (%(personID)s, %(affiliation)s, %(email)s)")

    data_reviewer = {
        'personID': personID,
        'affiliation': affiliation,
        'email': email,
    }

    cursor.execute(add_reviewer, data_reviewer)

    for ricode in ricodes:
        add_reviewerRICode = ("INSERT INTO reviewer_has_RICode "
                              "(reviewer_personID,RICode_RICodeID) "
                              "VALUES (%(reviewer_personID)s, %(RICode_RICodeID)s)")
        data_reviewerRICode = {
            'reviewer_personID': personID,
            'RICode_RICodeID': ricode,
        }
        cursor.execute(add_reviewerRICode, data_reviewerRICode)

    con.commit()

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
        print("Manuscript statuses for user ID {}: \n".format(db.user_id))
        status_author(db, db.user_id)

    # submit manuscript to system
    elif command == 'submit':

        now = datetime.datetime.now()

        title       = tokens[1]
        affiliation = tokens[2]
        RICode      = tokens[3]
        # author2 = None
        # author3 = None
        # author4 = None

        # assign an editor to manuscript
        query = ("SELECT personID FROM editor;")
        cursor.execute(query)

        # compile list of possible editors
        editors_array = []

        for row in cursor:
            for col in row:
                if(col > 0):
                    editors_array.append(col)

        # randomly pick an editor
        editor_id = random.choice(editors_array)


        add_manuscript = ("INSERT INTO manuscript "
                          "(author_personID,editor_personID,title,status,ricodeID,numPages,"
                          "startingPage,issueOrder,dateReceived,dateSentForReview,dateAccepted,"
                          "issue_publicationYear,issue_periodNumber) "
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

        print("Submitted and updated:\n"
              "  Manuscript ID is " + str(manuscript_id) + "\n"
              "  Manuscript SUBMITTED on " + now.strftime("%Y-%m-%d") + " \n")


        # add secondary authors (if any)
        i = 1
        num_secondary_authors = len(tokens) - 4

        while i <= num_secondary_authors:
            add_SA, data_SA = insert_secondaryAuthors(manuscript_id, tokens[i+3], i)
            cursor.execute(add_SA, data_SA)
            i += 1

        con.commit()


    # immediately remove manuscript, regardless of status
    elif command == 'retract':
        manuscript_num = tokens[1]

        # ensure that author can only retract his/her own manuscripts
        query = "SELECT manuscriptID, author_personID FROM manuscript WHERE author_personID = " +  str(db.user_id) + " AND manuscriptID = " + str(manuscript_num) + ';'
        cursor.execute(query)

        if not cursor.fetchone():
            print("Sorry, you are not the author of this manuscript.")
            return

        s = raw_input('Are you sure? (y/n): ')
        if s.lower() == 'y':
            query = "DELETE FROM manuscript WHERE manuscriptID = " + str(manuscript_num) + ';'
            get_cursor_results(db, query)

            query = "DELETE FROM feedback WHERE manuscriptID = " + str(manuscript_num) + ';'
            get_cursor_results(db, query)

            print("Manuscript {} has been deleted".format(manuscript_num))

            con.commit()

        else:
            print("No action taken.")

    else:
        print("Invalid input. Command '" + command + "' not recognized.")



def process_editor(db, tokens):
    command = tokens[0]

    now     = datetime.datetime.now()

    con     = db.get_con()
    cursor  = db.get_cursor()

    if command == 'status':
        status_editor(db, db.user_id)

    elif command == 'assign' and len(tokens) == 3:
        manuscript_num = tokens[1]
        reviewer_id = tokens[2]

        # check to make sure that RICode matches
        getManuscriptRICode = "SELECT ricodeID FROM manuscript WHERE manuscriptID = " + str(manuscript_num) + ';'
        manuscriptRICode    = get_single_query(db, getManuscriptRICode)

        getReviewerRICodes  = "SELECT RICode_RICodeID  from reviewer_has_RICode WHERE reviewer_personID = " + str(reviewer_id) + ';'
        cursor.execute(getReviewerRICodes)

        reviewerRICodes = []

        for row in cursor:
            for col in row:
                if(col > 0):
                    reviewerRICodes.append(col)

        # print("Reviewer RICodes are " + str(reviewerRICodes))
        # print("Manuscript RICode is " + str(manuscriptRICode))

        if manuscriptRICode in reviewerRICodes:

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
                            "(manuscriptID,reviewer_personID,appropriateness,clarity,methodology,"
                            "contribution,recommendation,dateReceived) VALUES "
                            "(%(manuscriptID)s, %(reviewer_personID)s, NULL, NULL, NULL, NULL, NULL, %(dateReceived)s)")

            data_feedback = {
                'manuscriptID': manuscript_num,
                'reviewer_personID': reviewer_id,
                'dateReceived': date,
            }

            cursor.execute(add_feedback, data_feedback)

            query = "UPDATE manuscript SET `status` = 'underReview', dateSentForReview = NOW() WHERE manuscriptID = " + str(manuscript_num) + ';'
            cursor.execute(query)
            # date received?
            # insert_feedback = ""
            print("Manuscript ID {} assigned to reviewer {}. Manuscript status set to 'underReview'.".format(manuscript_num, reviewer_id))

            con.commit()
        else:
            print("Invalid entry. This reviewer does not have the appropriate RICode.")

    elif command == 'reject' and len(tokens) == 2:
        manuscript_num  = tokens[1]
        # TODO: add column in manuscript for date rejected
        query = "UPDATE manuscript SET `status` = 'rejected' WHERE manuscriptID = " + str(manuscript_num) + ';'
        cursor.execute(query)
        con.commit()
        print("Manuscript {} rejected on {}").format(manuscript_num, now.strftime("%Y-%m-%d"))

    elif command == 'accept' and len(tokens) == 2:
        manuscript_num  = tokens[1]
        query = "UPDATE manuscript SET `status` = 'accepted', dateAccepted = NOW() WHERE manuscriptID = " + str(manuscript_num) + ';'
        cursor.execute(query)
        con.commit()
        print("Manuscript {} accepted on {}").format(manuscript_num, now.strftime("%Y-%m-%d"))

    elif command == 'typeset' and len(tokens) == 3:
        manuscript_num  = tokens[1]
        pp              = tokens[2]

        query = "UPDATE manuscript SET `status` = 'typeset', numPages = {} WHERE manuscriptID = {};".format(pp, manuscript_num)
        cursor.execute(query)
        con.commit()
        print("Manuscript {} status set to 'typeset' on {}. {} pages logged").format(manuscript_num, now.strftime("%Y-%m-%d"), pp)

    elif command == 'schedule' and len(tokens) == 4:
        manuscript_num  = tokens[1]
        issueYear       = tokens[2]
        issuePeriod     = tokens[3]

        getNumPages = "SELECT numPages FROM manuscript WHERE issue_publicationYear = {} AND issue_periodNumber = {};".format(issueYear, issuePeriod)
        cursor.execute(getNumPages)

        page_sum = 0

        for row in cursor:
            for col in row:
                if col > 0:
                    page_sum += int(col)

        getNumManuscriptPage = "SELECT numPages FROM manuscript WHERE manuscriptID = {}".format(manuscript_num)
        page = get_single_query(db, getNumManuscriptPage)

        # ensure that we do not exceed 100 pages per issue
        if page and (page + page_sum <= 100):
            query = "UPDATE manuscript SET status = 'scheduled', issue_publicationYear = {}, issue_periodNumber = {} WHERE manuscriptID = {};".format(issueYear, issuePeriod, manuscript_num)
            cursor.execute(query)
            con.commit()
            print("Manuscript {} scheduled for issue year {}, period {}").format(manuscript_num, issueYear, issuePeriod)
        else:
            print("Invalid entry. Check if manuscript {} has a valid number of pages or number of pages in issue does not have any errors.".format(manuscript_num))


    elif command == 'publish' and len(tokens) == 3:
        issueYear    = tokens[1]
        issuePeriod  = tokens[2]

        query = "UPDATE manuscript SET status = 'published' WHERE issue_publicationYear = {} AND issue_periodNumber = {};".format(issueYear, issuePeriod)
        cursor.execute(query)

        query = "UPDATE issue SET datePrinted = NOW() WHERE publicationYear = {} AND periodNumber = {};".format(issueYear, issuePeriod)
        cursor.execute(query)

        con.commit()
        print("Issue year {}, period {} printed on {}. Status of all corresponding manuscripts changed to 'published'").format(issueYear, issuePeriod, now.strftime("%Y-%m-%d"))

    else:
        print("Invalid input. Command '" + command + "' not recognized, or corresponding arguments are not correct")

def submit_feedback(db, manuscript_num, appropriateness, clarity, methodology, contribution, recommendation, new_status):

    con     = db.get_con()
    cursor  = db.get_cursor()

    getManuscripts  = "SELECT manuscriptID from manuscriptWReviewers WHERE reviewer_personID = " + str(db.user_id) + ';'
    cursor.execute(getManuscripts)

    manuscripts = []

    for row in cursor:
        for col in row:
            if(col > 0):
                manuscripts.append(int(col))

    # print "manuscript nums are " + str(manuscripts)
    # print "manuscript is " + str(manuscript_num)
    getManuscriptStatus  = "SELECT `status` from manuscript WHERE manuscriptID = " + str(manuscript_num) + ';'
    check_status = get_single_query(db, getManuscriptStatus)

    # print "Test " + str(int(manuscript_num) in manuscripts)
    # print "Check status is " + str(check_status)

    if (int(manuscript_num) in manuscripts) and (check_status == "underReview"):
        getDate = "SELECT dateReceived FROM manuscript WHERE manuscriptID = " + str(manuscript_num) + ';'
        date = get_single_query(db, getDate)

        update_feedback = ("UPDATE feedback "
                           "SET appropriateness = %(appropriateness)s, "
                           "clarity = %(clarity)s, "
                           "methodology = %(methodology)s, "
                           "contribution = %(contribution)s, "
                           "recommendation = %(recommendation)s, "
                           "dateReceived = %(dateReceived)s"
                           "WHERE manuscriptID = %(manuscriptID)s AND reviewer_personID = %(reviewer_personID)s")

        data_feedback = {
            'appropriateness': appropriateness,
            'clarity': clarity,
            'methodology': methodology,
            'contribution': contribution,
            'recommendation': recommendation,
            'dateReceived': date,
            'manuscriptID': manuscript_num,
            'reviewer_personID': db.user_id
        }

        cursor.execute(update_feedback, data_feedback)

        if(new_status == "rejected"):
            print "rejected"
            query = "UPDATE manuscript SET `status` = 'rejected' WHERE manuscriptID = {};".format(manuscript_num)
        elif(new_status == "accepted"):
            print "accepted"
            query = "UPDATE manuscript SET `status` = 'accepted', dateAccepted = NOW() WHERE manuscriptID = {};".format(manuscript_num)

        cursor.execute(query)

        con.commit()
        print("Feedback for manuscript {} recorded. Status set to {}").format(manuscript_num, new_status)

    else:
        print("User cannot review this manuscript at this time.")

def process_reviewer(db, tokens):
    command = tokens[0]

    con     = db.get_con()
    cursor  = db.get_cursor()

    if command == 'status' and len(tokens) == 1:
        status_reviewer(db, db.user_id)

    elif command == 'resign' and len(tokens) == 1:
        # prompt to enter unique ID

        s = raw_input('Please enter your user ID to confirm: ')
        if s == str(db.user_id):
            query = "DELETE FROM reviewer WHERE personID = " + str(db.user_id) + ';'
            cursor.execute(query)
            print("Thank you for your service!")
            con.commit()

        else:
            print("No action taken. User ID does not match")

        # TODO: remove user from system (invoke trigger)
    elif command == 'reject':
        manuscript_num  = tokens[1]
        appropriateness = tokens[2]
        clarity         = tokens[3]
        methodology     = tokens[4]
        contribution    = tokens[5]
        recommendation  = tokens[6]

        submit_feedback(db, manuscript_num, appropriateness, clarity, methodology, contribution, recommendation, 'rejected')

    elif command == 'accept':
        manuscript_num  = tokens[1]
        appropriateness = tokens[2]
        clarity         = tokens[3]
        methodology     = tokens[4]
        contribution    = tokens[5]
        recommendation  = tokens[6]

        submit_feedback(db, manuscript_num, appropriateness, clarity, methodology, contribution, recommendation, 'accepted')

    else:
        print("Invalid input. Command '" + command + "' not recognized or arguments are not appropriate.")

def status_query_return(db, query):
    cursor = db.get_cursor()
    cursor.execute(query)

    # display results
    for row in cursor:
        for col in row:
            if col > 0:
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

    # TODO: typesetting (status = typeset?)

    query = "SELECT count FROM authorNumScheduled WHERE personID = " +  str(author_id) + ';'
    print("{} manuscripts scheduled".format(status_query_return(db, query)))

    query = "SELECT count FROM authorNumPublished WHERE personID = " +  str(author_id) + ';'
    print("{} manuscripts published\n".format(status_query_return(db, query)))


def status_editor(db, editor_id):

    cursor = db.get_cursor()
    query = "SELECT status, manuscriptID, title FROM manuscript WHERE editor_personID = {} ORDER BY status, manuscriptID".format(editor_id)
    # query = "SELECT status, manuscriptID, title FROM manuscript ORDER BY status, manuscriptID"
    cursor.execute(query)

    print("Here are your current manuscripts: ")
    for (status, manuscriptID, title) in cursor:
        print("   ID {} -- status: {}: '{}' ".format(manuscriptID, status, title))

def status_reviewer(db, reviewer_id):

    cursor = db.get_cursor()
    # select * from manuscriptWReviewers WHERE reviewer_personID = 422;
    query = "SELECT status, manuscriptID, title FROM manuscriptWReviewers WHERE reviewer_personID = {}".format(reviewer_id)
    # query = "SELECT status, manuscriptID, title FROM manuscript ORDER BY status, manuscriptID"
    cursor.execute(query)

    print("Here are your current manuscripts: ")
    for (status, manuscriptID, title) in cursor:
        print("   ID {} -- status: {}: '{}' ".format(manuscriptID, status, title))
