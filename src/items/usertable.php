<?php

    if(isset($_POST["standalone"]) && $_POST["standalone"] == true){
      include('../utils/dbconnection.php');
    }

    if(!isset($conn)){
       $conn = connectdb();
    }

   if($conn){

     $query = "SELECT id, username, diritti FROM utenti;";

     $result = $conn->query($query);

     if ($result->num_rows > 0) {
       echo '<table style="box-shadow: 1px 1px 10px #BBBBBB;" class="striped centered">
         <thead>
           <tr>
               <th>ID</th>
               <th>Username</th>
               <th>Tipologia</th>
           </tr>
         </thead>

         <tbody>';
       while($row = $result->fetch_assoc()) {
         if($row["diritti"] == 0){
           $type = "Amministratore";
         } else if($row["diritti"] == 1){
           $type = "Editor";
         } else if($row["diritti"] == 2){
           $type = "Visualizzatore";
         } else{
           continue;
         }
         echo '<tr>
                 <td>' . $row["id"]                                           . '</td>
                 <td>' . $row["username"]                                    . '</td>
                 <td>' . $type                                                  . '</td>';
          echo '</tr>';
       }
       echo '
     </tbody>
   </table>';
     }
   } else{
     echo '<p class="center-align" style="color: red;">Tabella non disponibile! Errore di connessione al database.</p>';
   }

 ?>
