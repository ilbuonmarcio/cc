class InvalidFormValueError extends Error{
  constructor(msg) {
    super(msg);
    this.name = 'InvalidFormValueError';
  }
}

class Panel{
  constructor(id){
    this.id = id;
    this.panel = M.Modal.init(
      document.querySelector(this.id)
    );
  }

  initFields(){}

  loadFields(){}

  submit(){}

  open(){
    this.initFields();
    this.panel.open();
  }
}

class CreateUserPanel extends Panel{

  constructor(id){
    super(id);
    this.phpformfile = 'createuser.php';
  }

  initFields(){
    this.priviledgesSelector = M.FormSelect.init(
      document.querySelector('#createuser-priviledges')
    );
  }

  loadFields(){
    var fieldsData = {
      username : document.getElementById('createuser-username').value,
      password : document.getElementById('createuser-password').value,
      priviledges : document.getElementById('createuser-priviledges').value
    };

    if(fieldsData.username.length < 3 || fieldsData.password.length < 8) {
      throw new InvalidFormValueError();
    }

    return fieldsData;
  }

  submit(){
    try{
      var data = this.loadFields();
      console.log(data);
    } catch (e){
      if(e instanceof InvalidFormValueError){
        M.toast({
          html: 'Errore: Presenti alcuni campi vuoti!',
          classes: 'rounded'
        })
      }
      return;
    }

    $.post("utils/" + this.phpformfile, data, this.onSubmitReturn);

    M.toast({
        html: 'Form inviato!',
        classes: 'rounded'
    });
  }

  onSubmitReturn(response, status){
    response = JSON.parse(JSON.stringify(eval("(" + response + ")")));
    if (response.querystatus === "good") {
        M.toast({
            html: 'Utente inserito con successo!',
            classes: 'rounded'
        });
    }
    if (response.querystatus === "bad") {
        M.toast({
            html: response.status,
            classes: 'rounded'
        });
    }
  }
}

// Pannello per Gestione Gruppi
class ManageGroupsPanel extends Panel{

  constructor(id){
    super(id);
    this.createphpformfile = 'creategroup.php';
    this.deletephpformfile = 'deletegroup.php';
  }

  initFields(){
    this.groupTypeSelector = M.FormSelect.init(
      document.querySelector('#managegroupscreate-grouptype'));
    this.groupDeleteSelector = M.FormSelect.init(
      document.querySelector('#managegroupsdelete-groupname'));

  }

  loadFields(){
    var fieldsData = {
      groupname : document.getElementById('managegroupscreate-groupname').value,
      description : document.getElementById('managegroupscreate-groupdesc').value,
      grouptype : document.getElementById('managegroupscreate-grouptype').value
    };

    if(fieldsData.groupname.length < 1) {
      throw new InvalidFormValueError();
      M.toast({
          html: 'Form inviato!',
          classes: 'rounded'
      });
    }
    return fieldsData;
  }

  submit(){
    try{
      var data = this.loadFields();
      console.log(data);
    } catch (e){
      if(e instanceof InvalidFormValueError){
        M.toast({
          html: 'Errore, inserire un nome valido per il gruppo!',
          classes: 'rounded'
        })
      }
      return;
    }

    $.post("utils/" + this.createphpformfile, data, this.onSubmitReturn);

    M.toast({
        html: 'Form inviato!',
        classes: 'rounded'
    });
  }

  onSubmitReturn(response, status){
    response = JSON.parse(JSON.stringify(eval("(" + response + ")")));
    if (response.querystatus === "good") {
        M.toast({
            html: 'Gruppo inserito con successo!',
            classes: 'rounded'
        });
    }
    if (response.querystatus === "bad") {
        M.toast({
            html: 'Gruppo già inserito! Cambia il nome!',
            classes: 'rounded'
        });
    }
  }
}




var sidenavElem = document.querySelector('.sidenav');
var sidenavInstance = M.Sidenav.init(sidenavElem, {
  'edge': 'left'
});

createuserpanel = new CreateUserPanel('#createuser-panel');
managegroupspanel = new  ManageGroupsPanel('#managegroups-panel');
