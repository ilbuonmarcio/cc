<?php
	include("../utils/dbconnection.php");
	
	class EmptyGroupException extends Exception { }
	class NoConfigFoundException extends Exception { }

	Class Alunno{
		
		function __construct($id, $cognome, $nome, $matricola, $cf, $desiderata, $sesso, $data_nascita, $cap, $nazionalita, $legge_170, $legge_104, $classe_precedente, $classe_successiva, $scelta_indirizzo, $cod_cat, $voto, $id_gruppo){
			$this->id = $id;
			$this->cognome = $cognome;
			$this->nome = $nome;
			$this->matricola = $matricola;
			$this->cf = $cf;
			$this->desiderata = $desiderata;
			$this->sesso = $sesso;
			$this->data_nascita = $data_nascita;
			$this->cap = $cap;
			$this->nazionalita = $nazionalita;
			$this->legge_170 = $legge_170;
			$this->legge_104 = $legge_104;
			$this->classe_precedente = $classe_precedente;
			$this->classe_successiva = $classe_successiva;
			$this->scelta_indirizzo = $scelta_indirizzo;
			$this->cod_cat = $cod_cat;
			$this->voto = $voto;
			$this->id_gruppo = $id_gruppo;
		}
	}
	
	Class Alunni{
		
		function __construct($groupid){
			try{
				$this->fillStudentsArrayFromDB($groupid);
			} catch(EmptyGroupException $e){
				echo $e;
			}
		}
		
		function fillStudentsArrayFromDB($groupid){
			$conn = connectdb();
			$query = "SELECT * FROM alunni WHERE id_gruppo = ". $groupid .";";

			$result = $conn->query($query);
			
			$tmparray = array();
			
			if ($result->num_rows > 0) {
				while($row = $result->fetch_assoc()){
					
					array_push($tmparray, new Alunno($row["id"], $row["cognome"], $row["nome"], $row["matricola"], $row["cf"], $row["desiderata"], $row["sesso"], $row["data_nascita"], $row["cap"], $row["nazionalita"],$row["legge_107"], $row["legge_104"], $row["classe_precedente"], $row["classe_successiva"], $row["scelta_indirizzo"], $row["cod_cat"], $row["voto"], $row["id_gruppo"]));
					
				}
				
				$this->students = $tmparray;
				
			}else{
				throw new EmptyGroupException("Empty result set (loadStudents)");
			}
		}
		
		function getStudentsArray(){
			return $this->students;
		}
	}
	
	Class Classe{
	
		function __construct($nome){
			$this->nome = $nome;
		}
	}
	
	Class ClassiComposte{
		/********************************
		*				ROBBE			*
		*********************************/
	}
	
	Class Config{
		
		function __construct($configid){
			try{
				$this->loadConfigFromDB($configid);
			} catch(NoConfigFoundException $e){
				echo $e;
			}
		}
		
		private function loadConfigFromDB($configid){
			$conn = connectdb();
			$query = "SELECT * FROM configurazioni WHERE id = ". $configid .";";

			$result = $conn->query($query);
			
			if ($result->num_rows == 1) {
				while($row = $result->fetch_assoc()){
					$this->id = $row["id"];
					$this->nome = $row["nome"];
					$this->min_alunni = $row["min_alunni"];
					$this->max_alunni = $row["max_alunni"];
					$this->numero_femmine = $row["numero_femmine"];
					$this->numero_maschi = $row["numero_maschi"];
					$this->max_per_cap = $row["max_per_cap"];
					$this->max_per_naz = $row["max_per_naz"];
					$this->max_naz = $row["max_naz"];
					$this->num_170 = $row["num_170"];
				}
			}else{
				throw new NoConfigFoundException("Empty result set (loadConfigCC)");
			}
		}
		
	}
	
	Class CC{
		
		function __construct($students, $config){
			$this->students = $students;
			$this->config = $config;
		}
	}
	
	$students = new Alunni(1);	
	$config = new Config(1);
	$cc = new CC($students, $config);	
	
?>