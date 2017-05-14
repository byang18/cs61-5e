# Barry Yang and Lily Xu
# CS 61 Databases
# Lab 2 part e
# May 12, 2017

# helper functions for database execution


import datetime         # get current date
import random
import getpass          # raw_input substitute for passwords
from random import randint

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
        output = output[:-1] + '\n'

    return output


def insert_query(db, query, data):
    con    = db.get_con()
    cursor = db.get_cursor()
    cursor.execute(query, data)
    con.commit()

    return cursor.lastrowid

# single query, useful for update and delete
def change_query(db, query):
    con     = db.get_con()
    cursor  = db.get_cursor()
    cursor.execute(query)
    con.commit()


# parse input from user
# process command if 'login' or 'register'
# call appropriate function to process command for author, editor, or reviewer
def parse_input(db, string):
    tokens = string.strip().split('|')

    if len(tokens) == 0:
        print("ERROR: Invalid input. Query cannot be blank.")
        return

    # log in user
    if tokens[0] == 'login' and len(tokens) > 1:
        user_id = tokens[1]
        return login(db, user_id)
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
        print("ERROR: Invalid input. Please login or register.")


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
        login_check, pw = login_authenticate(db, user_id)
        if not login_check:
            if(pw != "no password"):
                print("Incorrect password.")
            return

        print "LOGIN USER: " + "team17_" + str(user_id)
        print "PASSWORD : " + pw

        store_info = ["team17_" + str(user_id), str(pw), str(user_id), "author"]

        results = submit_query_return(db, query)
        results = results.strip().split('|')

        print("\nWelcome back, author " + str(user_id) + "! Here's what we have stored about you:")
        print("  First name: " + results[0])
        print("  Last name:  " + results[1])
        print("  Address:    " + results[2])

        # execute login
        db.change_user_id(int(user_id))
        db.change_user_type('author')
        db.log_on()

        status_author(db, user_id)

        return store_info

    # is the user an editor?
    query = "SELECT fname, lname FROM editor JOIN person ON editor.personID " + \
            "= person.personID WHERE editor.personID = " + str(user_id) + ';'

    results = submit_query_return(db, query)

    if results != '':

        login_check, pw = login_authenticate(db, user_id)
        if not login_check:
            if(pw != "no password"):
                print("Incorrect password.")
            return

        print "LOGIN USER: " + "team17_" + str(user_id)
        print "PASSWORD : " + pw

        store_info = ["team17_" + str(user_id), str(pw), str(user_id), "editor"]

        results = submit_query_return(db, query)
        results = results.strip().split('|')

        print("\nWelcome back, editor " + str(user_id) + "! Here's what we have stored about you:")
        print("  First name: " + results[0])
        print("  Last name:  " + results[1])

        # execute login
        db.change_user_id(int(user_id))
        db.change_user_type('editor')
        db.log_on()

        status_editor(db, user_id)

        return store_info

    # is the user a reviewer?
    query = "SELECT fname, lname FROM reviewer JOIN person ON reviewer.personID " + \
            "= person.personID WHERE reviewer.personID = "+ str(user_id) + ';'

    results = submit_query_return(db, query)

    if results != '':
        login_check, pw = login_authenticate(db, user_id)

        if not login_check:
            if(pw != "no password"):
                print("Incorrect password.")
            return

        print "LOGIN USER: " + "team17_" + str(user_id)
        print "PASSWORD : " + pw

        store_info = ["team17_" + str(user_id), str(pw), str(user_id), "reviewer"]

        results = submit_query_return(db, query)
        results = results.strip().split('|')

        print("\nWelcome back, reviewer " + str(user_id) + "! Here's what we have stored about you:")
        print("  First name: " + results[0])
        print("  Last name:  " + results[1])

        # execute login
        db.change_user_id(int(user_id))
        db.change_user_type('reviewer')
        db.log_on()

        # TODO: everything should be limited to manuscripts assigned to that reviewer
        status_reviewer(db, user_id)

        return store_info

    # no user corresponds to given id
    print('ERROR: No user exists corresponding to ID ' + str(user_id) + '.')



# returns True if authentication was successful
# returns False otherwise
# if no password is setup, returns True
def login_authenticate(db, user_id):
    # check if user has an associated password
    query = 'SELECT * FROM credential WHERE personID = ' + str(user_id) + ';'

    result = get_single_query(db,query)

    # no associated password
    if not result:
        print("This user has no associated password. User may be locked (e.g. from resignation)")
        return (False, "no password")

    # request login from user
    print('Please enter your password:')
    pw = getpass.getpass('-->')

    # confirm validity of password
    query = 'SELECT * FROM credential WHERE personID = ' + str(user_id) + \
            ' AND AES_DECRYPT(pword, @master_key) = "' + pw + '";'
    result = get_single_query(db,query)

    # returns true if result is not none, otherwise return false
    return (result != None, pw)



# register a new user in the system
def register(db, tokens):
    user_type = tokens[1]

    if user_type == 'author':
        personID = register_author(db, tokens[2], tokens[3], tokens[4], tokens[5])

    elif user_type == 'editor':
        personID = register_editor(db, tokens[2], tokens[3])

    elif user_type == 'reviewer':
        if len(tokens) == 7:
            personID = register_reviewer(db, tokens[2], tokens[3], tokens[4], tokens[5], tokens[6])
        elif len(tokens) == 8:
            personID = register_reviewer(db, tokens[2], tokens[3], tokens[4], tokens[5], tokens[6], tokens[7])
        elif len(tokens) == 9:
            personID = register_reviewer(db, tokens[2], tokens[3], tokens[4], tokens[5], tokens[6], tokens[7], tokens[8])
        else:
            print("ERROR: Invalid input. Incorrect number of arguments.")
            return

    else:
        print("ERROR: User type " + user_type + " is invalid.")
        return

    # if the confidential setting is on, prompt for a password
    if db.is_confidential():
        print('Please enter a password.')
        pw = getpass.getpass('-->')

        query = 'INSERT INTO credential (personID, pword) VALUES (' + str(personID) + \
                ', AES_ENCRYPT("' + pw + '",@master_key));'

        change_query(db, query)

        # DROP USER IF EXISTS 'team17_300';
        # CREATE USER 'team17_300' IDENTIFIED BY 'password';

        query = "DROP USER IF EXISTS 'team17_" + str(personID) + "';"
        print "1st: " + query
        change_query(db, query)

        query = "CREATE USER 'team17_{}' IDENTIFIED BY '{}';".format(personID, pw)
        change_query(db, query)
        print "2nd: " + query

        query = "GRANT SELECT ON byang_db.authorNumSubmitted TO 'team17_{}';".format(personID)
        change_query(db, query)

        change_query(db, "FLUSH PRIVILEGES;")

        # prevent a view not created
        query = "DROP VIEW IF EXISTS view_as{};".format(personID)
        change_query(db, query)

        if user_type == 'author':

            # EXTRA CREDIT QUERY: INSERT to create a new manuscript
            query = "GRANT INSERT ON byang_db.manuscript TO 'team17_{}';".format(personID)
            change_query(db, query)

            query = "CREATE VIEW view_as{} AS SELECT author_personID, manuscriptID, status, title FROM manuscript WHERE author_personID = {};".format(personID, personID)
            change_query(db, query)

            # EXTRA CREDIT QUERY: SELECT only on Title and Status of authors own manuscripts
            query = "GRANT SELECT ON byang_db.view_as{} TO 'team17_{}';".format(personID, personID)
            change_query(db, query)

            # to help with SUBMIT
            query = "GRANT SELECT ON byang_db.editor TO 'team17_{}';".format(personID)
            change_query(db, query)

            query = "GRANT INSERT ON byang_db.secondaryAuthor TO 'team17_{}';".format(personID)
            change_query(db, query)

            query = "GRANT ALL PRIVILEGES ON byang_db.author TO 'team17_{}';".format(personID)
            change_query(db, query)

            # miscellaneous
            query = "GRANT SELECT ON byang_db.authorNumSubmitted TO 'team17_{}';".format(personID)
            change_query(db, query)

            query = "GRANT SELECT ON byang_db.authorNumUnderReview TO 'team17_{}';".format(personID)
            change_query(db, query)

            query = "GRANT SELECT ON byang_db.authorNumRejected TO 'team17_{}';".format(personID)
            change_query(db, query)

            query = "GRANT SELECT ON byang_db.authorNumAccepted TO 'team17_{}';".format(personID)
            change_query(db, query)

            query = "GRANT SELECT ON byang_db.authorNumTypeset TO 'team17_{}';".format(personID)
            change_query(db, query)

            query = "GRANT SELECT ON byang_db.authorNumScheduled TO 'team17_{}';".format(personID)
            change_query(db, query)

            query = "GRANT SELECT ON byang_db.authorNumPublished TO 'team17_{}';".format(personID)
            change_query(db, query)

        elif user_type == 'editor':

            # EXTRA CREDIT: query all access
            query = "GRANT ALL PRIVILEGES ON byang_db.* TO 'team17_{}';".format(personID)
            change_query(db, query)

        elif user_type == 'reviewer':

            query = ("CREATE VIEW view_as{} AS SELECT * FROM manuscript WHERE manuscriptID IN "
                     "(SELECT DISTINCT manuscript.manuscriptID FROM manuscript "
                     "JOIN feedback ON (manuscript.manuscriptID = feedback.manuscriptID) "
                     "WHERE reviewer_personID = {});").format(personID, personID)
            change_query(db, query)

            # EXTRA CREDIT QUERY: SELECT only manuscripts in which reviewer has view
            query = "GRANT SELECT ON byang_db.view_as{} TO 'team17_{}';".format(personID, personID)
            change_query(db, query)

            # EXTRA CREDIT QUERY: INSERT on feedback
            query = "GRANT INSERT ON byang_db.feedback TO 'team17_{}';".format(personID)
            change_query(db, query)

            # This makes sense, as reviewer should have right to look at, update, and insert new data.
            # A better way would've been to make a separate view
            query = "GRANT ALL PRIVILEGES ON byang_db.feedback TO 'team17_{}';".format(personID)
            change_query(db, query)

            # Helper to make other queries work
            query = "GRANT SELECT ON byang_db.manuscriptWReviewers TO 'team17_{}';".format(personID)
            change_query(db, query)

            query = "GRANT UPDATE ON byang_db.view_as{} TO 'team17_{}';".format(personID, personID)
            change_query(db, query)

            query = "GRANT UPDATE ON byang_db.manuscript TO 'team17_{}';".format(personID)
            change_query(db, query)

            query = "GRANT SELECT ON byang_db.manuscript TO 'team17_{}';".format(personID)
            change_query(db, query)

            query = "GRANT UPDATE ON byang_db.reviewer TO 'team17_{}';".format(personID)
            change_query(db, query)

            query = "GRANT UPDATE ON byang_db.credential TO 'team17_{}';".format(personID)
            change_query(db, query)

            query = "GRANT SELECT ON byang_db.reviewer TO 'team17_{}';".format(personID)
            change_query(db, query)

            query = "GRANT SELECT ON byang_db.credential TO 'team17_{}';".format(personID)
            change_query(db, query)

        print('User registered successfully')


def register_person(db, fname, lname):
    add_person = ('INSERT INTO person (fname,lname) VALUES (%s, %s);')

    data_add = (fname, lname)

    personID = insert_query(db, add_person, data_add)

    print("{} {} will be registered with ID {} ".format(fname, lname, str(personID)))

    return personID


# def create_user_db(db):
#
#     db.ge
#
#     query = "DROP USER IF EXISTS 'team17_" + str(db.user_id) + "'@'sunapee';"
#     cursor.


def register_author(db, fname, lname, email, address):

    # Over here insert the thing
    # DROP USER IF EXISTS 'team17_100'@'sunapee';
    # CREATE USER 'team17_100'@'sunapee' IDENTIFIED BY 'password';

    personID = register_person(db, fname, lname)

    add_author = ("INSERT INTO author "
                  "(personID,email,address,affiliation) "
                  "VALUES (%(personID)s, %(email)s, %(address)s, NULL)")

    data_author = {
        'personID': personID,
        'email': email,
        'address': address,
    }

    insert_query(db, add_author, data_author)

    return personID


def register_editor(db, fname, lname):
    personID = register_person(db, fname, lname)

    add_editor = ("INSERT INTO editor "
                  "(personID) "
                  "VALUES (%(personID)s)")

    data_editor = {
        'personID': personID
    }

    insert_query(db, add_editor, data_editor)

    return personID


def register_reviewer(db, fname, lname, email, affiliation, *ricodes):
    personID = register_person(db, fname, lname)

    add_reviewer = ("INSERT INTO reviewer "
                    "(personID,affiliation,email) "
                    "VALUES (%(personID)s, %(affiliation)s, %(email)s)")

    data_reviewer = {
        'personID': personID,
        'affiliation': affiliation,
        'email': email,
    }

    insert_query(db, add_reviewer, data_reviewer)

    for ricode in ricodes:
        add_reviewerRICode = ("INSERT INTO reviewer_has_RICode "
                              "(reviewer_personID,RICode_RICodeID) "
                              "VALUES (%(reviewer_personID)s, %(RICode_RICodeID)s)")
        data_reviewerRICode = {
            'reviewer_personID': personID,
            'RICode_RICodeID': ricode,
        }
        insert_query(db, add_reviewerRICode, data_reviewerRICode)

    return personID


def insert_secondaryAuthors(manuscript_id, name, order):
    names = name.split()

    add_SA = ("INSERT INTO secondaryAuthor "
              "(manuscriptID, authorOrder, fname, lname) "
              "VALUES (%s, %s, %s, %s)")

    data_SA = (manuscript_id, order, names[0], names[1])

    return add_SA, data_SA


def process_author(db, tokens):
    command = tokens[0]

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

        manuscript_id = insert_query(db, add_manuscript, data_author)

        update_affiliation = ("UPDATE author SET affiliation = %s WHERE personID = %s;")

        insert_query(db, update_affiliation, (affiliation, db.user_id))

        print("Submitted and updated:\n"
              "  Manuscript ID is " + str(manuscript_id) + "\n"
              "  Manuscript SUBMITTED on " + now.strftime("%Y-%m-%d") + " \n")


        # add secondary authors (if any)
        i = 1
        num_secondary_authors = len(tokens) - 4

        while i <= num_secondary_authors:
            add_SA, data_SA = insert_secondaryAuthors(manuscript_id, tokens[i+3], i)
            insert_query(db, add_SA, data_SA)
            i += 1


    # immediately remove manuscript, regardless of status
    elif command == 'retract':
        manuscript_num = tokens[1]

        # ensure that author can only retract his/her own manuscripts
        query = "SELECT manuscriptID, author_personID FROM manuscript WHERE author_personID = " +  str(db.user_id) + " AND manuscriptID = " + str(manuscript_num) + ';'
        result = get_single_query(db, query)

        if not result:
            print("Sorry, you are not the author of this manuscript.")
            return

        s = raw_input('Are you sure? (y/n): ')
        if s.lower() == 'y':
            query = "DELETE FROM manuscript WHERE manuscriptID = " + str(manuscript_num) + ';'
            change_query(db, query)

            query = "DELETE FROM feedback WHERE manuscriptID = " + str(manuscript_num) + ';'
            change_query(db, query)

            print("Manuscript {} has been deleted".format(manuscript_num))

        else:
            print("No action taken.")

    else:
        print("ERROR: Invalid input. Command '" + command + "' not recognized.")



def process_editor(db, tokens):
    command = tokens[0]

    now     = datetime.datetime.now()
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
                if col > 0:
                    reviewerRICodes.append(col)

        if manuscriptRICode in reviewerRICodes:

            getDate = "SELECT dateReceived FROM manuscript WHERE manuscriptID = " + str(manuscript_num) + ';'

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

            insert_query(db, add_feedback, data_feedback)

            query = "UPDATE manuscript SET `status` = 'underReview', dateSentForReview = NOW() WHERE manuscriptID = " + str(manuscript_num) + ';'
            change_query(db, query)
            # date received?
            # insert_feedback = ""
            print("Manuscript ID {} assigned to reviewer {}. Manuscript status set to 'underReview'.".format(manuscript_num, reviewer_id))
        else:
            print("ERROR: Invalid entry. This reviewer does not have the appropriate RICode.")

    elif command == 'reject' and len(tokens) == 2:
        manuscript_num  = tokens[1]
        query = "UPDATE manuscript SET `status` = 'rejected' WHERE manuscriptID = " + str(manuscript_num) + ';'
        change_query(db, query)
        print("Manuscript {} rejected on {}").format(manuscript_num, now.strftime("%Y-%m-%d"))

    elif command == 'accept' and len(tokens) == 2:
        manuscript_num  = tokens[1]
        query = "UPDATE manuscript SET `status` = 'accepted', dateAccepted = NOW() WHERE manuscriptID = " + str(manuscript_num) + ';'
        change_query(db, query)
        print("Manuscript {} accepted on {}").format(manuscript_num, now.strftime("%Y-%m-%d"))

    elif command == 'typeset' and len(tokens) == 3:
        manuscript_num = tokens[1]
        pp             = tokens[2]

        query = "UPDATE manuscript SET `status` = 'typeset', numPages = {} WHERE manuscriptID = {};".format(pp, manuscript_num)
        change_query(db, query)
        print("Manuscript {} status set to 'typeset' on {}. {} pages logged").format(manuscript_num, now.strftime("%Y-%m-%d"), pp)

    elif command == 'schedule' and len(tokens) == 4:
        manuscript_num = tokens[1]
        issueYear      = tokens[2]
        issuePeriod    = tokens[3]

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
            change_query(db, query)

            print("Manuscript {} scheduled for issue year {}, period {}").format(manuscript_num, issueYear, issuePeriod)
        else:
            print("ERROR: Invalid entry. Check if manuscript {} has a valid number of pages or number of pages in issue does not have any errors.".format(manuscript_num))


    elif command == 'publish' and len(tokens) == 3:
        issueYear   = tokens[1]
        issuePeriod = tokens[2]

        query = "UPDATE manuscript SET status = 'published' WHERE issue_publicationYear = {} AND issue_periodNumber = {};".format(issueYear, issuePeriod)
        change_query(db, query)

        query = "UPDATE issue SET datePrinted = NOW() WHERE publicationYear = {} AND periodNumber = {};".format(issueYear, issuePeriod)
        change_query(db, query)

        print("Issue year {}, period {} printed on {}. Status of all corresponding manuscripts changed to 'published'").format(issueYear, issuePeriod, now.strftime("%Y-%m-%d"))

    else:
        print("ERROR: Invalid input. Command '" + command + "' not recognized, or corresponding arguments are not correct")



def submit_feedback(db, manuscript_num, appropriateness, clarity, methodology, contribution, recommendation, new_status):

    cursor = db.get_cursor()

    getManuscripts  = "SELECT manuscriptID from manuscriptWReviewers WHERE reviewer_personID = " + str(db.user_id) + ';'
    cursor.execute(getManuscripts)

    manuscripts = []

    for row in cursor:
        for col in row:
            if col > 0:
                manuscripts.append(int(col))

    getManuscriptStatus  = "SELECT `status` from byang_db.view_as{} WHERE manuscriptID = ".format(db.user_id) + str(manuscript_num) + ';'
    check_status = get_single_query(db, getManuscriptStatus)

    if (int(manuscript_num) in manuscripts) and (check_status == "underReview"):
        getDate = "SELECT dateReceived FROM byang_db.view_as{} WHERE manuscriptID = ".format(db.user_id) + str(manuscript_num) + ';'
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

        insert_query(db, update_feedback, data_feedback)

        if new_status == "rejected":
            query = "UPDATE manuscript SET `status` = 'rejected' WHERE manuscriptID = {};".format(manuscript_num)
        elif new_status == "accepted":
            query = "UPDATE manuscript SET `status` = 'accepted', dateAccepted = NOW() WHERE manuscriptID = {};".format(manuscript_num)

        change_query(db, query)

        print("Feedback for manuscript {} recorded. Status set to {}").format(manuscript_num, new_status)

    else:
        print("User cannot review this manuscript at this time.")



def process_reviewer(db, tokens):
    command = tokens[0]

    if command == 'status' and len(tokens) == 1:
        status_reviewer(db, db.user_id)

    elif command == 'resign' and len(tokens) == 1:
        # prompt to enter unique ID
        s = raw_input('Please enter your user ID to confirm: ')
        if s == str(db.user_id):
            # UPDATE reviewer SET reviewer_status = "resigned" WHERE personID = 416;
            query = "UPDATE reviewer SET reviewer_status = 'resigned' WHERE personID = " + str(db.user_id) + ';'
            change_query(db, query)

            random_num = randint(0,1000)

            # locks the user by creating a random password
            query = 'UPDATE credential SET pword = AES_ENCRYPT("{}",@master_key) WHERE personID = {};'.format(str(random_num), str(db.user_id))
            print query
            change_query(db, query)

            print("Thank you for your service!")

            db.log_off()

        else:
            print("No action taken. User ID does not match.")

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
        print("ERROR: Invalid input. Command '" + command + "' not recognized or arguments are not appropriate.")


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
    query = "SELECT count FROM authorNumSubmitted WHERE personID = " +  str(author_id) + ';'
    print("{} manuscripts submitted".format(status_query_return(db, query)))

    query = "SELECT count FROM authorNumUnderReview WHERE personID = " +  str(author_id) + ';'
    print("{} manuscripts under review".format(status_query_return(db, query)))

    query = "SELECT count FROM authorNumRejected WHERE personID = " +  str(author_id) + ';'
    print("{} manuscripts rejected".format(status_query_return(db, query)))

    query = "SELECT count FROM authorNumAccepted WHERE personID = " +  str(author_id) + ';'
    print("{} manuscripts accepted".format(status_query_return(db, query)))

    query = "SELECT count FROM authorNumTypeset WHERE personID = " +  str(author_id) + ';'
    print("{} manuscripts typeset".format(status_query_return(db, query)))

    query = "SELECT count FROM authorNumScheduled WHERE personID = " +  str(author_id) + ';'
    print("{} manuscripts scheduled".format(status_query_return(db, query)))

    query = "SELECT count FROM authorNumPublished WHERE personID = " +  str(author_id) + ';'
    print("{} manuscripts published\n".format(status_query_return(db, query)))

    query = "SELECT status, manuscriptID, title FROM byang_db.view_as{} ORDER BY status, manuscriptID".format(author_id)
    display_manuscripts(db, query)


def status_editor(db, editor_id):
    query = "SELECT status, manuscriptID, title FROM manuscript WHERE editor_personID = {} ORDER BY status, manuscriptID".format(editor_id)
    display_manuscripts(db, query)


def status_reviewer(db, reviewer_id):
    query = "SELECT status, manuscriptID, title FROM manuscriptWReviewers WHERE reviewer_personID = {}".format(reviewer_id)
    display_manuscripts(db, query)


def display_manuscripts(db, query):
    result = submit_query_return(db, query)

    if result:
        print("Manuscript detail: ")
        rows = result.strip().split('\n')
        for row in rows:
            cols         = row.strip().split('|')
            status       = cols[0]
            manuscriptID = cols[1]
            title        = cols[2]
            print("   ID {} -- status: {}: '{}' ".format(manuscriptID, status, title))
    else:
        print("You have no manuscripts at this time.")
