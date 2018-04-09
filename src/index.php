<?php session_start(); ?>
<?php include('utils/utils.php'); ?>
<?php redirectIfNotLogon(); ?>

<!DOCTYPE html>

<html>

<head>
  <title>Home - CC</title>

  <!-- Compiled and minified noUISlider -->
  <link rel="stylesheet" href="css/nouislider.css">
  <script src="js/nouislider.min.js"></script>

  <!-- MaterializeIcons -->
  <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">

  <!-- Compiled and minified CSS -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-beta/css/materialize.min.css">

  <!-- Compiled and minified JavaScript -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-beta/js/materialize.min.js"></script>

  <!-- Compiled and minified jQuery -->
  <script src="https://code.jquery.com/jquery-3.3.1.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8="
    crossorigin="anonymous"></script>


  <!--Let browser know website is optimized for mobile-->
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <link href="css/base.css" type="text/css" rel="stylesheet" />

</head>

<body>

  <ul id="slide-out" class="sidenav " style="background-color: #eeeeee;">
    <li>
      <p class="sidenav-menu-title center-align">Menu - CC</p>
    </li>
    <li>
      <a onclick="createUserModal.open();" href="#!" class="waves-effect">
        <i class="material-icons">person_add</i>Aggiungi Nuovo Account</a>
    </li>
    <li>
      <div class="divider"></div>
    </li>
    <li>
      <a onclick="manageGroupsModal.open();" href="#!" class="waves-effect">
        <i class="material-icons">group</i>Gestisci Gruppi</a>
    </li>
    <li>
      <a onclick="uploadCSVModal.open();" href="#!" class="waves-effect">
        <i class="material-icons">cloud_upload</i>Carica CSV Alunni</a>
    </li>
    <li>
      <a onclick="configCCModal.open();" href="#!" class="waves-effect">
        <i class="material-icons">settings</i>Configura Parametri CC</a>
    </li>
    <li>
      <a onclick="genCCModal.open();" href="#!" class="waves-effect">
        <i class="material-icons">control_point</i>Genera CC</a>
    </li>
    <li>
      <div class="divider"></div>
    </li>
    <li>
      <a href="#!" class="waves-effect">
        <i class="material-icons">visibility</i>Visualizza CC</a>
    </li>
    <li>
      <a href="#!" class="waves-effect">
        <i class="material-icons">file_download</i>Scarica CC</a>
    </li>
    <li>
      <a href="login.php" class="waves-effect">
        <i class="material-icons">exit_to_app</i>Esci</a>
    </li>
  </ul>
  <a href="#" id="sidenav-trigger-button" data-target="slide-out" class="sidenav-trigger show-on-large btn btn-floating btn-large green">
    <i class="material-icons">menu</i>
  </a>

  <!-- Modulo per la creazione degli account -->
  <div id="create-user-panel" onclick="createUserModal.open();" class="modal modal-fixed-footer createuser-modal">
    <div class="modal-content">
      <h4 class="center-align">Aggiungi Nuovo Account</h4>

      <form class="col s12 createuser-form" action="./utils/createuser.php" method="post">
        <div class="row">

          <div class="input-field col s12">
            <i class="material-icons prefix">account_circle</i>
            <input pattern=".{3,}" required placeholder="Inserisci nome utente" id="username" name="username" type="text" class="validate">
            <label for="username">Nome Utente (Minimo 3 caratteri)</label>
          </div>

          <div class="input-field col s12">
            <i class="material-icons prefix">security</i>
            <input pattern=".{3,}" required placeholder="Inserisci password" id="password" name="password" type="text" class="validate">
            <label for="password">Password (Minimo 3 caratteri)</label>
          </div>

          <div class="input-field col s12">
            <select id="diritti" name="diritti">
              <option value="0">Amministratore</option>
              <option value="1" selected>Editor</option>
              <option value="2">Visualizzatore</option>
            </select>
            <label>Seleziona Permessi</label>
          </div>

          <div class="input-field col s12 center-align">
            <button class="btn waves-effect waves-light" type="submit" name="action">
              Crea Nuovo Account
            </button>
          </div>
        </div>
      </form>

    </div>

    <div class="modal-footer">
      <a href="#!" onclick="createUserModal.close();" class="modal-action modal-close waves-effect waves-green btn-flat">Chiudi</a>
    </div>
  </div>
  <!-- Fine modulo per la creazione degli account -->

  <!-- Modulo per la gestione dei gruppi -->
  <div id="manage-groups-panel" onclick="manageGroupsModal.open();" class="modal modal-fixed-footer managegroups-modal">
    <div class="modal-content">
      <h4 class="center-align">Gestisci Gruppi</h4>

      <div class="row">
        <div id="managegroups-table" class="col s12 center-align">
          <h6 class="center-align">Lista Gruppi</h6>
          <?php

             include("utils/dbconnection.php");

             $conn = connectdb();

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
        </div>
      </div>

      <div class="divider"></div>

      <div class="row">

        <form class="col s12 creategroup-form" action="./utils/creategroup.php" method="post">
          <div class="row">
            <h6 class="center-align">Crea Nuovo Gruppo</h6>

            <div class="input-field col s12">
              <i class="material-icons prefix">group</i>
              <input pattern=".{3,}" required placeholder="Inserisci nome nuovo gruppo" id="groupname" name="groupname" type="text" class="validate">
              <label for="groupname">Nome Gruppo (Minimo 3 caratteri)</label>
            </div>

            <div class="input-field col s12">
              <i class="material-icons prefix">description</i>
              <input placeholder="Inserisci descrizione (facoltativa)" id="description" name="description" type="text" class="validate">
              <label for="description">Descrizione (facoltativa)</label>
            </div>

            <div class="input-field col s12">
              <select id="creategroup-select" name="creategroup-select">
                <option value="1" selected>Classi Prime</option>
                <option value="3">Classi Terze</option>
              </select>
              <label>Seleziona Tipo</label>
            </div>

            <div class="input-field col s12 center-align">
              <button class="btn waves-effect waves-light" type="submit" name="action">
                Crea Gruppo
              </button>
            </div>

          </div>
        </form>

      </div>

      <div class="divider"></div>

      <div class="row">

        <form class="col s12 deletegroup-form" action="./utils/deletegroup.php" method="post">
          <div class="row">
            <h6 class="center-align">Elimina Gruppo</h6>

            <div class="input-field col s9">
              <select id="deletegroup-select" name="deletegroup-select">
                <?php

                 if($conn){

                   $query = "SELECT * FROM gruppi;";

                   $result = $conn->query($query);

                   if ($result->num_rows > 0) {
                     while($row = $result->fetch_assoc()){
                       if($row["tipo"] == 1){
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
              </select>
              <label>Seleziona Gruppo</label>
            </div>

            <div class="input-field col s3 center-align">
              <button class="btn waves-effect waves-light" type="submit" name="action">
                Cancella Gruppo
              </button>
            </div>

            <div class="col s12 center-align">
              <p style="color: red;">
                Attenzione! Questa azione eliminera anche tutti gli alunni associati a quello specifico gruppo!
              </p>
            </div>

          </div>
        </form>

      </div>

    </div>

    <div class="modal-footer">
      <a href="#!" onclick="manageGroupsModal.close();" class="modal-action modal-close waves-effect waves-green btn-flat">Chiudi</a>
    </div>
  </div>
  <!-- Fine modulo per la gestione dei gruppi -->

  <!-- Modulo per il caricamento dei file CSV -->
  <div id="upload-csv-panel" onclick="uploadCSVModal.open();" class="modal modal-fixed-footer uploadcsv-modal">
    <div class="modal-content">
      <h4 class="center-align">Carica CSV Alunni</h4>

      <form class="col s12 uploadcsv-form" action="utils/uploadcsv.php" method="post" enctype="multipart/form-data">
        <div class="row">

          <div class="input-field col s12">
            <select required id="uploadcsv-select" name="uploadcsv-select">
              <?php

                 if($conn){

                   $query = "SELECT * FROM gruppi;";

                   $result = $conn->query($query);

                   if ($result->num_rows > 0) {
                     while($row = $result->fetch_assoc()){
                       if($row["tipo"] == 1){
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
                   echo '<option required value="0" disabled>Impossibile connettersi al database.</option>';
                 }

               ?>
            </select>
            <label>Seleziona Gruppo</label>
          </div>

          <div class="file-field input-field">
            <div class="btn">
              <span>Apri</span>
              <input type="file" name="csv" id="csv" value="">
            </div>
            <div class="file-path-wrapper">
              <input required placeholder="Seleziona un file CSV" class="file-path validate" type="text">
            </div>
          </div>

          <div class="input-field col s12 center-align">
            <button class="btn waves-effect waves-light" type="submit" name="action">
              Carica CSV Alunni
            </button>
          </div>

        </div>
      </form>
    </div>

    <div class="modal-footer">
      <a href="#!" onclick="uploadCSVModal.close();" class="modal-action modal-close waves-effect waves-green btn-flat">Chiudi</a>
    </div>

  </div>
  <!-- Fine modulo per il caricamento dei file CSV -->

  <!-- Modulo per la configurazione dei Parametri -->
  <div id="configcc-panel" onclick="configCCModal.open();" class="modal modal-fixed-footer configcc-modal">
    <div class="modal-content">
      <h4 class="center-align">Configura Parametri CC</h4>

      <div class="col s12 configcc-form">

        <div class="col s12 loadcc-form">
          <!-- Select + button load TODO -->
        </div>

        <div class="col s12 configcc-form">

          <div class="row">
            <div class="input-field col s10 offset-s1">
              <i class="material-icons prefix">settings</i>
              <input required placeholder="Inserisci nome configurazione" id="configname" name="configname" type="text" class="validate">
              <label for="configname">Nome Configurazione</label>
            </div>
          </div>

          <div class="row">
            <div class="col s10 offset-s1">
              <p>Numero Alunni per Classe</p>
              <div id="slider"></div>
            </div>
          </div>

          <div class="row">
            <div class="input-field col s5 offset-s1">
              <input required placeholder="Inserisci numero bilanciato di maschi" id="num-males" name="num-males" type="number" class="validate">
              <label for="num-males">Numero Maschi</label>
            </div>
            <div class="input-field col s5">
              <input required placeholder="Inserisci numero bilanciato di femmine" id="num-females" name="num-females" type="number" class="validate">
              <label for="num-females">Numero Femmine</label>
            </div>
          </div>

          <div class="row">
            <div class="input-field col s5 offset-s1">
              <input required placeholder="Inscerisci numero massimo di CAP per gruppo" id="num-cap" name="num-cap" type="number" class="validate">
              <label for="num-cap">Numero CAP per Gruppo</label>
            </div>
            <div class="input-field col s5">
              <input required placeholder="Inserisci numero massimo di alunni 170 per classe" id="num-170" name="num-170" type="number"
                class="validate">
              <label for="num-170">Numero Alunni 170</label>
            </div>
          </div>

          <div class="row">
            <div class="input-field col s5 offset-s1">
              <input required placeholder="Inserisci numero massimo nazionalita'" id="num-naz" name="num-naz" type="number" class="validate">
              <label for="num-naz">Numero Massimo Nazionalita'</label>
            </div>
            <div class="input-field col s5">
              <input required placeholder="Inserisci numero massimo di alunni per nazionalita'" id="num-x-naz" name="num-x-naz" type="number"
                class="validate">
              <label for="description">Numero Massimo Alunni per Nazionalita'</label>
            </div>
          </div>

          <div class="input-field col s12 center-align">
            <button class="btn waves-effect waves-light" type="submit" name="action" onclick="loadAndSendConfigCCData();">
              Carica Configurazione
            </button>
          </div>
        </div>
      </div>
    </div>
    <div class="modal-footer">
      <a href="#!" onclick="configCCModal.close();" class="modal-action modal-close waves-effect waves-green btn-flat">Chiudi</a>
    </div>

  </div>
  <!-- Fine modulo per la configurazione dei Parametri -->

  <!-- Modulo per la Generazione CC -->
  <div id="gencc-panel" onclick="genCCModal.open();" class="modal modal-fixed-footer gencc-modal">
    <div class="modal-content">
      <h4 class="center-align">Genera CC</h4>
      <!-- da modificare il form -->
      <form class="col s12 configcc-form" action="./utils/gencc.php" method="post">
        <div class="row">
          <div class="input-field col s12">
            <i class="material-icons prefix">settings</i>
            <select required id="genconfigcc-select" name="genconfigcc-select">
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
            </select>
            <label>Seleziona Configurazione</label>
          </div>

          <div class="input-field col s12">
            <i class="material-icons prefix">group</i>
            <select id="genGroup-select" name="genGroup-select">
              <?php

               if($conn){

                 $query = "SELECT * FROM gruppi;";

                 $result = $conn->query($query);

                 if ($result->num_rows > 0) {
                   while($row = $result->fetch_assoc()){
                     if($row["tipo"] == 1){
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
            </select>
            <label>Seleziona Gruppo</label>
          </div>

          <div class="input-field col s12 center-align">
            <button class="btn waves-effect waves-light" type="submit" name="action">
              Genera
            </button>
          </div>

        </div>
      </form>
    </div>
    <div class="modal-footer">
      <a href="#!" onclick="genCCModal.close();" class="modal-action modal-close waves-effect waves-green btn-flat">Chiudi</a>
    </div>

  </div>
  <!-- Fine modulo per la Generazione CC -->


  <h3 class="center-align">Benvenuto,
    <?php echo $_SESSION["username"]; ?>!</h3>

  <!-- Contenitore con le informazioni per l'utilizzo -->
  <div class="container">
    <div class="row">
      <div class="col s12 m6 offset-m3 center-align feature-block">
        <i class="large material-icons">person_add</i>
        <h5>Aggiungi Nuovo Account</h5>
        <br>
        <em> Modulo che permette di creare un nuovo account, inserendo un nome utente, una password e la tipologia desiderata 
        </em>
      </div>
      <div class="col s12 m6 offset-m3 center-align feature-block">
        <i class="large material-icons">group</i>
        <h5>Gestisci Gruppi</h5>
        <br>
        <em> Modulo che permette di visualizzare i gruppi, di crearne, inserendo un nome, una descrizione, se desiderata, e la tipologia, ed infine l'eliminazione, selezionando l'apposito gruppo
        </em>
      </div>
      <div class="col s12 m6 offset-m3 center-align feature-block">
        <i class="large material-icons">cloud_upload</i>
        <h5>Carica CSV Alunni</h5>
        <br>
        <em> Modulo che permette di caricare un file in formato .csv contenente i dati relativi agli alunni in un determinato gruppo, selezionabile nell'apposito box
        </em>
      </div>
      <div class="col s12 m6 offset-m3 center-align feature-block">
        <i class="large material-icons">settings</i>
        <h5>Configura Parametri CC</h5>
        <br>
        <em> Modulo che permette di creare una configurazione, inserendo dei parametri (numero alunni per classe, numero maschi, femmine, numero cap per gruppo, numero alunni con legge 170, numero massimo di nazionalità e numero massimo di alunni con la stessa nazionalità)
        </em> 
      </div>
      <div class="col s12 m6 offset-m3 center-align feature-block">
        <i class="large material-icons">control_point</i>
        <h5>Genera CC</h5>
        <br>
        <em> Modulo che permette di generare l'algoritmo di composizione classi, selezionando la configurazione ed il gruppo desiderati
        </em>
      </div>
      <div class="col s12 m6 offset-m3 center-align feature-block">
        <i class="large material-icons">visibility</i>
        <h5>Visualizza CC</h5>
        <br>
        <em> Modulo che permette di visualizzare e modificare le classi generate automaticamente in precedenza
        </em>
      </div>
      <div class="col s12 m6 offset-m3 center-align feature-block">
        <i class="large material-icons">file_download</i>
        <h5>Scarica CC</h5>
        <br>
        <em> Modulo che permette di scaricare un file in formato .x contenente le classi composte 
        </em>
      </div>
    </div>
  </div>
  <!-- Fine contenitore con le informazioni per l'utilizzo -->

  <script src="js/generatemodals.js"></script>
  <script src="js/formcontroller.js"></script>

  <?php
     if(isset($_GET["newusercreated"])){
       echo "<script>M.toast({html: '" . "Account con nome utente `" . $_GET["newusercreated"] . "` creato!" . "', classes : 'rounded'})</script>";
     }
     if(isset($_GET["qerr"])){
       echo "<script>M.toast({html: 'Query non funzionante. Contattare l`amministratore.', classes : 'rounded'})</script>";
     }
     if(isset($_GET["uap"])){
       echo "<script>M.toast({html: 'Username non disponibile!', classes : 'rounded'})</script>";
     }
     if(isset($_GET["gr"])){
       echo "<script>M.toast({html: 'Gruppo rimosso con successo!', classes : 'rounded'})</script>";
     }
     if(isset($_GET["nodbc"])){
       echo "<script>M.toast({html: 'Database non disponibile!', classes : 'rounded'})</script>";
     }
     if(isset($_GET["opengg"])){
       echo "<script>
               manageGroupsModal.open();
             </script>";
     }
     if(isset($_GET["openccsv"])){
       echo "<script>
               manageGroupsModal.open();
             </script>";
     }
     if(isset($_GET["openccsv"]) && isset($_GET["r"]) && isset($_GET["w"])){
       echo "<script>
               uploadCSVModal.open();
               M.toast({html: 'Status caricamento: " . $_GET["r"] . " inserimenti corretti, " . $_GET["w"] . " inserimenti con errori!', classes : 'rounded'});
             </script>";
     }
     if(isset($_GET["openccc"])){
       echo "<script>
               configCCModal.open();
             </script>";
     }
     if(isset($_GET["gencc"])){
       echo "<script>
               genCCModal.open();
             </script>";
     }
     if(isset($_GET["gap"])){
       echo "<script>
               M.toast({html: 'Gruppo con lo stesso nome giá esistente!', classes : 'rounded'});
             </script>";
     }
     if(isset($_GET["newgroupcreated"])){
       echo "<script>
               M.toast({html: 'Gruppo con nome `" . $_GET["newgroupcreated"] . "` creato!', classes : 'rounded'});
             </script>";
     }
   ?>

</body>

</html>