CREATE DATABASE library_management_database;

CREATE TABLE Books (
id INT AUTO_INCREMENT PRIMARY KEY,
title VARCHAR(255) NOT NULL,
author_id INT NOT NULL,
FOREIGN KEY (author_id) REFERENCES Authors(id),
genre_id INT NOT NULL,
FOREIGN KEY (genre_id) REFERENCES Genres(id),
isbn VARCHAR(13) NOT NULL UNIQUE,
publication_date DATE,
availability BOOLEAN DEFAULT 1);

CREATE TABLE Authors (
id INT AUTO_INCREMENT Primary Key,
name VARCHAR(255) NOT NULL, 
home_country VARCHAR(100) NOT NULL);

CREATE TABLE Genres (
id INT AUTO_INCREMENT PRIMARY KEY, 
name VARCHAR(255) NOT NULL,
fict_or_nonfict VARCHAR(11) NOT NULL,
description TEXT);

CREATE TABLE Users (
id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(255) NOT NULL,
card_number VARCHAR(10) NOT NULL UNIQUE);

CREATE TABLE BorrowedBooks (
id INT AUTO_INCREMENT PRIMARY KEY,
user_id INT,
FOREIGN KEY (user_id) REFERENCES users(id),
book_id INT,
FOREIGN KEY (book_id) REFERENCES books(id),
borrow_date DATE NOT NULL,
return_date DATE);

--