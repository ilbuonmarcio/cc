<?php
  session_start();
  include("dbconnection.php");

  $username = $_POST["username"];
  $password = $_POST["password"];

  $conn = connectdb();

  if($conn){

    $sql = "SELECT * FROM utenti WHERE username = '" . $username . "';";
    $result = $conn->query($sql);

    if ($result->num_rows == 1) {

        $row = $result->fetch_assoc();

        if(password_verify($password, $row["password"])){

          $_SESSION["authenticated"] = 1;
          $_SESSION["username"] = $username;
          header("Location: ../index.php");

        } else{

            header("Location: ../login.php?wp=1");

        }

    } else {

        header("Location: ../login.php?unf=1");

    }
  } else {

    header("Location: ../login.php?nodbc=1");

  }
?>
