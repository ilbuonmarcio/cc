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
  initFields(){
    this.priviledgesSelector = M.FormSelect.init(
      document.querySelector('#createuser-priviledges')
    );
  }

  loadFields(){}

  submit(){
    M.toast({
        html: 'Form inviato!',
        classes: 'rounded'
    });
  }
}

var sidenavElem = document.querySelector('.sidenav');
var sidenavInstance = M.Sidenav.init(sidenavElem, {
  'edge': 'left'
});

createuserpanel = new CreateUserPanel('#createuser-panel');
