 <?php

  // Definisco le costanti per la connessione al database

  define("HOST", "localhost");
  define("DB_USER", "root");
  define("DB_PASSWORD", "30760");
  define("DB_NAME", "composizioneclassi");

  /*
    Funzione che ritorna un istanza di connessione al database, se disponibile
  */
	function connectdb() {
		$conn = new mysqli(HOST, DB_USER, DB_PASSWORD, DB_NAME);

		if ($conn->connect_error) {
			header("Location: ../index.php?nodbc=1");
		}
		return $conn;
	}
?>
