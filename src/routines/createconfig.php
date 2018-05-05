<?php

  include("../utils/db.php");

  $configname = $_POST["configname"];
  $rangeslider_down = $_POST["rangeslider_down"];
  $rangeslider_up = $_POST["rangeslider_up"];
  $nummales = $_POST["nummales"];
  $numfemales = $_POST["numfemales"];
  $numcap = $_POST["numcap"];
  $num170 = $_POST["num170"];
  $numnaz = $_POST["numnaz"];
  $nummaxforeachnaz = $_POST["nummaxforeachnaz"];

  if($nummales == ""){
    $nummales = "NULL";
  }
  if($numfemales == ""){
    $numfemales = "NULL";
  }

  $conn = connectDB();

  if($conn){

    $sql = "SELECT * FROM configurazioni WHERE nome = '" . $configname . "';";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {

      $sqlupdate = "UPDATE configurazioni
      SET
          min_alunni = " . $rangeslider_down . ",
          max_alunni = " . $rangeslider_up . ",
          numero_femmine = " . $numfemales . ",
          numero_maschi = " . $nummales . ",
          max_per_cap = " . $numcap . ",
          max_per_naz = " . $nummaxforeachnaz . ",
          max_naz = " . $numnaz . ",
          num_170 = " . $num170 . "
      WHERE nome = '" . $configname . "';";

      if($conn->query($sqlupdate)){
        echo "{
          status: 'Update Query Executed',
          querystatus : 'good'
        }";
      } else {
        echo '{
          status: "Update Query Executed",
          querystatus : "bad",
          executedquery : "' . $sqlupdate . '"
        }';
      }

    } else {

      $sqlinsert = "INSERT INTO configurazioni VALUES (
        NULL,
        '" . $configname . "',
        " . $rangeslider_down . ",
        " . $rangeslider_up . ",
        " . $numfemales . ",
        " . $nummales . ",
        " . $numcap . ",
        " . $nummaxforeachnaz . ",
        " . $numnaz . ",
        " . $num170 . "
      );";

      if($conn->query($sqlinsert)){
        echo "{
          status: 'Insert Query Executed',
          querystatus : 'good'
        }";
      } else {
        echo '{
          status: "Insert Query Executed",
          querystatus : "bad",
          executedquery : "' . $sqlinsert . '"
        }';
      }

    }
  } else {
    echo "{
      status: 'No Database Connection',
      querystatus: 'bad'
    }";
  }
?>
