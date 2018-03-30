<?php session_start(); ?>
<?php include('utils.php'); ?>

<!DOCTYPE html>

<html>

  <head>
    <title>Login - CC</title>

    <?php addMaterialize(); ?>
    <?php addBaseCSS(); ?>

  </head>

  <body>

    <?php addHeader("Login"); ?>

    <div class="container">
      <div class="row">
        <form class="col s12 login-form" action="./scripts/auth.php" method="post">
          <h3 class="center-align">Login</h3>
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
