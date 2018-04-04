<?php

  // Inizializzo la sessione se non ancora inizializzata
  // ed includo il file per la connessione al dabatase
  session_start();
  include("dbconnection.php");

  // Prendo in POST i valori di login
  $username = $_POST["username"];
  $password = $_POST["password"];

  // Creo un istanza di connessione al database
  $conn = connectdb();

  // Controllo se la connessione é disponibile
  if($conn){

    $sql = "SELECT * FROM users WHERE username = '" . $username . "' AND password = '" . $password . "';";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {

          // Sessione autenticata correttamente
          $_SESSION["authenticated"] = 1;
          $_SESSION["username"] = $username;
          header("Location: ../index.php");

    } else {

        // Sessione non autenticata, nessun match trovato
        header("Location: ../login.php?unf=1");

    }
  } else {

    // Impossibile instaurare una connessione al database
    header("Location: ../login.php?nodbc=1");

  }
?>
