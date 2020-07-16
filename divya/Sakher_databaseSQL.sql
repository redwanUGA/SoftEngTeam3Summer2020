CREATE SCHEMA IF NOT EXISTS `Bookstore` ;
USE `Bookstore` ;

-- -----------------------------------------------------
-- Table `Bookstore`.`Category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Bookstore`.`Category` (
  `idCategory` INT NOT NULL AUTO_INCREMENT,
  `category` VARCHAR(15) NOT NULL,
  PRIMARY KEY (`idCategory`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Bookstore`.`Books`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Bookstore`.`Books` (
  `ISBN` INT NOT NULL,
  `author` VARCHAR(30) NOT NULL,
  `title` VARCHAR(50) NOT NULL,
  `cover` VARCHAR(30) NOT NULL,
  `edition` VARCHAR(5) NOT NULL,
  `publisher` VARCHAR(30) NOT NULL,
  `pubYear` INT(5) NOT NULL,
  `category` INT NOT NULL,
  PRIMARY KEY (`ISBN`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Bookstore`.`userType`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Bookstore`.`userType` (
  `idUserType` INT NOT NULL,
  `userStatus` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idUserType`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Bookstore`.`Users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Bookstore`.`Users` (
  `userID` INT NOT NULL AUTO_INCREMENT,
  `firstName` VARCHAR(45) NOT NULL,
  `lastName` VARCHAR(45) NOT NULL,
  `password` VARCHAR(100) NOT NULL,
  `email` VARCHAR(45) UNIQUE NOT NULL,
  `phone` VARCHAR(20) NULL,
  `userTypeID` INT NOT NULL,
  `Subscription` TINYINT NULL,
  `active` TINYINT NOT NULL,
  `activationKey` INT NOT NULL,
  `suspended` INT NOT NULL,
  PRIMARY KEY (`userID`));


-- -----------------------------------------------------
-- Table `Bookstore`.`Address`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Bookstore`.`Address` (
  `idAddress` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(15) NOT NULL,
  `street` VARCHAR(30) NOT NULL,
  `street2` VARCHAR(30) NULL,
  `zipCode` INT(5) NOT NULL,
  `city` VARCHAR(15) NOT NULL,
  `state` VARCHAR(30) NOT NULL,
  `country` VARCHAR(30) NOT NULL,
  `AddressType` VARCHAR(5) NULL,
  `userID` INT NOT NULL,
  PRIMARY KEY (`idAddress`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Bookstore`.`Payment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Bookstore`.`Payment` (
  `cardNumber` VARCHAR(100) NOT NULL,
  `expiryYear` INT NOT NULL,
  `expiryMonth` INT NOT NULL,
  `securityCode` INT(3) NULL,
  `paymentType` VARCHAR(15) NOT NULL,
  `UserID` INT NOT NULL,
  PRIMARY KEY (`UserID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Bookstore`.`Promotion`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Bookstore`.`Promotion` (
  `idPromotion` INT NOT NULL AUTO_INCREMENT,
  `promoCode` VARCHAR(45) NOT NULL,
  `discountAmount` INT(5) NOT NULL,
  `startDate` DATE NOT NULL,
  `expirationDate` DATE NOT NULL,
  PRIMARY KEY (`idPromotion`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Bookstore`.`Order`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Bookstore`.`Order` (
  `orderID` INT NOT NULL AUTO_INCREMENT,
  `userID` INT NOT NULL,
  `total` INT NULL,
  `OrderDateTime` DATE NOT NULL,
  `AddressID` INT NOT NULL,
  `PromoID` INT NOT NULL,
  `paymentID` INT NOT NULL,
  PRIMARY KEY (`orderID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Bookstore`.`cartItems`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Bookstore`.`cart` (
  `userID` INT NOT NULL,
  `bookID` INT NOT NULL,
  `quantity` INT(10) NOT NULL,
  PRIMARY KEY (`userID` ,`bookID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Bookstore`.`orderItems`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Bookstore`.`orderItems` (
  `idOrder_Product` INT NOT NULL AUTO_INCREMENT,
  `orderID` INT NOT NULL,
  `ProductID` INT NOT NULL,
  `quantity` INT NOT NULL,
  PRIMARY KEY (`idOrder_Product`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Bookstore`.`bookInventory`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Bookstore`.`bookInventory` (
  `idbookInventory` INT NOT NULL AUTO_INCREMENT,
  `bookID` INT NOT NULL,
  `bookStatus` VARCHAR(15) NULL,
  `buyingPrice` INT(10) NULL,
  `sellingPrice` INT(10) NULL,
  `quantity` INT(5) NULL,
  PRIMARY KEY (`idbookInventory`))
ENGINE = InnoDB;