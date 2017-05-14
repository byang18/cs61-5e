user_id = 34
random_num = 4

query = "Table 'byang_db.view_as430' doesn't exist"
print query[-13:]

#query = "UPDATE reviewer SET reviewer_status = 'resigned' WHERE personID = " + str(db.user_id) + ';'

# query = 'UPDATE credential SET pword = AES_ENCRYPT("{}",@master_key) WHERE personID = {};'.format(str(random_num), str(user_id))
# print query
