<?php

  session_start();

  include("dbconnection.php");

  $username = $_GET["username"];
  $password = $_GET["password"];

  $conn = connectdb();

  if($conn){
    $sql = "SELECT * FROM users WHERE username = '" . $username . "' AND password = '" . $password . "';";

    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
      $_SESSION["authenticated"] = 1;
      header("Location: ../index.php");
    } else {
        header("Location: ../login.php?usernotfound=1");
    }
  } else{
    header("Location: ../login.php?nodbconnection=1");
  }
?>
