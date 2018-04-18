<?php session_start(); ?>
<?php include('utils/utils.php'); ?>
<?php redirectIfNotLogon(); ?>

<!DOCTYPE html>

<html>

<head>
	<title>Home - CC</title>

	<!-- MaterializeIcons -->
	<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">

	<!-- Compiled and minified CSS -->
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-beta/css/materialize.min.css">

	<!-- Compiled and minified JavaScript -->
	<script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-beta/js/materialize.min.js"></script>


	<!--Let browser know website is optimized for mobile-->
	<meta name="viewport" content="width=device-width, initial-scale=1.0" />

	<style>
		#group-label {
			bottom: 20px;
			right: 20px;
			position: fixed;
			background-color: #CCCCCC;
			opacity: 0.6;
		}

		#group-label>#label {
			color: white;
			font-size: 2em;
			padding: 0px 20px;
		}
	</style>

</head>

<body>

	<?php

	  if(isset($_GET["groupid"])){

		  $groupid = $_GET["groupid"];

		  include("utils/db.php");

		  $conn = connectdb();

		  if($conn){

				$query = "SELECT * FROM alunni WHERE id_gruppo = " . $groupid . ";";

				$result = $conn->query($query);

				if ($result->num_rows > 0) {
				  echo '<table class="striped centered box-shadow">
      						<thead>
      						  <tr>
      							  <th>Cognome</th>
      							  <th>Nome</th>
      							  <th>Matricola</th>
      							  <th>Codice Fiscale</th>
      							  <th>Desiderata</th>
      							  <th>Sesso</th>
      							  <th>Data di nascita</th>
      							  <th>Cap</th>
      							  <th>Nazionalita</th>
      							  <th>Legge 170</th>
      							  <th>Legge 104</th>
      							  <th>Classe precedente</th>
      							  <th>Classe sucessiva</th>
      							  <th>Scelta indirizzo</th>
      							  <th>Codice catastale</th>
      							  <th>Voto</th>
      							  <th>Id gruppo</th>
      						  </tr>
      						</thead>
      					<tbody>';

			  while($row = $result->fetch_assoc()) {
					echo '<tr>
							<td>' . $row["cognome"]           . '</td>
							<td>' . $row["nome"]              . '</td>
							<td>' . $row["matricola"]         . '</td>
							<td>' . $row["cf"]                . '</td>
							<td>' . $row["desiderata"]        . '</td>
							<td>' . $row["sesso"]             . '</td>
							<td>' . $row["data_nascita"]      . '</td>
							<td>' . $row["cap"]               . '</td>
							<td>' . $row["nazionalita"]       . '</td>
							<td>' . $row["legge_170"]         . '</td>
							<td>' . $row["legge_104"]         . '</td>
							<td>' . $row["classe_precedente"] . '</td>
							<td>' . $row["classe_successiva"] . '</td>
							<td>' . $row["scelta_indirizzo"]  . '</td>
							<td>' . $row["cod_cat"]           . '</td>
							<td>' . $row["voto"]              . '</td>
							<td>' . $row["id_gruppo"]         . '</td>
						  </tr>';
				  }
  			  echo '</tbody>
  				    </table>


					 <div id="group-label">
						<p id="label">' . $_GET["groupname"] . '</p>
					 </div>';

				} else {
					echo '<h2 style="color: red;" class="center-align">Tabella vuota!</h2>';
				}
		  } else{
		    echo '<h2 style="color: red;" class="center-align">Tabella non disponibile! Errore di connessione al database.</h2>';
		  }
	  }

  ?>

</body>

</html>
