Barry Yang and Lily Xu
CS 61 Databases
Lab 2 part e
May 12, 2017


# Running the code

Execute `setup.sql` and `triggers.sql`

In the command line, type:
```
db_driver.py
```



# Commands
Log in
```
login|<id>
```


### Author
```
register|author|<fname>|<lname>|<email>|<address>
submit|<title>|<affiliation>|<RICode>|<author2>|<author3>|<author4>
status
retract|<manuscript_id>
```


### Editor
```
register|editor|<fname>|<lname>
status
assign|<manuscript_id>|<reviewer_id>
reject|<manuscript_id>
accept|<manuscript_id>
typeset|<manuscript_id>|<pp>
schedule|<manuscript_id>|<issue>
publish|<issue_year>|<issue_period>
```


### Reviewer
```
register|reviewer|<fname>|<lname>|<RICode1>|<RICode2>|<RICode3>
status
resign
reject|<manuscriptID>|<appropriateness>|<clarity>|<methodology>|<contribution>
accept|<manuscriptID>|<appropriateness>|<clarity>|<methodology>|<contribution>
```

# Extra Credit

### Password authentication

### Authorization using `GRANT`


