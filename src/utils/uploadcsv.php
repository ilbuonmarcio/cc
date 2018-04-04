<?php

  include("dbconnection.php");

  $tmpName = $_FILES['csv']['tmp_name'];
  $csvAsArray = array_map('str_getcsv', file($tmpName));

  $conn = connectdb();

  if($conn){
    $query = "SELECT * FROM alunni;";

    $result = $conn->query($query);

    if ($result->num_rows > 0) {
      while($row = $result->fetch_assoc()) {
        echo $row["cf"];
      }
    }
  } else{
    header("Location: ../index.php?nodbc=1");
  }

?>
