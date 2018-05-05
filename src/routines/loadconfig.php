<?php

  ini_set('display_errors', 1);
  ini_set('display_startup_errors', 1);
  error_reporting(E_ALL);

  // Includo il file per la connessione al dabatase
  include("../utils/db.php");

  // Prendo in POST i valori per la creazione gruppo
  $configid = $_POST["configid"];

  // Creo un istanza di connessione al database
  $conn = connectdb();

  // Controllo se la connessione é disponibile
  if($conn){

    $loadConfig = "SELECT * FROM configurazioni WHERE id = '" . $configid . "';";

    $result = $conn->query($loadConfig);

    if($result){
      while($row = $result->fetch_assoc()){
        echo "{
          status: 'Query Executed',
          querystatus : 'good',
          values : {
            configid : '" . $row['id'] . "',
            configname : '" . $row['nome'] . "',
            min_alunni : '" . $row['min_alunni'] . "',
            max_alunni : '" . $row['max_alunni'] . "',
            numero_femmine : '" . $row['numero_femmine'] . "',
            numero_maschi : '" . $row['numero_maschi'] . "',
            max_per_cap : '" . $row['max_per_cap'] . "',
            max_per_naz : '" . $row['max_per_naz'] . "',
            max_naz : '" . $row['max_naz'] . "',
            num_170 : '" . $row['num_170'] . "'
          }
        }";
      }
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
