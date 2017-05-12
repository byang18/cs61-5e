-- PART E EXTRA CREDIT


DROP TABLE IF EXISTS `credential`;      -- PART E EXTRA CREDIT
CREATE TABLE IF NOT EXISTS `byang_db`.`credential` (
  `personID` INT NOT NULL AUTO_INCREMENT,
  `password` VARCHAR(30) NOT NULL,
  PRIMARY KEY (`personID`))
ENGINE = InnoDB;


-- Encryption algorithm; can be 'DSA' or 'DH' instead
SET @algo = 'RSA';
-- Key length in bits; make larger for stronger keys
SET @key_len = 1024;

-- Create private key
SET @priv = CREATE_ASYMMETRIC_PRIV_KEY(@algo, @key_len);
-- Derive corresponding public key from private key, using same algorithm
SET @pub = CREATE_ASYMMETRIC_PUB_KEY(@algo, @priv);


SET @ciphertext = ASYMMETRIC_ENCRYPT(@algo, 'My secret text', @priv);
SET @cleartext = ASYMMETRIC_DECRYPT(@algo, @ciphertext, @pub);





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
