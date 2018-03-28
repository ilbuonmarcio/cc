<?

  include("dbconnection.php");

  $username = $_POST["username"];
  $password = $_POST["password"];

  $conn = connectdb();

  $query = "SELECT * FROM users WHERE username = '" . $username . "' AND password = '" . $password . "';";

  $result = $conn->query($query);

  if ($result->num_rows > 0) {
    $_SESSION["authenticated"] = True;
    header("Location: ../index.php");
  } else {
      header("Location: ../login.php?c=0");
  }
  $conn->close();
?>
