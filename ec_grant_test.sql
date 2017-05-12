-- these should be triggered every time a new user is created!

-- helpful webpage with short examples: 
-- https://www.digitalocean.com/community/tutorials/how-to-create-a-new-user-and-grant-permissions-in-mysql


-- author
DROP USER IF EXISTS 'team17_100'@'sunapee';
CREATE USER 'team17_100'@'sunapee';

GRANT INSERT ON lilyx_db.manuscript TO 'team17_100'@'sunapee';
GRANT SELECT ON lilyx_db.manuscript TO 'team17_100'@'sunapee'; -- if author is author of manuscript

-- reload all privileges
FLUSH PRIVILEGES;


-- manuscript: SELECT (title and status of author's own) and INSERT
-- review: no access


-- editor
-- manuscript access grant: ALL access
-- review access grant: ALL access

DROP USER IF EXISTS 'team17_300'@'sunapee';
CREATE USER 'team17_300'@'sunapee';

GRANT ALL PRIVILEGES ON lilyx_db.manuscript TO 'team17_300'@'sunapee';
GRANT ALL PRIVILEGES ON lilyx_db.feedback TO 'team17_300'@'sunapee';


-- reviewer
-- manuscript: SELECT only on manuscripts assigned to this reviewer
-- review: INSERT 


DROP USER IF EXISTS 'team17_400'@'sunapee';
CREATE USER 'team17_400'@'sunapee';

GRANT SELECT ON lilyx_db.manuscript TO 'team17_400'@'sunapee'; -- if manuscript assigned to this reviewer
GRANT ALL PRIVILEGES ON lilyx_db.feedback TO 'team17_400'@'sunapee';


-- when a reviewer resigns, the reviewer’s id should be locked 
-- (i.e., no longer be able to login).
-- clarify above point:
-- Ensure that a resigned reviewer can no longer login, 
-- but all the information about that reviewer and any completed 
-- reviews is retained.




