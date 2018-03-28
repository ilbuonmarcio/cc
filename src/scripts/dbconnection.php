 <?php

  include('../config/dbconfig.php');

	function dbconnection() {
		$conn = new mysqli(HOST, DB_USER, DB_PASSWORD, DB_NAME);

		if ($conn->connect_error) {
			die("Errore di connessione al database");
		}
		echo "Connected successfully";

		return $conn;
	}
?>
