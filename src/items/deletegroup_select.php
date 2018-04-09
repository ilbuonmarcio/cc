<?php

include("utils/dbconnection.php");

$conn = connectdb();

if($conn){
  $query = "SELECT * FROM gruppi;";
  $result = $conn->query($query);

  if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()){
       if($row["tipo"] == 1){ù
         $type = "Classi Prime";
       } else if($row["tipo"] == 3){
         $type = "Classi Terze";
       } else {
         continue;
       }
       echo '<option value="' . $row["id"] . '">' . $row["nome"] . ' - ' . $type . '</option>';
     }
    }
  } else {
    echo '<option value="0" disabled>Impossibile connettersi al database.</option>';
  }

?>
