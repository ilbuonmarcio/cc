<?php

  if(isset($_POST["ajaxrefreshrequest"]) && $_POST["ajaxrefreshrequest"] == true){
    include('../utils/db.php');
  }

  if(!isset($conn)){
     $conn = connectdb();
  }

  $conn = connectdb();

  if($conn){
    $query = "SELECT * FROM configurazioni;";
    $result = $conn->query($query);

    if ($result->num_rows > 0) {
      while($row = $result->fetch_assoc()){
         echo '<option value="' . $row["id"] . '">' . $row["nome"] . '</option>';
       }
      }
    } else {
      echo '<option value="0" disabled>Impossibile connettersi al database.</option>';
    }

?>
