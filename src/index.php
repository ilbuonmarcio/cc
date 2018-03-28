<?php include('utils.php'); ?>
<?php
  if(!isset($_SESSION["authenticated"])){
    header("Location: login.php");
  }
?>

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

    <?php addFooter(); ?>

  </body>
</html>
