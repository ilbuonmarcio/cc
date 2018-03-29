<?php
	function alert($msg){
		echo '<div class="alert success">';
		echo '<span class="closebtn">&times;</span>';
		echo '<strong>Success!</strong> '. $msg;
		echo '</div>';
	}
?>