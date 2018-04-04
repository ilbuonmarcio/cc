<?php session_start(); ?>
<?php include('utils.php'); ?>
<?php redirectIfNotLogon(); ?>

<!DOCTYPE html>

<html>

  <head>
    <title>Home - CC</title>

    <?php addMaterialize(); ?>
    <?php addBaseCSS(); ?>

  </head>

  <body>

    <?php addSidenav(); ?>

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

    <!-- Modulo per la creazione degli account -->
    <div id="create-user-panel" onclick="createUserModal.open();" class="modal modal-fixed-footer createuser-modal">
      <div class="modal-content">
        <h4 class="center-align">Aggiungi Nuovo Account</h4>

        <form class="col s12 createuser-form" action="./scripts/createuser.php" method="post">
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
              <select id="priviledges" name="priviledges">
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

    <?php addFunctionalScripts(); ?>

    <?php
      if(isset($_GET["newusercreated"])){
        echo "<script>M.toast({html: '" . "Account con nome utente `" . $_GET["newusercreated"] . "` creato!" . "'})</script>";
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

  </body>
</html>
