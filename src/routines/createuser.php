<?php

  include("../utils/db.php");

  $username = $_POST["username"];
  $password = $_POST["password"];
  $priviledges = $_POST["priviledges"];

  $conn = connectdb();

  if($conn){

    $sql = "SELECT * FROM utenti WHERE username = '" . $username . "';";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {

      echo "{
        status: 'Username already present!',
        querystatus: 'bad'
      }";

    } else {

      // Nessun match trovato, creazione account!
      $sql = "INSERT INTO utenti (id, username, password, diritti) VALUES (NULL, '" . $username . "', '" . password_hash($password, PASSWORD_DEFAULT) . "', " . $priviledges . ");";

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
  } else {
    echo "{
      status: 'No Database Connection',
      querystatus: 'bad'
    }";
  }
?>
