-- FRESH INSTALL, WILL DELETE AN EXISTING ONE!!!
DROP DATABASE mysqlkikbot; 

-- Create the user for the database
-- Not gonna show my pw :)
-- CREATE USER 'rip-mysql'@'localhost' IDENTIFIED BY password;

-- Create the actual db
CREATE DATABASE mysqlkikbot; -- CREATE DATABASE [IF NOT EXISTS] mysqlkikbot

-- This should be already InnoDB, but let's make sure.
SET default_storage_engine=INNODB;

-- Give the permissions for the user for the database
GRANT ALL PRIVILEGES ON mysqlkikbot.* TO 'rip-mysql'@'localhost';

USE mysqlkikbot;

/* Create the required tables */

CREATE TABLE IF NOT EXISTS group_chat(
	id INT AUTO_INCREMENT PRIMARY KEY,
	group_jid NVARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS group_chat_illegal_phrases(
	id INT AUTO_INCREMENT PRIMARY KEY,
	group_chat_id INT,
	phrase_text LONGTEXT,

	FOREIGN KEY (group_chat_id) REFERENCES group_chat(id)
);