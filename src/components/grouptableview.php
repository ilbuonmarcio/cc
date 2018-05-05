<?php

    if(isset($_POST["ajaxrefreshrequest"]) && $_POST["ajaxrefreshrequest"] == true){
      include('../utils/db.php');
    }

    if(!isset($conn)){
       $conn = connectdb();
    }

   if($conn){

     $query = "SELECT gruppi.id, gruppi.nome, gruppi.descrizione, gruppi.tipo, COUNT(alunni.id_gruppo) as numero_alunni FROM alunni RIGHT JOIN gruppi ON alunni.id_gruppo = gruppi.id GROUP BY gruppi.id;";

     $result = $conn->query($query);

     if ($result->num_rows > 0) {
       echo '<table style="box-shadow: 1px 1px 10px #BBBBBB;" class="striped centered">
         <thead>
           <tr>
               <th>Nome</th>
               <th>Descrizione</th>
               <th>Tipo</th>
               <th>Numero Alunni</th>
               <th>Link</th>
           </tr>
         </thead>

         <tbody>';
       while($row = $result->fetch_assoc()) {
         if($row["tipo"] == 1){
           $type = "Classi Prime";
         } else if($row["tipo"] == 3){
           $type = "Classi Terze";
         } else {
           continue;
         }
         echo '<tr>
                 <td>' . $row["nome"]                                           . '</td>
                 <td>' . $row["descrizione"]                                    . '</td>
                 <td>' . $type                                                  . '</td>
                 <td>' . $row["numero_alunni"]                                  . '</td>
                 <td>';

                 if($row["numero_alunni"] > 0){
                   echo '<a target="_blank" href="viewer.php?groupid=' . $row["id"] . "&groupname=" . $row["nome"] . '">Visualizza</a>';
                 }
          echo '</td>
              </tr>';
       }
       echo '
     </tbody>
   </table>';
     }
   } else{
     echo '<p class="center-align" style="color: red;">Tabella non disponibile! Errore di connessione al database.</p>';
   }

 ?>
