<?php

  // Includo il file per la connessione al dabatase
  include("dbconnection.php");

  // Prendo in POST i valori per la creazione utente
  $username = $_POST["username"];
  $password = $_POST["password"];
  $diritti = $_POST["diritti"];

  // Creo un istanza di connessione al database
  $conn = connectdb();

  // Controllo se la connessione é disponibile
  if($conn){

    $sql = "SELECT * FROM utenti WHERE username = '" . $username . "';";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {

      // Username giá in uso! redirect in index.php
      header("Location: ../index.php?uap=1");

    } else {

      // Nessun match trovato, creazione account!
      $sql = "INSERT INTO utenti (id, username, password, diritti) VALUES (NULL, '" . $username . "', '" . password_hash($password, PASSWORD_DEFAULT) . "', " . $diritti . ");";

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
