<?php

  // Includo il file per la connessione al dabatase
  include("dbconnection.php");

  // Prendo in POST i valori per la creazione utente
  $username = $_POST["username"];
  $password = $_POST["password"];
  $priviledges = $_POST["priviledges"];

  // Creo un istanza di connessione al database
  $conn = connectdb();

  // Controllo se la connessione é disponibile
  if($conn){

    $sql = "SELECT * FROM users WHERE username = '" . $username . "';";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {

      // Username giá in uso! redirect in index.php
      header("Location: ../index.php?uap=1");

    } else {

      // Nessun match trovato, creazione account!
      $sql = "INSERT INTO users (id, username, password, priviledges) VALUES (NULL, '" . $username . "', '" . $password . "', " . $priviledges . ");";

      if($conn->query($sql) === true){
        // Nuovo user creato, redirect in index.php
        header("Location: ../index.php?newusercreated=" . $username);
      } else{
        // Errore nella query, redirect in index.php
        header("Location: ../index.php?qerr=1");
      }
    }
  } else {

    // Impossibile instaurare una connessione al database
    header("Location: ../login.php?nodbc=1");

  }
?>
