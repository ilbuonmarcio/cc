<?php

  // Includo il file per la connessione al dabatase
  include("dbconnection.php");

  // Prendo in POST i valori per la creazione gruppo
  $groupname = $_POST["groupname"];
  $description = $_POST["description"];
  $creategroup_type = $_POST["creategroup-type"];

  // Creo un istanza di connessione al database
  $conn = connectdb();

  // Controllo se la connessione é disponibile
  if($conn){

    // Nessun match trovato, creazione account!
    $sql = "INSERT INTO gruppi (id, nome, tipo,  descrizione) VALUES (NULL, '" . $groupname . "', " . $creategroup_type . ", '" . $description . "');";

    if($conn->query($sql) === true){
      // Nuovo user creato, redirect in index.php
      header("Location: ../index.php?opengg=1&newgroupcreated=" . $groupname);
    } else{
      // Username giá in uso! redirect in index.php
      header("Location: ../index.php?opengg=1&gap=1&qerr=1");
    }
    
  } else {

    // Impossibile instaurare una connessione al database
    header("Location: ../login.php?nodbc=1");

  }
?>
