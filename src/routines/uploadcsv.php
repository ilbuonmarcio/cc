<?php

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

  include("../utils/db.php");

  $uploadcsv_select = $_POST["groupname"];

  $tmpName = $_FILES["filepath"]["tmp_name"];
  $csvAsArray = array_map('str_getcsv', file($tmpName));

  $conn = connectdb();

  if($conn){

    $right = 0;
    $wrong = 0;

    // Cognome, Nome,      Matricola, CF,               Desiderata,       Sesso, DataNascita, Cap,   Naz,     107, 104, prec, scelta_indirizzo, cod_cat, voto
    // Scalco,  Valentina, 20001,     ADCBBA27A092EE79, 40A83FA3984A8664, f,     2/2/2001,    70024, Tedesca, s,   n,   NULL, 3,                691B,    1

    $stringarraypositions = array(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 14);

    foreach($csvAsArray as $row){

      $query = "INSERT INTO alunni VALUES ";
      $query .= "(NULL,";


      for($i = 0; $i < sizeof($row); $i++){
        if($row[$i] == ""){
          $query .= "NULL, ";
          continue;
        }
        if (in_array($i, $stringarraypositions)){
          $query .= "'" . $row[$i] . "', ";
        } else {
          $query .= $row[$i] . ", ";
        }
      }

      $query .= $uploadcsv_select . ");";

      if($conn->query($query) === true){
        $right += 1;
      } else{
        $wrong += 1;
      }
    }

    $conn->query("UPDATE alunni SET sesso = LOWER(sesso)");

    echo "{
      status: 'Query Executed',
      querystatus : 'good',
      right : " . $right . ",
      wrong : " . $wrong . "
    }";

  } else {
    echo "{
      status: 'No Database Connection',
      querystatus: 'bad'
      right : " . $right . ",
      wrong : " . $wrong . "
    }";
  }

?>
