<?php session_start(); ?>
<?php include('utils/utils.php'); ?>
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

    <?php addFunctionalScripts(); ?>

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

  </body>
</html>
