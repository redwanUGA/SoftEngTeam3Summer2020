CREATE SCHEMA IF NOT EXISTS `bookstore` ;
USE `bookstore` ;

-- -----------------------------------------------------
-- Table `bookstore`.`Category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bookstore`.`category` (
  `idCategory` INT NOT NULL AUTO_INCREMENT,
  `category` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`idCategory`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bookstore`.`Books`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bookstore`.`books` (
  `ISBN` INT NOT NULL,
  `author` VARCHAR(50) NOT NULL,
  `title` VARCHAR(50) NOT NULL,
  `cover` VARCHAR(50) NOT NULL,
  `edition` VARCHAR(5) NOT NULL,
  `publisher` VARCHAR(50) NOT NULL,
  `pubYear` INT(5) NOT NULL,
  `category` INT NOT NULL,
  PRIMARY KEY (`ISBN`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bookstore`.`userType`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bookstore`.`usertype` (
  `idUserType` INT NOT NULL,
  `userStatus` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idUserType`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bookstore`.`Users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bookstore`.`users` (
  `userID` INT NOT NULL AUTO_INCREMENT,
  `firstName` VARCHAR(45) NOT NULL,
  `lastName` VARCHAR(45) NOT NULL,
  `password` VARCHAR(100) NOT NULL,
  `email` VARCHAR(45) UNIQUE NOT NULL,
  `gender` VARCHAR(6) NULL,
  `phone` VARCHAR(20) NULL,
  `userTypeID` INT NOT NULL,
  `Subscription` TINYINT NULL,
  `active` TINYINT NOT NULL,
  `activationKey` INT NOT NULL,
  `suspended` INT NOT NULL,
  PRIMARY KEY (`userID`));


-- -----------------------------------------------------
-- Table `bookstore`.`Address`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bookstore`.`address` (
  `idAddress` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `street` VARCHAR(100) NOT NULL,
  `street2` VARCHAR(100) NULL,
  `zipCode` INT(10) NOT NULL,
  `city` VARCHAR(50) NOT NULL,
  `state` VARCHAR(30) NOT NULL,
  `AddressType` VARCHAR(10) NULL,
  `userID` INT NOT NULL,
  PRIMARY KEY (`idAddress`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bookstore`.`Payment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bookstore`.`payment` (
  `cardNumber` VARCHAR(100) NOT NULL,
  `expiryYear` INT NOT NULL,
  `expiryMonth` INT NOT NULL,
  `securityCode` INT(3) NULL,
  `nameoncard` VARCHAR(100) NULL,
  `paymentType` VARCHAR(15) NOT NULL,
  `UserID` INT NOT NULL,
  PRIMARY KEY (`UserID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bookstore`.`Promotion`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bookstore`.`promotion` (
  `idPromotion` INT NOT NULL AUTO_INCREMENT,
  `promoCode` VARCHAR(45) NOT NULL,
  `discountAmount` INT(5) NOT NULL,
  `startDate` DATE NOT NULL,
  `expirationDate` DATE NOT NULL,
  PRIMARY KEY (`idPromotion`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bookstore`.`Order`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bookstore`.`Order` (
  `orderID` INT NOT NULL AUTO_INCREMENT,
  `userID` INT NOT NULL,
  `total` INT NULL,
  `OrderDateTime` DATE NOT NULL,
  `AddressID` INT NOT NULL,
  `PromoID` INT NULL,
  `paymentID` INT NOT NULL,
  `orderStatus` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`orderID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bookstore`.`cartItems`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bookstore`.`cart` (
  `userID` INT NOT NULL,
  `bookID` INT NOT NULL,
  `quantity` INT(10) NOT NULL,
  PRIMARY KEY (`userID` ,`bookID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bookstore`.`orderItems`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bookstore`.`orderItems` (
  `idOrder_Product` INT NOT NULL AUTO_INCREMENT,
  `orderID` INT NOT NULL,
  `ProductID` INT NOT NULL,
  `quantity` INT NOT NULL,
  PRIMARY KEY (`idOrder_Product`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bookstore`.`bookInventory`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bookstore`.`bookinventory` (
  `idbookInventory` INT NOT NULL AUTO_INCREMENT,
  `bookID` INT NOT NULL,
  `bookStatus` VARCHAR(15) NULL,
  `buyingPrice` INT(10) NULL,
  `sellingPrice` INT(10) NULL,
  `quantity` INT(5) NULL,
  PRIMARY KEY (`idbookInventory`))
ENGINE = InnoDB;

INSERT INTO `usertype` (`idUserType`, `userStatus`) VALUES ('1', 'Admin');
INSERT INTO `usertype` (`idUserType`, `userStatus`) VALUES ('2', 'Registered User');
INSERT INTO `users` VALUES (1,'team3','admin','pbkdf2:sha256:150000$1EGsALIX$da3cd4923a0591df667460428594bb64da58a64f806c5febc9aa49032ca6d376','MdRedwan.Islam@uga.edu',NULL,'',1,1,1,1234,0);
INSERT INTO `promotion` (`promoCode`, `discountAmount`, `startDate`, `expirationDate`) VALUES ('50OFF', '50', '2020-02-14', '2020-04-14');
INSERT INTO `promotion` (`promoCode`, `discountAmount`, `startDate`, `expirationDate`) VALUES ('JUL04', '25', '2020-07-01', '2020-07-05');
INSERT INTO `promotion` (`promoCode`, `discountAmount`, `startDate`, `expirationDate`) VALUES ('LOYAL', '30', '2020-07-20', '2020-11-06');
INSERT INTO `category` (`category`) VALUES ('Romance');
INSERT INTO `category` (`category`) VALUES ('Technology');
INSERT INTO `category` (`category`) VALUES ('Fantasy');
INSERT INTO `category` (`category`) VALUES ('Mystery');
INSERT INTO `category` (`category`) VALUES ('History');
INSERT INTO `category` (`category`) VALUES ('Thriller');
