 <?php

  // Carico le costanti per la connessione al database
  include('../config/dbconfig.php');

  /*
    Funzione che ritorna un istanza di connessione al database, se disponibile
  */
	function connectdb() {
		$conn = new mysqli(HOST, DB_USER, DB_PASSWORD, DB_NAME);

		if ($conn->connect_error) {
			die("Errore di connessione al database.");
		}
		return $conn;
	}
?>
