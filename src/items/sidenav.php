<!-- Pannello per la creazione di un utente -->
<div id="createuser-panel" class="modal modal-fixed-footer">

  <div class="modal-content">
    <div id="createuser-form">

      <h4 class="center-align">Aggiungi Nuovo Account</h4>

      <div class="row">
        <div class="input-field col s12">
          <input placeholder="Inserisci username" id="createuser-username" name="createuser-username" type="text" class="validate">
          <label for="createuser-username">Nome Utente</label>
        </div>

        <div class="input-field col s12">
          <input placeholder="Inserisci password" id="createuser-password" name="createuser-password" type="text" class="validate">
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
<!-- fine creazione di un utente -->


<!-- Pannello per la gestione dei gruppi -->
<div id="managegroups-panel" class="modal modal-fixed-footer">

  <div class="modal-content">
        <h4 class="center-align">Gestisci Gruppi</h4>
      <div id="managegroups-table" class="col s12 center-align">
        <h6 class="center-align">Lista Gruppi</h6>
        <?php include("grouptable.php"); ?>
      </div>
      <div class="divider"></div>

      <div id="managegroupscreate-form">

        <div class="row">

          <div class="input-field col s12">
            <input placeholder="Inserisci Nome del gruppo" id="managegroupscreate-groupname" name="managegroupscreate-groupname" type="text" class="validate">
            <label for="managegroupscreate-groupname">Nome gruppo</label>
          </div>

          <div class="input-field col s12">
            <input placeholder="Inserisci Descrizione del gruppo" id="managegroupscreate-groupdesc" name="managegroupscreate-groupdesc" type="text" class="validate">
            <label for="managegroupscreate-groupdesc">Descrizione gruppo</label>
          </div>

          <div class="input-field col s12">
            <select id="managegroupscreate-grouptype" name="managegroupscreate-grouptype">
              <option value="1" selected>Classi Prime</option>
              <option value="3">Classi Terze</option>
            </select>
            <label>Seleziona Tipo</label>
          </div>

        <div class="col s12 center-align">
          <a class="waves-effect waves-light btn" onclick="managegroupspanel.submit();">
            Crea Gruppo
          </a>
        </div>

       </div>
      </div>
      <div class="divider"></div>

      <div class="row">

      <div id= "managegroupsdelete-form">
        <div class="row">
          <h6 class="center-align">Elimina Gruppo</h6>

          <div class="input-field col s9">
            <select id="managegroupsdelete-groupname" name="managegroupsdelete-groupname">
              <?php //include("deletegroup_select.php"); ?>
            </select>
            <label>Seleziona Gruppo</label>
          </div>

          <div class="input-field col s3 center-align">
            <button onclick="managegroupsdelete.submit();" class="btn waves-effect waves-light">
              Cancella Gruppo
            </button>
          </div>

          <div class="col s12 center-align">
            <p id="managegroupsdelete-warning" style="color: red;">
              Attenzione! Questa azione eliminera anche tutti gli alunni associati a quello specifico gruppo!
            </p>
          </div>

        </div>
      </div>

    </div>
    </div>

  <div class="modal-footer">
    <a class="modal-action modal-close waves-effect waves-green btn-flat">Chiudi</a>
  </div>

</div>
<!-- fine gestione gruppi -->


<script src="js/PanelController.js"></script>
