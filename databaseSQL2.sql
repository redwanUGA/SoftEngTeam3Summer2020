-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema Bookstore
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema Bookstore
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `Bookstore` ;
USE `Bookstore` ;

-- -----------------------------------------------------
-- Table `Bookstore`.`Category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Bookstore`.`Category` (
  `idCategory` INT NOT NULL,
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
  `userID` INT NOT NULL,
  `firstName` VARCHAR(45) NOT NULL,
  `lastName` VARCHAR(45) NOT NULL,
  `password` VARCHAR(12) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `phone` INT(15) NULL,
  `userTypeID` INT NOT NULL,
  `Subscription` TINYINT NULL,
  PRIMARY KEY (`userID`));


-- -----------------------------------------------------
-- Table `Bookstore`.`Address`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Bookstore`.`Address` (
  `idAddress` INT NOT NULL,
  `name` VARCHAR(15) NOT NULL,
  `street` VARCHAR(30) NOT NULL,
  `street2` VARCHAR(30) NULL,
  `zipCode` INT(5) NOT NULL,
  `city` VARCHAR(15) NOT NULL,
  `state` VARCHAR(30) NOT NULL,
  `country` VARCHAR(30) NOT NULL,
  `AddressType` VARCHAR(5) NULL,
  `userID` INT NULL,
  PRIMARY KEY (`idAddress`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Bookstore`.`Payment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Bookstore`.`Payment` (
  `cardNumber` INT NOT NULL,
  `name` VARCHAR(11) NOT NULL,
  `expirationDate` DATE NOT NULL,
  `securityCode` INT(3) NOT NULL,
  `paymentType` VARCHAR(15) NULL,
  `UserID` INT NOT NULL,
  PRIMARY KEY (`cardNumber`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Bookstore`.`Promotion`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Bookstore`.`Promotion` (
  `idPromotion` INT NOT NULL,
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
  `orderID` INT NOT NULL,
  `userID` INT NOT NULL,
  `total` INT NULL,
  `OrderDateTime` DATE NOT NULL,
  `AddressID` INT NOT NULL,
  `PromoID` INT NOT NULL,
  `paymentID` INT NOT NULL,
  PRIMARY KEY (`orderID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Bookstore`.`Cart`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Bookstore`.`Cart` (
  `idCart` INT NOT NULL,
  `userID` INT NOT NULL,
  `orderID` INT NOT NULL,
  PRIMARY KEY (`idCart`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Bookstore`.`cartItems`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Bookstore`.`cartItems` (
  `idcartItems` INT NOT NULL,
  `cartID` INT NOT NULL,
  `bookID` INT NOT NULL,
  `quantity` INT(10) NOT NULL,
  PRIMARY KEY (`idcartItems`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Bookstore`.`orderItems`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Bookstore`.`orderItems` (
  `idOrder_Product` INT NOT NULL,
  `orderID` INT NOT NULL,
  `ProductID` INT NOT NULL,
  `quantity` INT NOT NULL,
  PRIMARY KEY (`idOrder_Product`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Bookstore`.`bookInventory`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Bookstore`.`bookInventory` (
  `idbookInventory` INT NOT NULL,
  `bookID` INT NOT NULL,
  `bookStatus` VARCHAR(15) NULL,
  `buyingPrice` INT(10) NULL,
  `sellingPrice` INT(10) NULL,
  `quantity` INT(5) NULL,
  PRIMARY KEY (`idbookInventory`))
ENGINE = InnoDB;

CREATE USER 'user1';


-- -----------------------------------------------------
-- Data for table `Bookstore`.`Category`
-- -----------------------------------------------------
START TRANSACTION;
USE `Bookstore`;
INSERT INTO `Bookstore`.`Category` (`idCategory`, `category`) VALUES (1, 'ActionAdventure');
INSERT INTO `Bookstore`.`Category` (`idCategory`, `category`) VALUES (2, 'ScienceFiction');
INSERT INTO `Bookstore`.`Category` (`idCategory`, `category`) VALUES (3, 'Fantasy');
INSERT INTO `Bookstore`.`Category` (`idCategory`, `category`) VALUES (4, 'Romance');
INSERT INTO `Bookstore`.`Category` (`idCategory`, `category`) VALUES (5, 'Suspense');
INSERT INTO `Bookstore`.`Category` (`idCategory`, `category`) VALUES (6, 'Thriller');
INSERT INTO `Bookstore`.`Category` (`idCategory`, `category`) VALUES (7, 'YoungAdult');
INSERT INTO `Bookstore`.`Category` (`idCategory`, `category`) VALUES (8, 'Horror');
INSERT INTO `Bookstore`.`Category` (`idCategory`, `category`) VALUES (9, 'Mystery');
INSERT INTO `Bookstore`.`Category` (`idCategory`, `category`) VALUES (10, 'Historical');
INSERT INTO `Bookstore`.`Category` (`idCategory`, `category`) VALUES (11, 'Education');
INSERT INTO `Bookstore`.`Category` (`idCategory`, `category`) VALUES (12, 'GraphicNovel');
INSERT INTO `Bookstore`.`Category` (`idCategory`, `category`) VALUES (13, 'Art');
INSERT INTO `Bookstore`.`Category` (`idCategory`, `category`) VALUES (14, 'SelfHelp');
INSERT INTO `Bookstore`.`Category` (`idCategory`, `category`) VALUES (15, 'Health');
INSERT INTO `Bookstore`.`Category` (`idCategory`, `category`) VALUES (16, 'Children');

COMMIT;


-- -----------------------------------------------------
-- Data for table `Bookstore`.`userType`
-- -----------------------------------------------------
START TRANSACTION;
USE `Bookstore`;
INSERT INTO `Bookstore`.`userType` (`idUserType`, `userStatus`) VALUES (1, 'Customer');
INSERT INTO `Bookstore`.`userType` (`idUserType`, `userStatus`) VALUES (2, 'Admin');

COMMIT;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
