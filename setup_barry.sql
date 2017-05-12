-- Barry Yang and Lily Xu
-- CS 61 Databases
-- Lab 2 part d
-- May 5, 2017

-- this SQL script sets up the database for testing triggers



-- -----------------------------------------------------
-- generate tables
-- -----------------------------------------------------

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';


-- -----------------------------------------------------
-- Schema byang_db
-- -----------------------------------------------------
USE `byang_db` ;


-- DROP statements
DROP TABLE IF EXISTS `feedback`;
DROP TABLE IF EXISTS `reviewer_has_RICode`;
DROP TABLE IF EXISTS `secondaryAuthor`;
DROP TABLE IF EXISTS `reviewer`;-- 
DROP TABLE IF EXISTS `manuscript`;
DROP TABLE IF EXISTS `author`;
DROP TABLE IF EXISTS `editor`;
DROP TABLE IF EXISTS `person`;
DROP TABLE IF EXISTS `RICode`;
DROP TABLE IF EXISTS `issue`;


-- person table
CREATE TABLE IF NOT EXISTS `byang_db`.`person` (
  `personID` INT NOT NULL AUTO_INCREMENT,
  `fname` VARCHAR(30) NOT NULL,
  `lname` VARCHAR(30) NOT NULL,
  PRIMARY KEY (`personID`))
ENGINE = InnoDB;


-- author table
CREATE TABLE IF NOT EXISTS `byang_db`.`author` (
  `personID` INT NOT NULL,
  `email` VARCHAR(80) NOT NULL,
  `address` VARCHAR(45) NOT NULL,
  `affiliation` VARCHAR(45) NULL,
  PRIMARY KEY (`personID`),
  CONSTRAINT `fk_author_person`
    FOREIGN KEY (`personID`)
    REFERENCES `byang_db`.`person` (`personID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- editor table
CREATE TABLE IF NOT EXISTS `byang_db`.`editor` (
  `personID` INT NOT NULL,
  PRIMARY KEY (`personID`),
  CONSTRAINT `fk_editor_person1`
    FOREIGN KEY (`personID`)
    REFERENCES `byang_db`.`person` (`personID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- reviewer table
CREATE TABLE IF NOT EXISTS `byang_db`.`reviewer` (
  `personID` INT NOT NULL,
  `affiliation` VARCHAR(45) NOT NULL,
  `email` VARCHAR(80) NOT NULL,
  PRIMARY KEY (`personID`),
  CONSTRAINT `fk_reviewer_person1`
    FOREIGN KEY (`personID`)
    REFERENCES `byang_db`.`person` (`personID`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- RICode table
CREATE TABLE IF NOT EXISTS `byang_db`.`RICode` (
  `RICodeID` MEDIUMINT NOT NULL AUTO_INCREMENT,
  `interest` VARCHAR(64) NOT NULL,
  PRIMARY KEY (`RICodeID`)) 
ENGINE = InnoDB;


-- issue table
CREATE TABLE IF NOT EXISTS `byang_db`.`issue` (
  `publicationYear` INT NOT NULL ,
  `periodNumber` INT NOT NULL,
  `datePrinted` DATE NULL,
  PRIMARY KEY (`publicationYear`, `periodNumber`)) 
ENGINE = InnoDB;


-- manuscript table
CREATE TABLE IF NOT EXISTS `byang_db`.`manuscript` (
  `manuscriptID` INT NOT NULL AUTO_INCREMENT,
  `author_personID` INT NOT NULL,
  `editor_personID` INT NOT NULL,
  `title` VARCHAR(100) NOT NULL,
  `status` VARCHAR(20) NOT NULL,
  `ricodeID` MEDIUMINT NOT NULL,
  `numPages` INT NULL,
  `startingPage` INT NULL,
  `issueOrder` INT NULL,
  `dateReceived` DATE NOT NULL,
  `dateSentForReview` DATE NULL,
  `dateAccepted` DATE NULL,
  `issue_publicationYear` INT NULL,
  `issue_periodNumber` INT NULL,
  PRIMARY KEY (`manuscriptID`),
  CONSTRAINT `fk_manuscript_RICode1`
    FOREIGN KEY (`ricodeID`)
    REFERENCES `byang_db`.`RICode` (`RICodeID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_manuscript_editor1`
    FOREIGN KEY (`editor_personID`)
    REFERENCES `byang_db`.`editor` (`personID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_manuscript_author1`
    FOREIGN KEY (`author_personID`)
    REFERENCES `byang_db`.`author` (`personID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_manuscript_issue1`
    FOREIGN KEY (`issue_publicationYear` , `issue_periodNumber`)
    REFERENCES `byang_db`.`issue` (`publicationYear` , `periodNumber`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- feedback table
CREATE TABLE IF NOT EXISTS `byang_db`.`feedback` (
  `manuscriptID` INT NOT NULL,
  `reviewer_personID` INT NOT NULL,
  `appropriateness` INT NULL,
  `clarity` INT NULL,
  `methodology` INT NULL,
  `contribution` INT NULL,
  `recommendation` TINYINT NULL,
  `dateReceived` DATE NULL,
  PRIMARY KEY (`manuscriptID`, `reviewer_personID`),
  CONSTRAINT `fk_feedback_manuscript1`
    FOREIGN KEY (`manuscriptID`)
    REFERENCES `byang_db`.`manuscript` (`manuscriptID`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_feedback_reviewer1`
    FOREIGN KEY (`reviewer_personID`)
    REFERENCES `byang_db`.`reviewer` (`personID`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- reviewer_has_RICode table
CREATE TABLE IF NOT EXISTS `byang_db`.`reviewer_has_RICode` (
  `reviewer_personID` INT NOT NULL,
  `RICode_RICodeID` MEDIUMINT NOT NULL,
  CONSTRAINT `fk_reviewer_has_RICode_reviewer1`
    FOREIGN KEY (`reviewer_personID`)
    REFERENCES `byang_db`.`reviewer` (`personID`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_reviewer_has_RICode_RICode1`
    FOREIGN KEY (`RICode_RICodeID`)
    REFERENCES `byang_db`.`RICode` (`RICodeID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- secondaryAuthor table
CREATE TABLE IF NOT EXISTS `byang_db`.`secondaryAuthor` (
  `manuscriptID` INT NOT NULL,
  `authorOrder` INT NOT NULL,
  `fname` VARCHAR(30) NOT NULL,
  `lname` VARCHAR(30) NOT NULL,
  PRIMARY KEY (`authorOrder`, `manuscriptID`),
  CONSTRAINT `fk_secondaryAuthor_manuscript1`
    FOREIGN KEY (`manuscriptID`)
    REFERENCES `byang_db`.`manuscript` (`manuscriptID`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;



-- -----------------------------------------------------
-- insert example data
-- -----------------------------------------------------


-- person table
-- primary authors: 100-129
INSERT INTO `person` (`personID`,`fname`,`lname`) VALUES (100,"Kirestin","Ayala"),(101,"Indira","Oneill"),(102,"Rogan","Byers"),(103,"Roanna","Reynolds"),(104,"Beverly","Stein"),(105,"Hadassah","Sykes"),(106,"Karyn","Elliott"),(107,"Moana","Ashley"),(108,"Berk","Hines"),(109,"Nero","Kelley");
INSERT INTO `person` (`personID`,`fname`,`lname`) VALUES (110,"Tanner","Lang"),(111,"Chandler","Fox"),(112,"Zena","Miles"),(113,"MacKensie","Petersen"),(114,"Lance","Parrish"),(115,"Tatum","Morgan"),(116,"Frances","Clemons"),(117,"Mariko","Gamble"),(118,"Brandon","Hoover"),(119,"Darrel","Dudley");
INSERT INTO `person` (`personID`,`fname`,`lname`) VALUES (120,"Jocelyn","Yang"),(121,"Vera","Norton"),(122,"Nash","Whitfield"),(123,"Hop","Rice"),(124,"Shoshana","Gregory"),(125,"Raphael","Travis"),(126,"Carolyn","Chase"),(127,"Todd","Macias"),(128,"Josephine","Vazquez"),(129,"Robin","Bird");
-- editors: 300-319
INSERT INTO `person` (`personID`,`fname`,`lname`) VALUES (300,"Mona","Rasmussen"),(301,"Ori","Lamb"),(302,"Ira","Kline"),(303,"Clark","Adams"),(304,"Quynn","Russell"),(305,"Marvin","Kirk"),(306,"Jemima","King"),(307,"Savannah","Matthews"),(308,"Nissim","Adams"),(309,"Susan","Whitley");
INSERT INTO `person` (`personID`,`fname`,`lname`) VALUES (310,"Desiree","Tanner"),(311,"Kieran","Salinas"),(312,"Amy","Ochoa"),(313,"Meghan","Boone"),(314,"Kirk","Cummings"),(315,"Lance","Stephens"),(316,"Emery","Richardson"),(317,"Imelda","Ferguson"),(318,"Brandon","Talley"),(319,"Elmo","Leach");
-- reviewers: 400-429
INSERT INTO `person` (`personID`,`fname`,`lname`) VALUES (400,"Warren","Nixon"),(401,"Kyle","Bird"),(402,"Chanda","Phillips"),(403,"Cleo","Wooten"),(404,"Bree","Howell"),(405,"Beck","Buckner"),(406,"Patricia","Garner"),(407,"Hanae","Vazquez"),(408,"Brody","Hurst"),(409,"Cassady","Nicholson");
INSERT INTO `person` (`personID`,`fname`,`lname`) VALUES (410,"Quamar","Sykes"),(411,"Judah","Kim"),(412,"Aiko","Waller"),(413,"Ocean","Boyle"),(414,"Karyn","Ratliff"),(415,"Sarah","Stanton"),(416,"Phelan","Kirby"),(417,"Madaline","Petty"),(418,"Amos","Bright"),(419,"Grant","Jarvis");
INSERT INTO `person` (`personID`,`fname`,`lname`) VALUES (420,"Camille","Oneill"),(421,"Hunter","Hoover"),(422,"Karleigh","Lott"),(423,"Channing","Maddox"),(424,"Ila","Moses"),(425,"Illiana","Bruce"),(426,"Martena","Campos"),(427,"Fiona","Barton"),(428,"Athena","Love"),(429,"Chadwick","Edwards");



-- primary authors
INSERT INTO `author` (`personID`,`email`,`address`,`affiliation`) VALUES (100,"nisi.magna@consectetuer.edu","Ap #456-1812 Erat Avenue","Arcu Imperdiet Corporation"),(101,"tellus.non@scelerisqueduiSuspendisse.ca","1883 Mauris Rd.","Quisque Nonummy Ipsum Inc."),(102,"quis@ametfaucibusut.net","2896 Erat. St.","Sed Tortor Integer LLC"),(103,"a@Duiselementum.net","Ap #152-6114 Ipsum Street","Fusce Mi Consulting"),(104,"purus@auctorvelit.org","5149 Mattis. Av.","Ligula Donec Company"),(105,"vehicula@enim.net","1348 Aliquam Ave","Mauris Quis Corp."),(106,"at.nisi.Cum@ametdapibusid.co.uk","P.O. Box 321, 7837 Velit. Ave","Mauris Company"),(107,"eu.erat@at.ca","P.O. Box 185, 192 Interdum. St.","Pellentesque Ultricies PC"),(108,"risus.Nunc@magnaUt.co.uk","3635 Faucibus Road","Faucibus Id Libero Limited"),(109,"non.enim@liberolacus.net","216-9506 Mi Ave","Velit Cras Incorporated");
INSERT INTO `author` (`personID`,`email`,`address`,`affiliation`) VALUES (110,"per.conubia.nostra@Morbiquisurna.co.uk","Ap #169-8331 Egestas. Road","Fusce Diam Nunc PC"),(111,"sem@pede.net","245 Turpis Av.","Orci LLC"),(112,"est@dolor.net","P.O. Box 826, 4428 Tincidunt Road","Ultrices Iaculis Industries"),(113,"ridiculus.mus.Proin@lectus.edu","P.O. Box 140, 6697 Aliquam Av.","At Fringilla Purus Ltd"),(114,"tempus@enimNunc.co.uk","Ap #331-2558 Nunc Street","Vulputate Posuere Vulputate Limited"),(115,"semper@Cras.net","P.O. Box 363, 8279 Ullamcorper Rd.","Dignissim Maecenas Inc."),(116,"consectetuer.cursus.et@molestiedapibusligula.org","151 Tellus Rd.","Cum Sociis Natoque Institute"),(117,"Quisque@necmalesuada.com","923-7802 Phasellus St.","Montes Nascetur PC"),(118,"tempor.bibendum@Quisque.co.uk","P.O. Box 995, 9557 Bibendum Rd.","Eu Enim Etiam Industries"),(119,"laoreet@blanditNamnulla.net","6454 Luctus Rd.","Ut Semper Foundation");
INSERT INTO `author` (`personID`,`email`,`address`,`affiliation`) VALUES (120,"Duis@dignissimlacusAliquam.net","P.O. Box 348, 4278 Dapibus Road","Egestas Industries"),(121,"odio@orci.com","P.O. Box 663, 5819 Quis Avenue","Luctus Corp."),(122,"amet@odiosempercursus.com","735-9006 Eu, Road","Senectus Et LLC"),(123,"nibh.dolor.nonummy@purus.net","Ap #161-2672 Amet Av.","Nulla LLC"),(124,"risus.Nulla.eget@arcuVestibulum.com","P.O. Box 722, 7857 Sed Road","Libero Proin Corp."),(125,"at.lacus@malesuadafames.com","323-4314 Convallis Road","Mollis Duis Sit Inc."),(126,"ut.odio.vel@noncursusnon.co.uk","P.O. Box 317, 816 In St.","Diam Limited"),(127,"accumsan.convallis.ante@pretiumaliquet.co.uk","P.O. Box 987, 5050 Pede, Street","Natoque Consulting"),(128,"lectus.Cum.sociis@lobortisauguescelerisque.co.uk","Ap #639-557 Vulputate, Ave","Tortor LLP"),(129,"Nulla.eget@ametfaucibus.co.uk","9679 Non, Ave","Eget Industries");



-- RICodes
INSERT INTO `RICode` (`interest`) VALUES
('Agricultural engineering'),
('Biochemical engineering'),
('Biomechanical engineering'),
('Ergonomics'),
('Food engineering'),
('Bioprocess engineering'),
('Genetic engineering'),
('Human genetic engineering'),
('Metabolic engineering'),
('Molecular engineering'),
('Neural engineering'),
('Protein engineering'),
('Rehabilitation engineering'),
('Tissue engineering'),
('Aquatic and environmental engineering'),
('Architectural engineering'),
('Civionic engineering'),
('Construction engineering'),
('Earthquake engineering'),
('Earth systems engineering and management'),
('Ecological engineering'),
('Environmental engineering'),
('Geomatics engineering'),
('Geotechnical engineering'),
('Highway engineering'),
('Hydraulic engineering'),
('Landscape engineering'),
('Land development engineering'),
('Pavement engineering'),
('Railway systems engineering'),
('River engineering'),
('Sanitary engineering'),
('Sewage engineering'),
('Structural engineering'),
('Surveying'),
('Traffic engineering'),
('Transportation engineering'),
('Urban engineering'),
('Irrigation and agriculture engineering'),
('Explosives engineering'),
('Biomolecular engineering'),
('Ceramics engineering'),
('Broadcast engineering'),
('Building engineering'),
('Signal Processing'),
('Computer engineering'),
('Power systems engineering'),
('Control engineering'),
('Telecommunications engineering'),
('Electronic engineering'),
('Instrumentation engineering'),
('Network engineering'),
('Neuromorphic engineering'),
('Engineering Technology'),
('Integrated engineering'),
('Value engineering'),
('Cost engineering'),
('Fire protection engineering'),
('Domain engineering'),
('Engineering economics'),
('Engineering management'),
('Engineering psychology'),
('Ergonomics'),
('Facilities Engineering'),
('Logistic engineering'),
('Model-driven engineering'),
('Performance engineering'),
('Process engineering'),
('Product Family Engineering'),
('Quality engineering'),
('Reliability engineering'),
('Safety engineering'),
('Security engineering'),
('Support engineering'),
('Systems engineering'),
('Metallurgical Engineering'),
('Surface Engineering'),
('Biomaterials Engineering'),
('Crystal Engineering'),
('Amorphous Metals'),
('Metal Forming'),
('Ceramic Engineering'),
('Plastics Engineering'),
('Forensic Materials Engineering'),
('Composite Materials'),
('Casting'),
('Electronic Materials'),
('Nano materials'),
('Corrosion Engineering'),
('Vitreous Materials'),
('Welding'),
('Acoustical engineering'),
('Aerospace engineering'),
('Audio engineering'),
('Automotive engineering'),
('Building services engineering'),
('Earthquake engineering'),
('Forensic engineering'),
('Marine engineering'),
('Mechatronics'),
('Nanoengineering'),
('Naval architecture'),
('Sports engineering'),
('Structural engineering'),
('Vacuum engineering'),
('Military engineering'),
('Combat engineering'),
('Offshore engineering'),
('Optical engineering'),
('Geophysical engineering'),
('Mineral engineering'),
('Mining engineering'),
('Reservoir engineering'),
('Climate engineering'),
('Computer-aided engineering'),
('Cryptographic engineering'),
('Information engineering'),
('Knowledge engineering'),
('Language engineering'),
('Release engineering'),
('Teletraffic engineering'),
('Usability engineering'),
('Web engineering'),
('Systems engineering');



-- editor table
INSERT INTO `editor` (`personID`) VALUES (300),(301),(302),(303),(304),(305),(306),(307),(308),(309);



-- issue table
-- IDs: 2014 through 2018, periods 1-4
INSERT INTO `issue` (`publicationYear`,`periodNumber`,`datePrinted`) VALUES (2014,1,"2014-01-16"),(2014,2,"2014-05-20"),(2014,3,"2014-09-20"),(2014,4,"2014-11-16");
INSERT INTO `issue` (`publicationYear`,`periodNumber`,`datePrinted`) VALUES (2015,1,"2015-02-19"),(2015,2,"2015-04-15"),(2015,3,"2015-08-19"),(2015,4,"2015-10-23");
INSERT INTO `issue` (`publicationYear`,`periodNumber`,`datePrinted`) VALUES (2016,1,"2016-03-17"),(2016,2,"2016-05-12"),(2016,3,"2016-09-20"),(2016,4,"2016-11-04");
INSERT INTO `issue` (`publicationYear`,`periodNumber`,`datePrinted`) VALUES (2017,1,"2016-01-16"),(2017,2,"2017-04-25"),(2017,3,"2017-09-01"),(2017,4,"2017-10-05");
INSERT INTO `issue` (`publicationYear`,`periodNumber`,`datePrinted`) VALUES (2018,1,"2018-02-07"),(2018,2,"2018-05-18"),(2018,3,"2012-08-26"),(2018,4,"2018-11-06");



-- reviewer table
INSERT INTO `reviewer` (`personID`,`affiliation`,`email`) VALUES (400,"At Velit Corporation","eu.eleifend@ornareplacerat.com"),(401,"In At Pede Ltd","Donec@congue.co.uk"),(402,"Gravida Aliquam Tincidunt Institute","gravida.Aliquam@utnullaCras.co.uk"),(403,"Enim Sed Nulla Corp.","odio.Phasellus.at@nec.org"),(404,"Suspendisse Aliquet Molestie Industries","mi.lorem@tinciduntpede.org"),(405,"Metus Vitae Velit Incorporated","Integer.id@felis.co.uk"),(406,"Quisque Company","est.congue@metusAenean.com"),(407,"Fames LLC","mauris@tincidunt.ca"),(408,"Diam Vel Corporation","vitae.risus.Duis@euultricessit.ca"),(409,"In PC","auctor.non.feugiat@lorem.ca");
INSERT INTO `reviewer` (`personID`,`affiliation`,`email`) VALUES (410,"Dui Fusce Aliquam Limited","Fusce.dolor@nisiCumsociis.com"),(411,"Auctor Corp.","sit.amet@orciPhasellusdapibus.edu"),(412,"Magnis Inc.","mollis@ac.edu"),(413,"Mauris Elit Dictum PC","ipsum@vulputatemauris.org"),(414,"Purus Ltd","fermentum@habitantmorbi.co.uk"),(415,"Magna Incorporated","aliquam.adipiscing@utpellentesque.ca"),(416,"Accumsan Interdum Industries","dui.augue@antelectusconvallis.net"),(417,"Ridiculus Mus Proin Corporation","eget.ipsum.Suspendisse@dapibus.net"),(418,"Mauris Blandit Enim Foundation","ipsum.cursus.vestibulum@amet.ca"),(419,"Pharetra Quisque Inc.","dis.parturient@Duisa.com");
INSERT INTO `reviewer` (`personID`,`affiliation`,`email`) VALUES (420,"Egestas Incorporated","rhoncus.Nullam.velit@ullamcorperviverra.ca"),(421,"Curabitur Egestas PC","Aliquam@etmagnaPraesent.co.uk"), (422,"Tempus Risus Donec Inc.","facilisis.Suspendisse.commodo@bibendumDonec.ca"),(423,"Cursus Luctus LLP","amet.luctus.vulputate@sociisnatoque.ca"),(424,"Fermentum Arcu Company","fermentum.vel@nullaInteger.net"),(425,"Sed Ltd","mauris.Integer.sem@sodales.ca"),(426,"Et Risus Institute","risus.odio@enimCurabitur.ca"),(427,"Ultricies Ornare Elit Consulting","Cras@sociosquadlitora.ca"),(428,"Leo In Lobortis Limited","ut.aliquam.iaculis@idante.edu"),(429,"Mauris Vestibulum Ltd","diam.Sed@non.co.uk");



-- reviewer_has_RICode table
INSERT INTO `reviewer_has_RICode` (`reviewer_personID`,`RICode_RICodeID`) VALUES (400,7),(401,91),(402,57),(403,68),(404,61),(405,82),(406,74),(407,44),(408,48),(409,84);
INSERT INTO `reviewer_has_RICode` (`reviewer_personID`,`RICode_RICodeID`) VALUES (400,98),(401,44),(402,98),(403,17),(404,22),(405,50),(406,38),(407,98),(408,54),(409,83);
INSERT INTO `reviewer_has_RICode` (`reviewer_personID`,`RICode_RICodeID`) VALUES (400,2),(401,26),(402,77),(403,2),(404,83),(405,39),(406,39),(407,82),(408,40),(409,73);
INSERT INTO `reviewer_has_RICode` (`reviewer_personID`,`RICode_RICodeID`) VALUES (410,4),(411,13),(412,26),(413,54),(414,13),(415,7),(416,47),(417,84),(418,39),(419,28);
INSERT INTO `reviewer_has_RICode` (`reviewer_personID`,`RICode_RICodeID`) VALUES (410,40),(411,48),(412,68),(413,75),(414,2),(415,84),(416,45),(417,48),(418,17),(419,65);
INSERT INTO `reviewer_has_RICode` (`reviewer_personID`,`RICode_RICodeID`) VALUES (410,4),(411,4),(412,13),(413,22),(414,22),(415,50),(416,50),(417,48),(418,17),(419,65);
INSERT INTO `reviewer_has_RICode` (`reviewer_personID`,`RICode_RICodeID`) VALUES (420,93),(421,41),(422,26),(423,34),(424,27),(425,95),(426,68),(427,89),(428,91),(429,54);
INSERT INTO `reviewer_has_RICode` (`reviewer_personID`,`RICode_RICodeID`) VALUES (420,7),(421,17),(422,40),(423,82),(424,82),(425,83),(426,91),(427,93),(428,93),(429,17);



-- manuscript table
-- manuscript IDs: 0-59
INSERT INTO `manuscript` (`manuscriptID`,`author_personID`,`editor_personID`,`title`,`status`,`ricodeID`,`numPages`,`startingPage`,`issueOrder`,`dateReceived`,`dateSentForReview`,`dateAccepted`,`issue_publicationYear`,`issue_periodNumber`) VALUES (0,111,301,"metus urna convallis erat, eget tincidunt dui augue eu tellus.","received",2,NULL,NULL,NULL,"2016-09-15",NULL,NULL,NULL,NULL),(2,102,307,"arcu. Vestibulum ut eros non enim commodo hendrerit. Donec porttitor","received",39,NULL,NULL,NULL,"2017-02-08",NULL,NULL,NULL,NULL),(3,113,301,"enim. Mauris quis turpis vitae purus gravida","received",7,NULL,NULL,NULL,"2015-01-27",NULL,NULL,NULL,NULL),(4,118,307,"congue, elit sed consequat auctor, nunc nulla vulputate dui,","received",68,NULL,NULL,NULL,"2017-07-04",NULL,NULL,NULL,NULL),(5,115,301,"bibendum sed, est. Nunc laoreet lectus","received",93,NULL,NULL,NULL,"2018-01-15",NULL,NULL,NULL,NULL),(6,121,302,"tempor arcu. Vestibulum ut eros non enim commodo hendrerit. Donec","received",4,NULL,NULL,NULL,"2017-08-03",NULL,NULL,NULL,NULL),(7,117,301,"erat vitae risus. Duis a mi fringilla","received",68,NULL,NULL,NULL,"2014-08-02",NULL,NULL,NULL,NULL),(8,125,306,"interdum. Nunc sollicitudin commodo ipsum. Suspendisse non leo. Vivamus","received",82,NULL,NULL,NULL,"2017-01-16",NULL,NULL,NULL,NULL),(9,129,307,"tellus lorem eu metus. In lorem.","received",26,NULL,NULL,NULL,"2015-04-18",NULL,NULL,NULL,NULL);
INSERT INTO `manuscript` (`manuscriptID`,`author_personID`,`editor_personID`,`title`,`status`,`ricodeID`,`numPages`,`startingPage`,`issueOrder`,`dateReceived`,`dateSentForReview`,`dateAccepted`,`issue_publicationYear`,`issue_periodNumber`) VALUES (10,109,304,"diam dictum sapien. Aenean massa. Integer vitae","received",4,NULL,NULL,NULL,"2015-02-03",NULL,NULL,NULL,NULL),(11,120,301,"mauris blandit mattis. Cras eget nisi dictum augue malesuada","received",93,NULL,NULL,NULL,"2016-08-15",NULL,NULL,NULL,NULL),(12,116,302,"Suspendisse eleifend. Cras sed leo. Cras vehicula aliquet","received",26,NULL,NULL,NULL,"2017-06-01",NULL,NULL,NULL,NULL),(13,119,305,"augue id ante dictum cursus. Nunc mauris elit, dictum","received",68,NULL,NULL,NULL,"2018-04-21",NULL,NULL,NULL,NULL),(14,105,309,"nunc. In at pede. Cras vulputate velit","received",83,NULL,NULL,NULL,"2015-10-10",NULL,NULL,NULL,NULL),(15,129,308,"libero. Integer in magna. Phasellus dolor elit, pellentesque","received",91,NULL,NULL,NULL,"2014-11-12",NULL,NULL,NULL,NULL),(16,116,307,"leo, in lobortis tellus justo sit amet nulla.","received",39,NULL,NULL,NULL,"2015-04-12",NULL,NULL,NULL,NULL),(17,122,306,"risus. Nunc ac sem ut dolor dapibus gravida.","received",17,NULL,NULL,NULL,"2014-05-03",NULL,NULL,NULL,NULL),(18,114,305,"libero est, congue a, aliquet vel, vulputate eu, odio. Phasellus","received",50,NULL,NULL,NULL,"2016-02-16",NULL,NULL,NULL,NULL),(19,125,304,"ornare placerat, orci lacus vestibulum lorem, sit amet ultricies","received",54,NULL,NULL,NULL,"2018-04-05",NULL,NULL,NULL,NULL);
INSERT INTO `manuscript` (`manuscriptID`,`author_personID`,`editor_personID`,`title`,`status`,`ricodeID`,`numPages`,`startingPage`,`issueOrder`,`dateReceived`,`dateSentForReview`,`dateAccepted`,`issue_publicationYear`,`issue_periodNumber`) VALUES (20,101,309,"ut odio vel est tempor bibendum. Donec","rejected",7,NULL,NULL,NULL,"2016-06-11",NULL,NULL,NULL,NULL),(21,123,308,"enim nec tempus scelerisque, lorem ipsum sodales purus, in","rejected",82,NULL,NULL,NULL,"2017-12-21",NULL,NULL,NULL,NULL),(22,113,307,"enim non nisi. Aenean eget metus. In nec","rejected",50,NULL,NULL,NULL,"2017-11-26",NULL,NULL,NULL,NULL),(23,125,302,"gravida mauris ut mi. Duis risus odio,","rejected",84,NULL,NULL,NULL,"2015-03-13",NULL,NULL,NULL,NULL),(24,101,309,"sociis natoque penatibus et magnis dis parturient montes, nascetur","rejected",91,NULL,NULL,NULL,"2015-05-22",NULL,NULL,NULL,NULL),(25,100,302,"nulla vulputate dui, nec tempus mauris erat eget","rejected",93,NULL,NULL,NULL,"2014-12-30",NULL,NULL,NULL,NULL),(26,104,300,"turpis vitae purus gravida sagittis. Duis gravida. Praesent eu","rejected",54,NULL,NULL,NULL,"2017-01-02",NULL,NULL,NULL,NULL),(27,106,306,"sapien imperdiet ornare. In faucibus. Morbi","rejected",98,NULL,NULL,NULL,"2016-06-05",NULL,NULL,NULL,NULL),(28,109,309,"Nunc ac sem ut dolor dapibus gravida. Aliquam","rejected",82,NULL,NULL,NULL,"2014-06-10",NULL,NULL,NULL,NULL),(29,125,309,"lorem ut aliquam iaculis, lacus pede sagittis augue,","rejected",50,NULL,NULL,NULL,"2015-03-09",NULL,NULL,NULL,NULL);
INSERT INTO `manuscript` (`manuscriptID`,`author_personID`,`editor_personID`,`title`,`status`,`ricodeID`,`numPages`,`startingPage`,`issueOrder`,`dateReceived`,`dateSentForReview`,`dateAccepted`,`issue_publicationYear`,`issue_periodNumber`) VALUES (30,117,308,"fermentum fermentum arcu. Vestibulum ante ipsum primis in faucibus orci","underReview",50,2,8,4,"2016-01-15","2015-04-14",NULL,NULL,NULL),(31,123,307,"vitae odio sagittis semper. Nam tempor diam dictum","underReview",48,2,27,9,"2017-11-30","2016-02-02",NULL,NULL,NULL),(32,123,303,"felis, adipiscing fringilla, porttitor vulputate, posuere vulputate, lacus. Cras","underReview",22,3,27,9,"2017-12-05","2015-10-01",NULL,NULL,NULL),(33,109,300,"magna, malesuada vel, convallis in, cursus","underReview",4,2,54,1,"2017-10-26","2016-09-16",NULL,NULL,NULL),(34,119,304,"at, velit. Cras lorem lorem, luctus ut, pellentesque","underReview",93,3,38,9,"2014-08-15","2014-10-28",NULL,NULL,NULL),(35,128,308,"lacus, varius et, euismod et, commodo","underReview",26,2,53,6,"2015-06-23","2015-04-04",NULL,NULL,NULL),(36,103,305,"lacinia mattis. Integer eu lacus. Quisque imperdiet, erat","underReview",7,4,50,3,"2014-11-18","2017-03-23",NULL,NULL,NULL),(37,111,308,"dolor. Fusce mi lorem, vehicula et, rutrum eu,","underReview",39,4,41,2,"2016-03-29","2015-11-17",NULL,NULL,NULL),(38,116,301,"dui. Cum sociis natoque penatibus et","underReview",83,3,80,4,"2016-05-30","2017-01-08",NULL,NULL,NULL),(39,118,303,"ut mi. Duis risus odio, auctor","underReview",17,2,61,9,"2017-04-12","2016-02-25",NULL,NULL,NULL);
INSERT INTO `manuscript` (`manuscriptID`,`author_personID`,`editor_personID`,`title`,`status`,`ricodeID`,`numPages`,`startingPage`,`issueOrder`,`dateReceived`,`dateSentForReview`,`dateAccepted`,`issue_publicationYear`,`issue_periodNumber`) VALUES (40,107,308,"lacus. Cras interdum. Nunc sollicitudin commodo ipsum.","accepted",54,4,64,2,"2015-04-06","2015-06-04","2016-05-06",2017,4),(41,113,300,"nec enim. Nunc ut erat. Sed","accepted",68,4,21,2,"2015-10-21","2016-06-29","2017-01-21",2017,2),(42,119,304,"nisi sem semper erat, in consectetuer ipsum nunc","accepted",54,4,13,9,"2015-02-05","2016-01-29","2016-03-13",2016,2),(43,103,308,"Nulla semper tellus id nunc interdum feugiat. Sed","accepted",7,4,15,6,"2014-02-18","2015-01-09","2016-10-16",2016,1),(44,103,305,"Fusce aliquam, enim nec tempus scelerisque, lorem ipsum","scheduled",93,4,82,10,"2015-06-28","2016-03-30","2016-10-15",2017,1),(45,114,301,"vel nisl. Quisque fringilla euismod enim. Etiam gravida","scheduled",68,3,7,10,"2015-04-28","2015-06-26","2016-01-17",2016,1),(46,101,308,"gravida nunc sed pede. Cum sociis natoque penatibus et magnis","published",26,3,75,10,"2014-07-22","2016-11-06","2017-01-21",2017,2),(47,128,303,"eu augue porttitor interdum. Sed auctor","published",54,2,69,9,"2014-05-29","2015-03-23","2016-02-07",2016,3),(48,111,301,"nibh enim, gravida sit amet, dapibus id, blandit","published",39,3,96,2,"2016-07-01","2014-03-11","2015-02-04",2017,1),(49,115,300,"non, luctus sit amet, faucibus ut, nulla. Cras eu tellus","published",54,3,67,10,"2015-12-20","2016-06-07","2017-10-05",2017,4);
INSERT INTO `manuscript` (`manuscriptID`,`author_personID`,`editor_personID`,`title`,`status`,`ricodeID`,`numPages`,`startingPage`,`issueOrder`,`dateReceived`,`dateSentForReview`,`dateAccepted`,`issue_publicationYear`,`issue_periodNumber`) VALUES (50,112,304,"a, scelerisque sed, sapien. Nunc pulvinar arcu","published",68,2,24,3,"2015-5-30","2015-10-09","2015-11-14",2017,4),(51,124,309,"vel sapien imperdiet ornare. In faucibus. Morbi vehicula. Pellentesque","published",84,3,99,6,"2014-11-04","2015-03-29","2015-12-05",2015,3),(52,117,300,"egestas. Fusce aliquet magna a neque. Nullam ut nisi a","published",50,3,27,10,"2014-03-21","2014-10-28","2015-02-10",2014,2),(53,120,308,"sapien imperdiet ornare. In faucibus. Morbi vehicula.","published",13,3,10,4,"2015-10-08","2016-08-09","2016-11-30",2017,4),(54,116,309,"lorem eu metus. In lorem. Donec elementum, lorem ut","published",7,4,52,8,"2015-09-10","2015-10-11","2016-03-26",2017,3),(55,113,301,"non, lacinia at, iaculis quis, pede. Praesent eu","published",82,3,10,1,"2014-04-06","2014-07-05","2015-08-09",2018,4),(56,120,303,"dictum ultricies ligula. Nullam enim. Sed nulla ante,","published",26,4,7,7,"2014-01-06","2015-11-30","2017-02-08",2018,2),(57,106,305,"nisl arcu iaculis enim, sit amet ornare","published",40,2,23,5,"2014-01-11","2014-03-14","2015-07-08",2017,2),(58,114,303,"mi lacinia mattis. Integer eu lacus. Quisque imperdiet, erat","published",68,4,96,9,"2014-4-06","2014-08-15","2016-03-12",2018,4),(59,106,308,"Sed et libero. Proin mi. Aliquam gravida mauris ut mi.","published",50,4,93,8,"2014-03-29","2014-10-02","2016-11-12",2017,4);



-- secondaryAuthor table
INSERT INTO `secondaryAuthor` (`manuscriptID`,`authorOrder`,`fname`,`lname`) VALUES (33,5,"Frances","Clemons"),(38,5,"Wynne","Avery"),(8,1,"Aubrey","Waters"),(27,2,"Charles","Palmer"),(10,2,"Myra","Cameron"),(4,2,"Marsden","Gordon"),(31,5,"Chancellor","Adkins"),(25,5,"Aurora","Kirk"),(34,3,"Malik","Potter"),(11,3,"Troy","Kidd");
INSERT INTO `secondaryAuthor` (`manuscriptID`,`authorOrder`,`fname`,`lname`) VALUES (24,1,"Kelly","Oliver"),(21,1,"Shea","Nunez"),(14,4,"Rashad","Mcdonald"),(10,1,"Noah","Wagner"),(58,4,"Patricia","Freeman"),(57,1,"Erica","Sellers"),(44,1,"Lawrence","Mccormick"),(24,2,"Alexis","Jackson"),(20,5,"Hedy","Nicholson"),(29,1,"Selma","Nolan");
INSERT INTO `secondaryAuthor` (`manuscriptID`,`authorOrder`,`fname`,`lname`) VALUES (5,4,"Mechelle","Holden"),(52,5,"Belle","Gould"),(5,3,"Louis","Watts"),(20,2,"May","Mccarthy"),(48,4,"Shelley","Donaldson"),(16,1,"Yvonne","Justice"),(43,2,"Amery","Calhoun"),(40,5,"Ferdinand","Holloway"),(31,4,"Angela","Garcia"),(55,5,"Raymond","Vargas");
INSERT INTO `secondaryAuthor` (`manuscriptID`,`authorOrder`,`fname`,`lname`) VALUES (58,2,"Jescie","Mercer"),(40,4,"Jessamine","Sandoval"),(4,3,"Aubrey","Hopper"),(27,4,"Wynne","Avery"),(52,1,"Hayes","Mcgee"),(16,4,"Zelenia","Harmon"),(43,1,"Claudia","Solis"),(41,4,"Quin","Solis"),(38,2,"Moana","Shepard"),(17,3,"Barrett","Snyder");
INSERT INTO `secondaryAuthor` (`manuscriptID`,`authorOrder`,`fname`,`lname`) VALUES (38,4,"Kirk","Monroe"),(12,3,"Alexandra","Holt"),(50,5,"Ira","George"),(11,1,"Naida","Serrano"),(30,2,"Rajah","Farley"),(19,3,"Byron","Livingston"),(19,5,"Jael","Powell"),(37,2,"Holly","Bernard"),(38,1,"Audrey","Vazquez"),(23,2,"Micah","Rodgers");
INSERT INTO `secondaryAuthor` (`manuscriptID`,`authorOrder`,`fname`,`lname`) VALUES (40,3,"Chiquita","Sparks"),(22,4,"Quail","Ellis"),(8,2,"Cameron","Leach"),(8,3,"Brock","Foster"),(7,1,"Myra","Terry"),(26,1,"Neil","Velazquez"),(58,5,"Guy","Barron"),(50,2,"Steven","Freeman"),(15,5,"Althea","Vance"),(55,1,"Kane","Rowe");
INSERT INTO `secondaryAuthor` (`manuscriptID`,`authorOrder`,`fname`,`lname`) VALUES (3,1,"Gil","Alvarez"),(19,4,"Megan","Mendoza"),(1,2,"Ashely","Glenn"),(46,5,"Britanni","Jones"),(25,2,"Kylie","Scott"),(28,1,"Grady","Scott"),(52,4,"Yasir","Alford"),(59,1,"Alexander","Sheppard"),(24,5,"Shellie","Sharpe"),(11,5,"Neil","Bentley");
INSERT INTO `secondaryAuthor` (`manuscriptID`,`authorOrder`,`fname`,`lname`) VALUES (56,5,"Brett","Shannon"),(23,4,"Bruno","Valenzuela"),(15,3,"Cruz","Burton"),(57,2,"Adrienne","Stafford"),(57,3,"Kathleen","Cleveland"),(15,2,"Hyatt","Fox"),(28,2,"Kenneth","Cline"),(7,2,"Vincent","Thompson"),(6,2,"Myra","Rivers"),(44,2,"Isaac","Meadows");
INSERT INTO `secondaryAuthor` (`manuscriptID`,`authorOrder`,`fname`,`lname`) VALUES (19,2,"Ezekiel","Nielsen"),(46,2,"Blaine","Waters"),(57,4,"Benjamin","Horn"),(40,2,"Lyle","Bridges"),(35,3,"Cameron","Mitchell"),(23,1,"Susan","Sloan"),(55,4,"Florence","Mccarthy"),(21,5,"Avye","Boyle"),(45,2,"Colby","Petersen"),(38,3,"Finn","Dawson");
INSERT INTO `secondaryAuthor` (`manuscriptID`,`authorOrder`,`fname`,`lname`) VALUES (21,4,"Danielle","Downs"),(53,1,"Vladimir","Spencer"),(56,4,"Cooper","Ratliff"),(51,1,"Kameko","Daniels"),(40,1,"Mercedes","Mccarthy"),(56,1,"Paki","Browning"),(6,1,"Oren","Mckee"),(3,3,"Isaiah","Santos"),(49,4,"Kessie","Slater"),(14,3,"Evelyn","Long");



-- feedback table
INSERT INTO `feedback` (`manuscriptID`,`reviewer_personID`,`appropriateness`,`clarity`,`methodology`,`contribution`,`recommendation`,`dateReceived`) VALUES (30,416,NULL,NULL,NULL,NULL,NULL,NULL),(30,419,NULL,NULL,NULL,NULL,NULL,NULL),(30,420,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO `feedback` (`manuscriptID`,`reviewer_personID`,`appropriateness`,`clarity`,`methodology`,`contribution`,`recommendation`,`dateReceived`) VALUES (31,426,NULL,NULL,NULL,NULL,NULL,NULL),(31,424,NULL,NULL,NULL,NULL,NULL,NULL),(31,402,NULL,NULL,NULL,NULL,NULL,NULL),(31,401,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO `feedback` (`manuscriptID`,`reviewer_personID`,`appropriateness`,`clarity`,`methodology`,`contribution`,`recommendation`,`dateReceived`) VALUES (32,413,NULL,NULL,NULL,NULL,NULL,NULL),(32,419,NULL,NULL,NULL,NULL,NULL,NULL),(32,412,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO `feedback` (`manuscriptID`,`reviewer_personID`,`appropriateness`,`clarity`,`methodology`,`contribution`,`recommendation`,`dateReceived`) VALUES (33,417,NULL,NULL,NULL,NULL,NULL,NULL),(33,400,NULL,NULL,NULL,NULL,NULL,NULL),(33,428,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO `feedback` (`manuscriptID`,`reviewer_personID`,`appropriateness`,`clarity`,`methodology`,`contribution`,`recommendation`,`dateReceived`) VALUES (34,409,NULL,NULL,NULL,NULL,NULL,NULL),(34,414,NULL,NULL,NULL,NULL,NULL,NULL),(34,417,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO `feedback` (`manuscriptID`,`reviewer_personID`,`appropriateness`,`clarity`,`methodology`,`contribution`,`recommendation`,`dateReceived`) VALUES (35,412,NULL,NULL,NULL,NULL,NULL,NULL),(35,419,NULL,NULL,NULL,NULL,NULL,NULL),(35,406,NULL,NULL,NULL,NULL,NULL,NULL),(35,417,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO `feedback` (`manuscriptID`,`reviewer_personID`,`appropriateness`,`clarity`,`methodology`,`contribution`,`recommendation`,`dateReceived`) VALUES (36,407,NULL,NULL,NULL,NULL,NULL,NULL),(36,401,NULL,NULL,NULL,NULL,NULL,NULL),(36,429,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO `feedback` (`manuscriptID`,`reviewer_personID`,`appropriateness`,`clarity`,`methodology`,`contribution`,`recommendation`,`dateReceived`) VALUES (37,403,NULL,NULL,NULL,NULL,NULL,NULL),(37,411,NULL,NULL,NULL,NULL,NULL,NULL),(37,427,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO `feedback` (`manuscriptID`,`reviewer_personID`,`appropriateness`,`clarity`,`methodology`,`contribution`,`recommendation`,`dateReceived`) VALUES (38,403,NULL,NULL,NULL,NULL,NULL,NULL),(38,402,NULL,NULL,NULL,NULL,NULL,NULL),(38,423,NULL,NULL,NULL,NULL,NULL,NULL),(38,412,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO `feedback` (`manuscriptID`,`reviewer_personID`,`appropriateness`,`clarity`,`methodology`,`contribution`,`recommendation`,`dateReceived`) VALUES (39,411,NULL,NULL,NULL,NULL,NULL,NULL),(39,415,NULL,NULL,NULL,NULL,NULL,NULL),(39,427,NULL,NULL,NULL,NULL,NULL,NULL);

INSERT INTO `feedback` (`manuscriptID`,`reviewer_personID`,`appropriateness`,`clarity`,`methodology`,`contribution`,`recommendation`,`dateReceived`) VALUES (40,428,6,1,7,8,1,"2014-11-21"),(40,409,1,5,9,5,1,"2014-11-19"),(40,424,6,1,7,7,0,"2017-06-08");
INSERT INTO `feedback` (`manuscriptID`,`reviewer_personID`,`appropriateness`,`clarity`,`methodology`,`contribution`,`recommendation`,`dateReceived`) VALUES (41,422,9,8,1,8,7,"2015-04-11"),(41,421,2,9,10,8,9,"2016-10-01"),(41,400,10,4,2,10,2,"2015-01-03");
INSERT INTO `feedback` (`manuscriptID`,`reviewer_personID`,`appropriateness`,`clarity`,`methodology`,`contribution`,`recommendation`,`dateReceived`) VALUES (42,417,6,6,8,6,0,"2014-07-30"),(42,423,6,4,8,5,0,"2016-06-09"),(42,421,2,3,8,9,0,"2018-07-01");
INSERT INTO `feedback` (`manuscriptID`,`reviewer_personID`,`appropriateness`,`clarity`,`methodology`,`contribution`,`recommendation`,`dateReceived`) VALUES (43,407,7,3,2,7,1,"2018-06-13"),(43,417,9,2,3,8,1,"2016-09-11"),(43,413,7,5,3,9,0,"2016-01-11");
INSERT INTO `feedback` (`manuscriptID`,`reviewer_personID`,`appropriateness`,`clarity`,`methodology`,`contribution`,`recommendation`,`dateReceived`) VALUES (44,424,7,7,3,9,1,"2015-08-09"),(44,418,10,9,7,2,5,"2016-12-21"),(44,410,3,6,5,8,7,"2014-05-10"),(44,412,3,10,2,9,8,"2016-11-27");
INSERT INTO `feedback` (`manuscriptID`,`reviewer_personID`,`appropriateness`,`clarity`,`methodology`,`contribution`,`recommendation`,`dateReceived`) VALUES (45,413,7,5,7,2,4,"2014-10-20"),(45,414,9,6,2,1,2,"2017-09-10"),(45,415,1,9,5,2,4,"2018-01-29");
INSERT INTO `feedback` (`manuscriptID`,`reviewer_personID`,`appropriateness`,`clarity`,`methodology`,`contribution`,`recommendation`,`dateReceived`) VALUES (46,401,1,4,5,2,10,"2014-07-22"),(46,419,6,9,3,2,9,"2016-12-06"),(46,403,2,1,3,1,3,"2014-10-09"),(46,412,7,5,4,10,3,"2017-02-27");
INSERT INTO `feedback` (`manuscriptID`,`reviewer_personID`,`appropriateness`,`clarity`,`methodology`,`contribution`,`recommendation`,`dateReceived`) VALUES (47,420,3,3,5,10,3,"2016-02-16"),(47,402,1,1,5,7,7,"2018-01-14"),(47,412,3,6,10,9,8,"2014-12-23"),(47,405,10,3,7,8,10,"2017-09-05"),(47,428,2,5,5,5,3,"2016-02-18"),(47,400,10,3,9,10,4,"2014-09-30");
INSERT INTO `feedback` (`manuscriptID`,`reviewer_personID`,`appropriateness`,`clarity`,`methodology`,`contribution`,`recommendation`,`dateReceived`) VALUES (48,429,2,8,5,8,1,"2014-04-25"),(48,424,10,7,1,7,0,"2017-11-27"),(48,406,10,10,7,1,0,"2014-07-15"),(48,423,5,10,4,8,1,"2015-01-25");
INSERT INTO `feedback` (`manuscriptID`,`reviewer_personID`,`appropriateness`,`clarity`,`methodology`,`contribution`,`recommendation`,`dateReceived`) VALUES (49,414,8,7,8,4,0,"2017-02-20"),(49,429,2,10,4,7,1,"2015-02-26"),(49,402,6,4,9,6,1,"2016-09-17");
INSERT INTO `feedback` (`manuscriptID`,`reviewer_personID`,`appropriateness`,`clarity`,`methodology`,`contribution`,`recommendation`,`dateReceived`) VALUES (50,404,2,6,5,7,4,"2017-02-14"),(50,413,3,8,10,1,3,"2017-11-13"),(50,405,10,6,5,7,10,"2016-07-13"),(50,416,4,3,2,1,3,"2017-03-28");
INSERT INTO `feedback` (`manuscriptID`,`reviewer_personID`,`appropriateness`,`clarity`,`methodology`,`contribution`,`recommendation`,`dateReceived`) VALUES (51,404,2,8,10,8,1,"2015-03-27"),(51,425,7,10,5,8,1,"2018-04-24"),(51,406,9,7,10,7,0,"2015-08-17");
INSERT INTO `feedback` (`manuscriptID`,`reviewer_personID`,`appropriateness`,`clarity`,`methodology`,`contribution`,`recommendation`,`dateReceived`) VALUES (52,408,5,7,9,7,0,"2016-10-22"),(52,424,5,5,8,3,0,"2014-10-02"),(52,418,2,2,10,6,0,"2016-08-01");
INSERT INTO `feedback` (`manuscriptID`,`reviewer_personID`,`appropriateness`,`clarity`,`methodology`,`contribution`,`recommendation`,`dateReceived`) VALUES (53,428,1,6,5,4,0,"2015-02-24"),(53,406,9,4,3,6,0,"2017-10-09"),(53,419,1,2,5,2,1,"2016-08-14");
INSERT INTO `feedback` (`manuscriptID`,`reviewer_personID`,`appropriateness`,`clarity`,`methodology`,`contribution`,`recommendation`,`dateReceived`) VALUES (54,409,9,2,2,7,9,"2016-03-30"),(54,402,1,1,8,8,8,"2014-06-10"),(54,413,3,4,10,1,2,"2017-09-26"),(54,424,2,5,1,5,1,"2017-08-08");
INSERT INTO `feedback` (`manuscriptID`,`reviewer_personID`,`appropriateness`,`clarity`,`methodology`,`contribution`,`recommendation`,`dateReceived`) VALUES (55,411,5,9,10,2,0,"2014-12-13"),(55,419,5,2,2,9,0,"2016-11-05"),(55,410,5,9,10,2,0,"2014-12-13"),(55,426,5,10,2,8,0,"2014-09-19");
INSERT INTO `feedback` (`manuscriptID`,`reviewer_personID`,`appropriateness`,`clarity`,`methodology`,`contribution`,`recommendation`,`dateReceived`) VALUES (56,403,7,7,6,10,0,"2015-04-23"),(56,424,10,6,6,10,0,"2018-10-11"),(56,423,5,4,9,3,0,"2017-10-14");
INSERT INTO `feedback` (`manuscriptID`,`reviewer_personID`,`appropriateness`,`clarity`,`methodology`,`contribution`,`recommendation`,`dateReceived`) VALUES (57,427,7,4,8,1,1,"2016-02-02"),(57,414,3,1,5,5,0,"2016-03-20"),(57,428,1,8,6,5,1,"2015-06-29"),(57,422,10,3,10,2,0,"2018-02-05");
INSERT INTO `feedback` (`manuscriptID`,`reviewer_personID`,`appropriateness`,`clarity`,`methodology`,`contribution`,`recommendation`,`dateReceived`) VALUES (58,406,5,9,9,8,9,"2017-05-13"),(58,415,7,2,7,6,1,"2018-02-03"),(58,422,4,5,4,10,0,"2016-08-22"),(58,416,4,7,3,3,0,"2014-05-22"),(58,429,3,8,5,8,0,"2014-03-31");
INSERT INTO `feedback` (`manuscriptID`,`reviewer_personID`,`appropriateness`,`clarity`,`methodology`,`contribution`,`recommendation`,`dateReceived`) VALUES (59,412,6,4,4,1,1,"2016-02-17"),(59,416,4,1,3,6,0,"2018-01-14"),(59,419,6,10,6,10,0,"2015-06-10");



-- -----------------------------------------------------
-- define views
-- -----------------------------------------------------


DROP VIEW IF EXISTS LeadAuthorManuscripts;
DROP VIEW IF EXISTS AnyAuthorManuscripts;
DROP VIEW IF EXISTS PublishedIssues;
DROP VIEW IF EXISTS ReviewQueue;
DROP VIEW IF EXISTS WhatsLeft;
DROP VIEW IF EXISTS ReviewStatus;


CREATE VIEW LeadAuthorManuscripts AS
SELECT author.personID, person.fname, person.lname, author.email, author.address, author.affiliation, manuscript.manuscriptID, manuscript.`status`, manuscript.dateReceived
FROM author 
JOIN manuscript ON manuscript.author_personID = author.personID
JOIN person ON person.personID = author.personID
ORDER BY person.lname ASC, manuscript.dateReceived ASC;



CREATE VIEW AnyAuthorManuscripts AS
(SELECT person.fname AS fname, person.lname AS lname, manuscript.manuscriptID AS manuscriptID, manuscript.`status` AS `status`, manuscript.dateReceived AS dateReceived
FROM manuscript 
JOIN person ON person.personID = manuscript.author_personID)
UNION
(SELECT secondaryAuthor.fname AS fname, secondaryAuthor.lname AS lname, secondaryAuthor.manuscriptID AS manuscriptID, manuscript.`status` AS `status`, manuscript.dateReceived AS dateReceived
FROM secondaryAuthor
JOIN manuscript ON manuscript.manuscriptID = secondaryAuthor.manuscriptID)
ORDER BY lname ASC, dateReceived ASC;



CREATE VIEW PublishedIssues AS
SELECT issue.publicationYear, issue.periodNumber, manuscript.title, manuscript.startingPage
FROM issue
JOIN manuscript ON
manuscript.issue_publicationYear = issue.publicationYear AND
manuscript.issue_periodNumber = issue.periodNumber
ORDER BY issue.publicationYear, issue.periodNumber, manuscript.startingPage;



CREATE VIEW ReviewQueue AS
SELECT manuscript.manuscriptID, manuscript.`status`, manuscript.dateReceived, manuscript.author_personID, authorPerson.fname AS author_fname, authorPerson.lname AS author_lname, feedback.reviewer_personID, reviewerPerson.fname, reviewerPerson.lname
FROM manuscript
JOIN person AS authorPerson ON manuscript.author_personID = authorPerson.personID
JOIN feedback ON feedback.manuscriptID = manuscript.manuscriptID
JOIN reviewer ON feedback.reviewer_personID = reviewer.personID
JOIN person AS reviewerPerson ON reviewer.personID = reviewerPerson.personID
WHERE manuscript.`status` = "underReview"
ORDER BY manuscript.dateReceived;



CREATE VIEW WhatsLeft AS
SELECT manuscript.manuscriptID, manuscript.`status`,
CASE WHEN manuscript.`status` = "received" THEN "underReview"
WHEN manuscript.`status` = "underReview" THEN "accepted/rejected"
WHEN manuscript.`status` = "rejected" THEN "better luck next time"
WHEN manuscript.`status` = "accepted" THEN "scheduled"
WHEN manuscript.`status` = "scheduled" THEN "published"
WHEN manuscript.`status` = "published" THEN "congrats!"
ELSE "unknown status" END AS nextStep
FROM manuscript
ORDER BY manuscript.manuscriptID;



CREATE VIEW ReviewStatus AS
SELECT reviewer.personID, manuscript.dateSentForReview, manuscript.manuscriptID, manuscript.title, feedback.appropriateness, feedback.clarity, feedback.methodology, feedback.contribution, feedback.recommendation
FROM reviewer
JOIN feedback ON feedback.reviewer_personID = reviewer.personID
JOIN manuscript ON feedback.manuscriptID = manuscript.manuscriptID;



DROP VIEW IF EXISTS manuscriptReviewers;

-- combines manuscriptID and reviewerID into one table
-- selects only manuscripts that are "underReview"
CREATE VIEW manuscriptReviewers AS
SELECT manuscript.manuscriptID, reviewer_personID, author_personID, editor_personID, title, `status`, RICodeID 
FROM manuscript JOIN feedback ON (manuscript.manuscriptID = feedback.manuscriptID)
WHERE `status` = "underReview"; 


DROP VIEW IF EXISTS countReviewers;

-- for each manuscript under review, count number of reviewers
CREATE VIEW countReviewers AS
SELECT manuscriptID, COUNT(reviewer_personID) as reviewerCount
FROM manuscriptReviewers
GROUP BY manuscriptID; 

--
-- LAB 5E HELPER VIEWS
--

-- number of manuscripts submitted
DROP VIEW IF EXISTS authorNumSubmitted;
CREATE VIEW authorNumSubmitted AS
SELECT personID, fname, lname, count(manuscriptID) AS count
FROM LeadAuthorManuscripts
WHERE `status` = "received"
GROUP BY personID
ORDER BY count(manuscriptID) desc;

-- number of manuscripts under review
DROP VIEW IF EXISTS authorNumUnderReview;
CREATE VIEW authorNumUnderReview AS
select personID, fname, lname, count(manuscriptID) AS count
FROM LeadAuthorManuscripts
WHERE `status` = "underReview"
GROUP BY personID
ORDER BY count(manuscriptID) desc;

-- number of manuscripts rejected
DROP VIEW IF EXISTS authorNumRejected;
CREATE VIEW authorNumRejected AS
select personID, fname, lname, count(manuscriptID) AS count
FROM LeadAuthorManuscripts
WHERE `status` = "rejected"
GROUP BY personID
ORDER BY count(manuscriptID) desc;

-- number of manuscripts accepted
DROP VIEW IF EXISTS authorNumAccepted;
CREATE VIEW authorNumAccepted AS
select personID, fname, lname, count(manuscriptID) AS count
FROM LeadAuthorManuscripts
WHERE `status` = "accepted"
GROUP BY personID
ORDER BY count(manuscriptID) desc;

DROP VIEW IF EXISTS authorNumTypeset;
CREATE VIEW authorNumTypeset AS
select personID, fname, lname, count(manuscriptID) AS count
FROM LeadAuthorManuscripts
WHERE `status` = "typeset"
GROUP BY personID
ORDER BY count(manuscriptID) desc;

-- number of manuscripts scheduled
DROP VIEW IF EXISTS authorNumScheduled;
CREATE VIEW authorNumScheduled AS
select personID, fname, lname, count(manuscriptID) AS count
FROM LeadAuthorManuscripts
WHERE `status` = "scheduled"
GROUP BY personID
ORDER BY count(manuscriptID) desc;

-- number of manuscripts published
DROP VIEW IF EXISTS authorNumPublished;
CREATE VIEW authorNumPublished AS
select personID, fname, lname, count(manuscriptID) AS count
FROM LeadAuthorManuscripts
WHERE `status` = "published"
GROUP BY personID
ORDER BY count(manuscriptID) desc;

-- individual athor
DROP VIEW IF EXISTS individualManuscripts;
CREATE VIEW individualManuscripts AS
SELECT personID, fname, lname, manuscriptID
FROM LeadAuthorManuscripts
WHERE personID = 128; # CHANGE NUMBER 

DROP VIEW IF EXISTS manuscriptWReviewers;

CREATE VIEW manuscriptWReviewers AS
SELECT manuscript.manuscriptID, reviewer_personID, author_personID, editor_personID, title, `status`, RICodeID 
FROM manuscript JOIN feedback ON (manuscript.manuscriptID = feedback.manuscriptID);

DROP TABLE IF EXISTS `credential`;
CREATE TABLE IF NOT EXISTS `byang_db`.`credential` (
`personID` INT NOT NULL AUTO_INCREMENT,
`pword` VARCHAR(30) NOT NULL,
PRIMARY KEY (`personID`))
ENGINE = InnoDB;

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

DROP VIEW IF EXISTS manuscriptRICode;
CREATE VIEW manuscriptRICode AS
SELECT manuscriptID, ricodeID
from manuscript;


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
    DELETE FROM `person` WHERE personID = old.personID;
END
/

-- restore delimiter
DELIMITER ;
