-- SQL script that creates a table users
CREATE TABLE users IF NOT EXISTS (PRIMARY KEY(id INT NOT NULL), email VARCHAR(255) NOT NULL UNIQUE, name VARCHAR(255));
