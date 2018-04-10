<?php


  include("../utils/db.php");

  // Prendo in POST i valori per la creazione gruppo
  $groupname = $_POST["groupname"];
  $groupdesc = $_POST["groupdesc"];
  $grouptype = $_POST["grouptype"];

  // Creo un istanza di connessione al database
  $conn = connectdb();

  // Controllo se la connessione é disponibile
  if($conn){

    // Nessun match trovato, creazione account!
    $sql = "INSERT INTO gruppi (id, nome, tipo,  descrizione) VALUES (NULL, '" . $groupname . "', " . $grouptype . ", '" . $groupdesc . "');";

    if ($conn->query($sql) === true) {
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
  }
  else {
    echo "{
      status: 'No Database Connection',
      querystatus: 'bad'
      }";
  }
?>
