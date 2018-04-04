DROP DATABASE IF EXISTS composizioneclassi;

CREATE DATABASE composizioneclassi;

USE composizioneclassi;

CREATE TABLE users(
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(64) NOT NULL,
  password VARCHAR(64) NOT NULL,
  priviledges INT(1) NOT NULL
);

CREATE TABLE classi(
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome CHAR(4) NOT NULL,
  anno CHAR(9) NOT NULL
);

CREATE TABLE classi_composte(
  classe INT NOT NULL,
  alunno INT NOT NULL,
  PRIMARY KEY (classe, alunno)
);

CREATE TABLE indirizzi(
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(50) NOT NULL
);

CREATE TABLE alunni(
  id INT AUTO_INCREMENT PRIMARY KEY,
  cognome VARCHAR(128) NOT NULL,
  nome VARCHAR(128) NOT NULL,
  matricola VARCHAR(50) NOT NULL,
  cf CHAR(16) NOT NULL,
  desiderata CHAR(16) DEFAULT NULL,
  sesso CHAR(1) NOT NULL,
  data_nascita VARCHAR(15) NOT NULL,
  cap VARCHAR(5) NOT NULL,
  nazionalita VARCHAR(25) NOT NULL,
  legge_107 CHAR(1) DEFAULT NULL,
  legge_104 CHAR(1) DEFAULT NULL,
  classe_precedente INT DEFAULT NULL,
  classe_successiva INT DEFAULT NULL,
  anno_scolastico CHAR(9) NOT NULL,
  scelta_indirizzo INT NOT NULL,
  cod_cat CHAR(4) NOT NULL,
  voto INT(2) NOT NULL,
  proprietario INT NOT NULL
);

CREATE TABLE configurazione(
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(64) NOT NULL,
  min_alunni INT(3) NOT NULL,
  max_alunni INT(3) NOT NULL,
  numero_femmine INT(3) NOT NULL,
  numero_maschi INT(3) NOT NULL,
  max_per_cap INT(3) NOT NULL,
  max_per_naz INT(3) NOT NULL,
  max_naz INT(3) NOT NULL,
  num_104 INT(3) NOT NULL
);


