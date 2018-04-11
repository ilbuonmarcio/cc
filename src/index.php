<?php session_start();
      include("utils/db.php");
?>
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

  <!-- Compiled and minified jQuery -->
  <script src="https://code.jquery.com/jquery-3.3.1.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>

  <!--Let browser know website is optimized for mobile-->
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <link href="css/index.css" type="text/css" rel="stylesheet" />

</head>

<body>

  <ul id="slide-out" class="sidenav" style="background-color: #eeeeee;">
    <li>
      <p class="sidenav-menu-title center-align">Menu - CC</p>
    </li>
    <li>
      <a onclick="createuserpanel.openPanel();" class="waves-effect">
        <i class="material-icons">person_add</i>Aggiungi Nuovo Account</a>
    </li>
    <li>
      <div class="divider"></div>
    </li>
    <li>
      <a onclick="managegroupspanel.openPanel();" class="waves-effect">
        <i class="material-icons">group</i>Gestisci Gruppi</a>
    </li>
    <li>
      <a onclick="uploadcsvpanel.openPanel();" class="waves-effect">
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





  <!-- Pannello per la creazione di un utente -->
  <div id="createuser-panel" class="modal modal-fixed-footer">

    <div class="modal-content">

      <h4 class="center-align">Aggiungi Nuovo Account</h4>

      <h6 class="panel-subtitle center-align">Lista Utenti</h6>
      <div id="createuser-table" class="col s12 center-align">

      </div>

      <h6 class="panel-subtitle center-align">Crea Nuovo Utente</h6>

      <div id="createuser-form">

        <div class="row">
          <div class="input-field col s12">
            <input placeholder="Inserisci username" id="createuser-username" name="createuser-username" type="text" class="validate">
            <label for="createuser-username">Nome Utente</label>
          </div>

          <div class="input-field col s12">
            <input placeholder="Inserisci password" id="createuser-password" name="createuser-password" type="text" class="validate">
            <label for="createuser-password">Password</label>
          </div>

          <div class="input-field col s12">
            <select id="createuser-priviledges" name="createuser-priviledges">
              <option value="0">Amministratore</option>
              <option value="1" selected>Editor</option>
              <option value="2">Visualizzatore</option>
            </select>
            <label>Seleziona Permessi</label>
          </div>

          <div class="col s12 center-align">
            <a class="waves-effect waves-light btn" onclick="createuserpanel.submit();">Invia</a>
          </div>
        </div>

      </div>
    </div>

    <div class="modal-footer">
      <a class="modal-action modal-close waves-effect waves-green btn-flat">Chiudi</a>
    </div>

  </div>
  <!-- fine creazione di un utente -->


  <!-- Pannello per la gestione dei gruppi -->
  <div id="managegroups-panel" class="modal modal-fixed-footer">

    <div class="modal-content">

      <h4 class="center-align">Gestisci Gruppi</h4>


      <h6 class="panel-subtitle center-align">Lista Gruppi</h6>
      <div id="managegroups-table" class="col s12 center-align">

      </div>

      <div class="divider"></div>

      <div id="managegroupscreate-form">

        <h6 class="center-align panel-subtitle">Crea Nuovo Gruppo</h6>

        <div class="row">

          <div class="input-field col s12">
            <input placeholder="Inserisci Nome del gruppo" id="managegroupscreate-groupname" name="managegroupscreate-groupname" type="text" class="validate">
            <label for="managegroupscreate-groupname">Nome gruppo</label>
          </div>

          <div class="input-field col s12">
            <input placeholder="Inserisci Descrizione del gruppo" id="managegroupscreate-groupdesc" name="managegroupscreate-groupdesc" type="text" class="validate">
            <label for="managegroupscreate-groupdesc">Descrizione gruppo</label>
          </div>

          <div class="input-field col s12">
            <select id="managegroupscreate-grouptype" name="managegroupscreate-grouptype">
              <option value="1" selected>Classi Prime</option>
              <option value="3">Classi Terze</option>
            </select>
            <label>Seleziona Tipo</label>
          </div>

          <div class="col s12 center-align">
            <a class="waves-effect waves-light btn" onclick="managegroupspanel.submitCreate();">
              Crea Gruppo
            </a>
          </div>

        </div>
      </div>


      <div class="divider"></div>

        <div id="managegroupsdelete-form">

          <h6 class="center-align panel-subtitle">Elimina Gruppo</h6>

          <div class="row">

            <div class="input-field col s9">
              <select id="managegroupsdelete-groupname" name="managegroupsdelete-groupname">

              </select>
              <label>Seleziona Gruppo</label>
            </div>

            <div class="input-field col s3 center-align">
              <button onclick="managegroupspanel.submitDelete();" class="btn waves-effect waves-light">
                Cancella Gruppo
              </button>
            </div>

            <div class="col s12 center-align">
              <p id="managegroupsdelete-warning" style="color: red;">
                Attenzione! Questa azione eliminera anche tutti gli alunni associati a quello specifico gruppo!
              </p>
            </div>

          </div>
        </div>

    </div>

    <div class="modal-footer">
      <a class="modal-action modal-close waves-effect waves-green btn-flat">Chiudi</a>
    </div>

  </div>




  <div id="uploadcsv-panel" class="modal modal-fixed-footer">

    <div class="modal-content">

      <h4 class="center-align">Carica CSV Alunni</h4>

      <div class="col s12" id="uploadcsv-form">
         <div class="row">

           <div class="input-field col s12">
             <select id="uploadcsv-groupname" name="uploadcsv-groupname">

             </select>
             <label>Seleziona Gruppo</label>
           </div>

           <div class="file-field input-field">
             <div class="btn">
               <span>Apri</span>
               <input type="file" name="uploadcsv-filepath" id="uploadcsv-filepath" value="">
             </div>
             <div class="file-path-wrapper">
               <input placeholder="Seleziona un file CSV" class="file-path validate" type="text">
             </div>
           </div>

           <div class="input-field col s12 center-align">
             <button class="btn waves-effect waves-light" onclick="uploadcsvpanel.submit();">
               Carica CSV
             </button>
           </div>

         </div>
       </div>

    </div>

    <div class="modal-footer">
      <a class="modal-action modal-close waves-effect waves-green btn-flat">Chiudi</a>
    </div>

  </div>

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

  <script src="js/Exceptions.js"></script>
  <script src="js/SideNavController.js"></script>
  <script src="js/Panel.js"></script>
  <script src="js/CreateUserPanel.js"></script>
  <script src="js/ManageGroupsPanel.js"></script>
  <script src="js/UploadCSVPanel.js"></script>

  <script src="js/PanelController.js"></script>

</body>

</html>
