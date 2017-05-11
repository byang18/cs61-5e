-- Barry Yang and Lily Xu
-- CS 61 Databases
-- Lab 2 part d
-- May 5, 2017

-- this SQL script defines two specified triggers


-- -----------------------------------------------------
-- helper views, used for trigger 2
-- -----------------------------------------------------

DROP VIEW IF EXISTS mWThreeReviewers;

-- select manuscripts that have three or fewer reviewers
-- aliasing
CREATE VIEW mWThreeReviewers AS
SELECT manuscriptID
FROM countReviewers
WHERE reviewerCount <= 3;


DROP VIEW IF EXISTS onlyThreeReviewers;

-- obtain names of reviewers
CREATE VIEW onlyThreeReviewers AS
SELECT mWThreeReviewers.manuscriptID AS manuscriptID, feedback.reviewer_personID AS reviewer_personID
FROM mWThreeReviewers
JOIN feedback ON mWThreeReviewers.manuscriptID = feedback.manuscriptID
ORDER BY manuscriptID;




DROP TRIGGER IF EXISTS no_available_reviewer;
DROP TRIGGER IF EXISTS reviewer_resign;

SET FOREIGN_KEY_CHECKS=0;


-- -----------------------------------------------------
-- Trigger 1
-- -----------------------------------------------------
-- When an author is submitting a new manuscript to the system with 
-- an RICode for which there are not at least three reviewers who handle that 
-- RICode, you should raise an exception that informs the author the paper can
-- not be considered at this time.


DELIMITER /

CREATE TRIGGER no_available_reviewer 
BEFORE INSERT ON manuscript
FOR EACH ROW
BEGIN
    DECLARE num_reviewers INT;
    DECLARE signal_message VARCHAR(128);
    SET signal_message = 'We do not have three reviewers with the corresponding RICode.';
    
    SELECT COUNT(*) INTO num_reviewers FROM reviewer_has_RICode 
           WHERE RICode_RICodeID = new.ricodeID;
    
    IF num_reviewers < 3 THEN
        -- MySQL defines SQLSTATE 45000 as "unhandled user-defined exception"
        SIGNAL SQLSTATE '45000' SET message_text = signal_message;
    END IF;
END
/


-- -----------------------------------------------------
-- Trigger 2
-- -----------------------------------------------------
-- When a reviewer resigns any manuscript in “underReview” state for which 
-- that reviewer was the only reviewer, that manuscript must be reset to 
-- “submitted” state and an apprpriate exception message displayed.


CREATE TRIGGER reviewer_resign
BEFORE DELETE ON reviewer
FOR EACH ROW
BEGIN
    IF (EXISTS (SELECT reviewer_personID FROM onlyOneReviewer
                WHERE reviewer_personID = old.personID))
        THEN
        UPDATE manuscript
        SET manuscript.`status` = "submitted"
        WHERE manuscript.manuscriptID
        IN (SELECT manuscriptID FROM onlyThreeReviewers WHERE reviewer_personID = old.personID);
    END IF;
    
    DELETE FROM `feedback` WHERE reviewer_personID = old.personID;
    DELETE FROM `reviewer_has_RICode` WHERE reviewer_personID = old.personID;
END
/


-- restore delimiter
DELIMITER ;

