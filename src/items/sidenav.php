<div id="createuser-panel" class="modal modal-fixed-footer">

  <div class="modal-content">
    <div id="createuser-form">

      <h4 class="center-align">Aggiungi Nuovo Account</h4>

      <div class="row">
        <div class="input-field col s12">
          <input placeholder="Inserisci username" id="createuser-username" type="text" class="validate">
          <label for="createuser-username">Nome Utente</label>
        </div>

        <div class="input-field col s12">
          <input placeholder="Inserisci password" id="createuser-password" type="text" class="validate">
          <label for="createuser-password">Password</label>
        </div>

        <div class="input-field col s12">
          <select id="createuser-priviledges" name="createuser-priviledges">
            <option value="0">Amministratore</option>
            <option value="1" selected>Editor</option>
            <option value="2">Visualizzatore</option>
          </select>
          <label>Seleziona Permessi</label>
        </div>

        <div class="col s12 center-align">
          <a class="waves-effect waves-light btn" onclick="createuserpanel.submit();">Invia</a>
        </div>
      </div>

    </div>
  </div>

  <div class="modal-footer">
    <a class="modal-action modal-close waves-effect waves-green btn-flat">Chiudi</a>
  </div>

</div>

<script src="js/SidenavController.js"></script>
