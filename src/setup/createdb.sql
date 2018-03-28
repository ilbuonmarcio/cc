DROP DATABASE IF EXISTS composizioneclassi;

CREATE DATABASE composizioneclassi;

USE composizioneclassi;

CREATE TABLE users(
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(64) NOT NULL,
  password CHAR(255) NOT NULL,
  diritti INT(1) NOT NULL
);
