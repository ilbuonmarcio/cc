<?php session_start(); ?>
<?php include('utils.php'); ?>
<?php include('scripts/messageprompt.php'); ?>
<?php redirectIfNotLogon(); ?>

<!DOCTYPE html>

<html>

  <head>
    <title>Home - CC</title>

    <?php addMaterialize(); ?>
    <?php addBaseCSS(); ?>
	<?php addAlertCSS(); ?>

  </head>

  <body>

    <?php addHeader("Home"); ?>
	

    <h3 class="center-align">Home Page</h3>
	
	<div class="right_bottom_corner" ><?php alert("Login riuscito.") ?></div>
	
	<?php addAlertScript(); ?>

  </body>
</html>
