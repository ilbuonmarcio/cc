<?php

  // Includo il file per la connessione al dabatase
  include("dbconnection.php");

  // Prendo in POST i valori per la creazione della configurazione

  $configname = $_POST["configname"];
  $rangevalue_lower = $_POST["rangevalue_lower"];
  $rangevalue_upper = $_POST["rangevalue_upper"];
  $num_males = $_POST["num_males"];
  $num_females = $_POST["num_females"];
  $num_cap = $_POST["num_cap"];
  $num_170 = $_POST["num_170"];
  $num_naz = $_POST["num_naz"];
  $num_x_naz = $_POST["num_x_naz"];

  // Creo un istanza di connessione al database
  $conn = connectdb();

  // Controllo se la connessione é disponibile
  if($conn){

    $sql = "INSERT INTO configurazioni (id, nome, min_alunni, max_alunni, numero_femmine, numero_maschi, max_per_cap, max_per_naz, max_naz, num_170) VALUES";
    $sql .= "(NULL, '" . $configname . "', " . $rangevalue_lower . ", " . $rangevalue_upper . ", " . $num_females . ", " . $num_males . ", " . $num_cap . ", " . $num_naz . ", " . $num_x_naz . ", " . $num_170 . ")";

    if ($conn->query($sql) === true) {
      echo "{
        status: 'Query Executed',
        querystatus : 'Good'
      }";
    } else {
      echo '{
        status: "Query Executed",
        querystatus : "Bad",
        executedquery : "' . $sql . '"
      }';
    }
  } else {
    echo "{
      status: 'No Database Connection',
      querystatus: 'Bad'
    }";
  }
?>
