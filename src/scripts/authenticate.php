<?

  include("dbconnection.php");

  $username = $_GET["username"];
  $password = $_GET["password"];

  $conn = connectdb();

  if($conn){
    $query = "SELECT * FROM users WHERE username = '" . $username . "' AND password = '" . $password . "';";
    echo $query;
    $result = $conn->query($query);

    if ($result->num_rows > 0) {
      header("Location: ../index.php");
    } else {
        header("Location: ../login.php");
    }
    $conn->close();
  } else{
    header("Location: ../login.php");
  }
?>
