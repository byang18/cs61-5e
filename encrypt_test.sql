-- PART E EXTRA CREDIT

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';


-- -----------------------------------------------------
-- Schema lilyx_db
-- -----------------------------------------------------
USE `lilyx_db`;




DROP TABLE IF EXISTS `credential`;      -- PART E EXTRA CREDIT
CREATE TABLE IF NOT EXISTS `lilyx_db`.`credential` (
  `personID` INT NOT NULL AUTO_INCREMENT,
  `pword` VARCHAR(30) NOT NULL,
  PRIMARY KEY (`personID`))
ENGINE = InnoDB;

SET @key_str = UNHEX('F3229A0B371ED2D9441B830D21A390C3');
SELECT @key_str;



DROP FUNCTION BLOB2TXT;
DELIMITER $$

CREATE FUNCTION BLOB2TXT (blobfield VARCHAR(255)) RETURNS longtext
DETERMINISTIC
NO SQL
BEGIN
       RETURN CAST(blobfield AS CHAR(100) CHARACTER SET utf8);
END
$$

DELIMITER ;

SELECT BLOB2TXT (UNHEX('F3229A0B371ED2D9441B830D21A390C3'));
SELECT BLOB2TXT (UNHEX('hellothere'));

-- SELECT CONVERT(* USING utf8) FROM ((SELECT UNHEX('hellotherehowareyou')) AS newtable);

SELECT UNHEX('xhellotherehowareyou') AS newtable;

SELECT UNHEX('xhellotherehowareyou');

INSERT INTO credential(personID, pword) VALUES (10, AES_ENCRYPT("barry",@key_str));
INSERT INTO credential(personID, pword) VALUES (14, AES_ENCRYPT("lily",@key_ssdfsftr));
INSERT INTO credential(personID, pword) VALUES (12, AES_ENCRYPT("pinocchio",@key_str));

SELECT * FROM credential WHERE pword = AES_ENCRYPT("hi",@key_str);

SELECT * FROM credential WHERE pword = AES_ENCRYPT("hi",@key_stxsdfr);


SELECT * FROM credential WHERE AES_DECRYPT(pword, @key_str) = "lily";




-- Encryption algorithm; can be 'DSA' or 'DH' instead
SET @algo = 'RSA';
-- Key length in bits; make larger for stronger keys
SET @key_len = 245;

CREATE FUNCTION create_asymmetric_priv_key RETURNS STRING
  SONAME 'openssl_udf.so';
CREATE FUNCTION create_asymmetric_pub_key RETURNS STRING
  SONAME 'openssl_udf.so';


-- Create private key
SET @priv = create_asymmetric_priv_key('DSA', 2048);
-- SET @priv = create_asymmetric_priv_key(@algo, @key_len);
-- Derive corresponding public key from private key, using same algorithm
SET @pub = create_asymmetric_pub_key(@algo, @priv);


SET @ciphertext = ASYMMETRIC_ENCRYPT(@algo, 'My secret text', @priv);
SET @cleartext = ASYMMETRIC_DECRYPT(@algo, @ciphertext, @pub);

DROP FUNCTION create_asymmetric_priv_key;
DROP FUNCTION create_asymmetric_pub_key;




DELIMITER /

CREATE TRIGGER encrypt_password 
BEFORE INSERT ON credential
FOR EACH ROW
BEGIN
    SET NEW.password = ASYMMETRIC_ENCRYPT(@algo, NEW.password, @priv);
END
/

-- restore delimiter
DELIMITER ;
