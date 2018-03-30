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

    <?php addHeader("Home"); ?>
    <?php addSidenav(); ?>

    <h5 class="center-align">Home Page</h5>

  </body>
</html>
