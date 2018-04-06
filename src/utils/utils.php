<?php

function resetAuth(){
  $_SESSION["authenticated"] = 0;
}

function redirectIfNotLogon(){
  if(!isset($_SESSION["authenticated"]) || $_SESSION["authenticated"] == 0){
    header("Location: login.php?noauth=1");
  }
  return;
}

?>
