<?php

function addBaseCSS(){
  echo '<link href="css/base.css" type="text/css" rel="stylesheet"/>
';
}

function addMaterialize(){
  echo '<!-- Compiled and minified CSS -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-beta/css/materialize.min.css">

    <!-- Compiled and minified JavaScript -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-beta/js/materialize.min.js"></script>
';
}

function addHeader(){
  echo '<div class="section header">
          <div class="row">
            <div class="col s12 blue">
              <h3 class="center-align">Header</h3>
            </div>
          </div>
        </div>';
}

function addFooter(){
  echo '<div class="section footer">
          <div class="row">
            <div class="col s12 green">
              <h5 class="center-align">footer</h5>
            </div>
          </div>
        </div>';
}

?>
