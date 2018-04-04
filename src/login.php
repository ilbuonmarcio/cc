<?php session_start(); ?>
<?php include('utils/utils.php'); ?>
<?php resetAuth(); ?>

<!DOCTYPE html>

<html>

  <head>
    <title>Login - CC</title>

    <?php addMaterialize(); ?>
    <?php addBaseCSS(); ?>

  </head>

  <body>

    <div class="row">
      <div class="col s12">
        <h1 class="login-title center-align">CC - <a href="https://github.com/marconivr/marconicc">marconicc</a>, but <i>stronger</i></h1>
      </div>
    </div>

    <div class="container">

      <?php
        if(isset($_GET["noauth"])){
          loginMessage("Sessione scaduta!");
        }
        if(isset($_GET["unf"])){
          loginMessage("Utente non trovato!");
        }
        if(isset($_GET["nodbc"])){
          loginMessage("Nessuna connessione disponibile al database!");
        }
      ?>

      <div class="row">
        <form class="col s12 login-form" action="./utils/auth.php" method="post">
          <h4 class="center-align">Login</h4>
          <div class="row">
            <div class="input-field col s12 m6 offset-m3">
              <i class="material-icons prefix">account_circle</i>
              <input placeholder="Inserisci nome utente" id="username" name="username" type="text" class="validate">
              <label for="username">Nome Utente</label>
            </div>
            <div class="input-field col s12 m6 offset-m3">
                <i class="material-icons prefix">security</i>
              <input placeholder="Inserisci password" id="password" name="password" type="password" class="validate">
              <label for="password">Password</label>
            </div>
            <div class="input-field col s12 m6 offset-m3 center-align">
              <button class="btn waves-effect waves-light" type="submit" name="action">
                Log in
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>

    <?php addFooter(); ?>

  </body>
</html>
