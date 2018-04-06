<?php

  // Includo il file per la connessione al dabatase
  include("dbconnection.php");

  // Prendo in POST i valori per la creazione gruppo
  $deletegroup_select = $_POST["deletegroup-select"];

  // Creo un istanza di connessione al database
  $conn = connectdb();

  // Controllo se la connessione é disponibile
  if($conn){

    $removeAlumni = "DELETE FROM alunni WHERE alunni.id_gruppo = " . $deletegroup_select . ";";
    $removeGroup = "DELETE FROM gruppi WHERE gruppi.id = " . $deletegroup_select . ";";

    if($conn->query($removeAlumni) === true && $conn->query($removeGroup)){
      header("Location: ../index.php?gr=1");
    } else{
      header("Location: ../index.php?qerr=1");
    }

  } else {

    // Impossibile instaurare una connessione al database
    header("Location: ../login.php?nodbc=1");

  }
?>
