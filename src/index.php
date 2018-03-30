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

  </body>
</html>
