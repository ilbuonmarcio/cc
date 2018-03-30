<?php

function addBaseCSS(){
  echo '
    <link href="css/base.css" type="text/css" rel="stylesheet"/>
';
}

function resetAuth(){
  $_SESSION["authenticated"] = 0;
}

function redirectIfNotLogon(){
  if(!isset($_SESSION["authenticated"]) || $_SESSION["authenticated"] == 0){
    header("Location: login.php?noauth=1");
  }
  return;
}

function loginMessage($msg){
  echo '<div class="row">' .
       '<div class="col s6 offset-s3 red" style="margin-top: 60px; border-radius: 30px; opacity: 0.9; color: white;">' .
       '<p class="center-align" style="font-size: 1.2em">' . $msg . '</p></div></div>';
}

function addMaterialize(){
  echo '<!-- MaterializeIcons -->
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">

    <!-- Compiled and minified CSS -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-beta/css/materialize.min.css">

    <!-- Compiled and minified JavaScript -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-beta/js/materialize.min.js"></script>


    <!--Let browser know website is optimized for mobile-->
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>';
}

function addFooter(){
  echo '<div class="section footer">
            <div class="row">
              <div class="col s12 m4 center-align">
                <h5>Development Team</h5>
                <ul>
                  <li>Alessandro Marchioro - 5CI 17/18</li>

                  <li>Daniele Fava - 5CI 17/18</li>

                  <li>Damiano Visentini - 5CI 17/18</li>

                  <li>Mattia Carra - 5CI 17/18</li>

                  <li>Leonardo Bonomi - 5CI 17/18</li>
                </ul>
              </div>
              <div class="col s12 m4 center-align">
                <h5>ITI Marconi, Verona</h5>
                P.le R. Guardini 1<br>
                Verona, IT 37138<br>
                Tel: +39 045 8101428<br>
                Fax: +39 045 573497<br>
                Mail: vrtf03000v@pec.istruzione.it<br>
                Site: marconiverona.gov.it<br>
              </div>
              <div class="col s12 m4 center-align">
                <h5>Altri Progetti</h5>
                <a href="https://campus.marconivr.it">Campus</a><br>
                <a href="">EDUS</a><br>
                <a href="">FantaMarconi</a><br>
                <a href="">OpenData</a><br>
                <a href="https://www.marconiverona.gov.it/portal/">Portale</a><br>
                <a href="http://apps.marconivr.it/poldo/">Poldo</a><br>
                <a href="http://www.anobii.com/marconivr/books">Biblioteca 2.0</a><br>
              </div>
            </div>
          </div>
';
}

function addSidenav(){
    echo '

    <ul id="slide-out" class="sidenav " style="background-color: #eeeeee;">
      <li>
        <p class="sidenav-menu-title center-align">Menu - CC</p>
      </li>
      <li>
        <a href="#!" class="waves-effect"><i class="material-icons">person_add</i>Aggiungi Nuovo Account</a>
      </li>
      <li>
        <div class="divider"></div>
      </li>
      <li>
        <a href="#!" class="waves-effect"><i class="material-icons">cloud_upload</i>Carica CSV Alunni</a>
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
    <script src="scripts/sidenav.js"></script>';
}


?>
