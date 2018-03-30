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

  // Controllo se la connessione non é disponibile
  if($conn){

    $sql = "SELECT username, password FROM users;";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {

      while($row = $result->fetch_assoc()) {
        if($username == $row["username"] && $password == $row["password"]){
          // echo $row["username"] . " - " . $row["password"] . " found!<br>";
          // Sessione autenticata correttamente
          $_SESSION["authenticated"] = 1;

          header("Location: ../index.php");

        }
      }
      // Sessione non autenticata, nessun match trovato
      header("Location: ../login.php?unf=1");
    }
  } else {

    // Impossibile instaurare una connessione al database
    header("Location: ../login.php?nodbc=1");

  }
?>
