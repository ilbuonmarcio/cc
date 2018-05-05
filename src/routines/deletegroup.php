<?php

  // Includo il file per la connessione al dabatase
  include("../utils/db.php");

  // Prendo in POST i valori per la creazione gruppo
  $groupname = $_POST["groupname"];

  // Creo un istanza di connessione al database
  $conn = connectdb();

  // Controllo se la connessione é disponibile
  if($conn){

    $removeAlumni = "DELETE FROM alunni WHERE alunni.id_gruppo = " . $groupname . ";";
    $removeGroup = "DELETE FROM gruppi WHERE gruppi.id = " . $groupname . ";";

    if($conn->query($removeAlumni) === true && $conn->query($removeGroup)){
      echo "{
        status: 'Query Executed',
        querystatus : 'good'
      }";
    } else {
      echo '{
        status: "Query Executed",
        querystatus : "bad",
        executedquery : "' . $sql . '"
      }';
    }

  } else {
    echo "{
      status: 'No Database Connection',
      querystatus: 'bad'
    }";
  }
?>
