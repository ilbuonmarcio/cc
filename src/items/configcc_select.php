<?php

 if($conn){

   $query = "SELECT * FROM configurazioni;";

   $result = $conn->query($query);

   if ($result->num_rows > 0) {
     while($row = $result->fetch_assoc()){
       echo '<option value="' . $row["id"] . '">' . $row["nome"] . '</option>';
     }
   }
 } else {
   echo '<option required value="0" disabled>Impossibile connettersi al database.</option>';
 }

?>
