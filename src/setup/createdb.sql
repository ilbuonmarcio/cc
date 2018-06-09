DROP DATABASE IF EXISTS composizioneclassi;

CREATE DATABASE composizioneclassi DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_unicode_ci;

USE composizioneclassi;

CREATE TABLE utenti(
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(64) NOT NULL,
  password CHAR(255) NOT NULL,
  diritti INT(1) NOT NULL
);

CREATE TABLE classi_composte(
  groupid INT NOT NULL,
  configid INT NOT NULL,
  studentid INT NOT NULL,
  PRIMARY KEY (groupid, configid, studentid)
);

CREATE TABLE indirizzi(
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(50) NOT NULL
);

CREATE TABLE gruppi(
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(50) NOT NULL,
  tipo INT(1) DEFAULT 0,
  descrizione VARCHAR(256) DEFAULT '',
  UNIQUE INDEX(nome)
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
  legge_170 CHAR(1) DEFAULT NULL,
  legge_104 CHAR(1) DEFAULT NULL,
  classe_precedente INT DEFAULT NULL,
  classe_successiva INT DEFAULT NULL,
  scelta_indirizzo INT NOT NULL,
  cod_cat CHAR(4) NOT NULL,
  voto INT(2) NOT NULL,
  id_gruppo INT NOT NULL,
  FOREIGN KEY (id_gruppo) REFERENCES gruppi(id),
  FOREIGN KEY (scelta_indirizzo) REFERENCES indirizzi(id),
  UNIQUE INDEX(matricola, cf, id_gruppo)
);

CREATE TABLE configurazioni(
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(64) NOT NULL,
  min_alunni INT(3) NOT NULL,
  max_alunni INT(3) NOT NULL,
  numero_femmine INT(3) DEFAULT NULL,
  numero_maschi INT(3) DEFAULT NULL,
  max_per_cap INT(3) NOT NULL,
  max_per_naz INT(3) NOT NULL,
  max_naz INT(3) NOT NULL,
  num_170 INT(3) NOT NULL,
  UNIQUE INDEX(nome)
);

INSERT INTO utenti (
  id,
  username,
  password,
  diritti
) VALUES (1, 'root', '$2y$10$Zl0xCv5YSf/6HFF53VxJlORx5APtdmAZBJTdy3ciAnwF68AdKabtG', 0);

INSERT INTO `configurazioni` (
  `id`,
  `nome`,
  `min_alunni`,
  `max_alunni`,
  `numero_femmine`,
  `numero_maschi`,
  `max_per_cap`,
  `max_per_naz`,
  `max_naz`,
  `num_170`
) VALUES (NULL, 'Configurazione di Default', '16', '28', '3', NULL, '6', '6', '5', '2');

INSERT INTO indirizzi (
  id,
  nome
) VALUES (
  1, 'Informatica'
), (
  2, 'Elettronica'
), (
  3, 'Logistica'
), (
  4, 'Telecomunicazioni'
), (
  5, 'Costruzione del Mezzo'
);

INSERT INTO gruppi (
  id,
  nome,
  tipo
) VALUES (
  NULL, 'Gruppo 1', 3
), (
  NULL, 'Gruppo 2', 1
), (
  NULL, 'Gruppo 3', 3
);
