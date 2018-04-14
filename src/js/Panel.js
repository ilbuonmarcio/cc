class Panel {

  constructor(id){
    this.id = id;
    this.panel = document.querySelector(id);
    this.instance = M.Modal.init(this.panel);
  }

  openPanel(){
    this.instance.open();
  }

  closePanel(){
    this.instance.close();
  }

  loadFieldsData(){}

  checkFieldsData(){}

  submit(){}

  callbackOnSubmit(){}
}
