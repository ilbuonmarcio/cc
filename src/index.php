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

    <h3 class="center-align">Home Page</h3>

  </body>
</html>
