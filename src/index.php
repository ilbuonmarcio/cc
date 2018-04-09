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

  <ul id="slide-out" class="sidenav" style="background-color: #eeeeee;">
    <li>
      <p class="sidenav-menu-title center-align">Menu - CC</p>
    </li>
    <li>
      <a onclick="" class="waves-effect">
        <i class="material-icons">person_add</i>Aggiungi Nuovo Account</a>
    </li>
    <li>
      <div class="divider"></div>
    </li>
    <li>
      <a onclick="" class="waves-effect">
        <i class="material-icons">group</i>Gestisci Gruppi</a>
    </li>
    <li>
      <a onclick="" class="waves-effect">
        <i class="material-icons">cloud_upload</i>Carica CSV Alunni</a>
    </li>
    <li>
      <a onclick="" class="waves-effect">
        <i class="material-icons">settings</i>Configura Parametri CC</a>
    </li>
    <li>
      <a onclick="" class="waves-effect">
        <i class="material-icons">control_point</i>Genera CC</a>
    </li>
    <li>
      <div class="divider"></div>
    </li>
    <li>
      <a class="waves-effect">
        <i class="material-icons">visibility</i>Visualizza CC</a>
    </li>
    <li>
      <a onclick="" class="waves-effect">
        <i class="material-icons">file_download</i>Scarica CC</a>
    </li>
    <li>
      <a href="login.php" class="waves-effect">
        <i class="material-icons">exit_to_app</i>Esci</a>
    </li>
  </ul>
  <a id="sidenav-trigger-button" data-target="slide-out" class="sidenav-trigger show-on-large btn btn-floating btn-large green">
    <i class="material-icons">menu</i>
  </a>

  <?php
    include("items/sidenav.php");
  ?>

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

</body>

</html>
