<?php session_start(); ?>
<?php include('utils/utils.php'); ?>
<?php redirectIfNotLogon(); ?>

<!DOCTYPE html>

<html>

  <head>
    <title>Home - CC</title>

    <!-- MaterializeIcons -->
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">

    <!-- Compiled and minified CSS -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-beta/css/materialize.min.css">

    <!-- Compiled and minified JavaScript -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-beta/js/materialize.min.js"></script>


    <!--Let browser know website is optimized for mobile-->
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>

    <link href="css/base.css" type="text/css" rel="stylesheet"/>

  </head>

  <body>

    <ul id="slide-out" class="sidenav " style="background-color: #eeeeee;">
      <li>
        <p class="sidenav-menu-title center-align">Menu - CC</p>
      </li>
      <li>
        <a onclick="createUserModal.open();" href="#!" class="waves-effect"><i class="material-icons">person_add</i>Aggiungi Nuovo Account</a>
      </li>
      <li>
        <div class="divider"></div>
      </li>
      <li>
        <a onclick="uploadCSVModal.open();" href="#!" class="waves-effect"><i class="material-icons">cloud_upload</i>Carica CSV Alunni</a>
      </li>
      <li>
        <a href="#!" class="waves-effect"><i class="material-icons">settings</i>Configura Parametri CC</a>
      </li>
      <li>
        <a href="#!" class="waves-effect"><i class="material-icons">control_point</i>Genera CC</a>
      </li>
      <li>
        <div class="divider"></div>
      </li>
      <li>
        <a href="#!" class="waves-effect"><i class="material-icons">visibility</i>Visualizza CC</a>
      </li>
      <li>
        <a href="#!" class="waves-effect"><i class="material-icons">file_download</i>Scarica CC</a>
      </li>
      <li>
        <a href="login.php" class="waves-effect"><i class="material-icons">exit_to_app</i>Esci</a>
      </li>
    </ul>
    <a href="#" id="sidenav-trigger-button" data-target="slide-out" class="sidenav-trigger show-on-large btn btn-floating btn-large green"><i class="material-icons">menu</i></a>

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

    <!-- Modulo per il caricamento dei file CSV -->
    <div id="upload-csv-panel" onclick="uploadCSVModal.open();" class="modal modal-fixed-footer uploadcsv-modal">
      <div class="modal-content">
        <h4 class="center-align">Carica CSV Alunni</h4>

        <form class="col s12 uploadcsv-form" action="utils/uploadcsv.php" method="post" enctype="multipart/form-data">
          <div class="row">

          <div class="input-field col s12">
            <i class="material-icons prefix">group</i>
            <input pattern=".{3,}" required placeholder="Inserisci Nome Gruppo" id="gruppo" name="gruppo" type="text" class="validate">
            <label for="gruppo">Nome Gruppo (Minimo 3 caratteri)</label>
          </div>

          <div class="col s12 center-align">
            <?php

              include("utils/dbconnection.php");

              $conn = connectdb();

              if($conn){

                $query = "SELECT * FROM gruppi;";

                $result = $conn->query($query);

                if ($result->num_rows > 0) {
                  echo '<p>Nomi dei gruppi gia` utilizzati: </p>';
                  while($row = $result->fetch_assoc()) {
                    echo '<div class="chip">' . $row["nome"] . '</div>';
                  }
                }
              } else{
                echo "Impossibile caricare i gruppi gia' formati.";
              }

            ?>
          </div>

        </div>

        <div class="row">

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

    </div>
    <!-- Fine modulo per il caricamento dei file CSV -->

    <h3 class="center-align">Benvenuto, <?php echo $_SESSION["username"]; ?>!</h3>

    <!-- Contenitore con le informazioni per l'utilizzo -->
    <div class="container">
      <div class="row">
        <div class="col s12 m6 offset-m3 center-align feature-block">
          <i class="large material-icons">person_add</i>
          <h5>Aggiungi Nuovo Account</h5>
        </div>
        <div class="col s12 m6 offset-m3 center-align feature-block">
          <i class="large material-icons">cloud_upload</i>
          <h5>Carica CSV Alunni</h5>
        </div>
        <div class="col s12 m6 offset-m3 center-align feature-block">
          <i class="large material-icons">settings</i>
          <h5>Configura Parametri CC</h5>
        </div>
        <div class="col s12 m6 offset-m3 center-align feature-block">
          <i class="large material-icons">control_point</i>
          <h5>Genera CC</h5>
        </div>
        <div class="col s12 m6 offset-m3 center-align feature-block">
          <i class="large material-icons">visibility</i>
          <h5>Visualizza CC</h5>
        </div>
        <div class="col s12 m6 offset-m3 center-align feature-block">
          <i class="large material-icons">file_download</i>
          <h5>Scarica CC</h5>
        </div>
      </div>
    </div>
    <!-- Fine contenitore con le informazioni per l'utilizzo -->

    <?php
      if(isset($_GET["newusercreated"])){
        echo "<script>M.toast({html: '" . "Account con nome utente `" . $_GET["newusercreated"] . "` creato!" . "', classes : 'rounded'})</script>";
      }
      if(isset($_GET["qerr"])){
        echo "<script>M.toast({html: 'Query non funzionante. Contattare l`amministratore.'})</script>";
      }
      if(isset($_GET["uap"])){
        echo "<script>M.toast({html: 'Username non disponibile!'})</script>";
      }
      if(isset($_GET["nodbc"])){
        echo "<script>M.toast({html: 'Database non disponibile!'})</script>";
      }
    ?>

    <script src="js/scripts.js"></script>

  </body>
</html>
