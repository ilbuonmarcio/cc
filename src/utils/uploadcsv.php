<?php
  // Check if the form was submitted
  if($_SERVER["REQUEST_METHOD"] == "POST"){
      // Check if file was uploaded without errors
      if(isset($_FILES["csv-to-upload"]) && $_FILES["csv-to-upload"]["error"] == 0){
          $allowed = array("csv" => "text/csv", "jpeg" => "image/jpeg");
          $filename = $_FILES["csv-to-upload"]["name"];
          $filetype = $_FILES["csv-to-upload"]["type"];
          $filesize = $_FILES["csv-to-upload"]["size"];

          // Verify file extension
          $ext = pathinfo($filename, PATHINFO_EXTENSION);
          if(!array_key_exists($ext, $allowed)) die("Error: Please select a valid file format.");

          // Verify file size - 5MB maximum
          $maxsize = 5 * 1024 * 1024;
          if($filesize > $maxsize) die("Error: File size is larger than the allowed limit.");

          // Verify MYME type of the file
          if(in_array($filetype, $allowed)){
              // Check whether file exists before uploading it
              if(file_exists("upload/" . $_FILES["csv-to-upload"]["name"])){
                  echo $_FILES["csv-to-upload"]["name"] . " is already exists.";
              } else{
                  move_uploaded_file($_FILES["csv-to-upload"]["tmp_name"], "../upload/" . $_FILES["csv-to-upload"]["name"]);
                  echo "Your file was uploaded successfully.";
                  echo '<img src="../uploads/' . $_FILES["csv-to-upload"]["name"] . '" border=0>';
              }
          } else{
              echo "Error: There was a problem uploading your file. Please try again.";
          }
      } else{
          echo "Error: " . $_FILES["csv-to-upload"]["error"];
      }
  }
?>
