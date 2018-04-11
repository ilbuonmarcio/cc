class ConfigureCCPanel extends Panel {
  constructor(id){
    super(id);
    this.configureCCOnLoadSelectConfigNameElement = document.querySelector('#configureccload-configname');
    this.configureCCOnLoadSelectConfigNameInstance = M.FormSelect.init(
      this.configureCCOnLoadSelectConfigNameElement
    );

    this.slider = document.querySelector('#configureccsave-rangeslider');

    noUiSlider.create(this.slider, {
      start: [15, 30],
      connect: true,
      step: 1,
      range: {
        'min': 10,
        'max': 35
      },
      format: wNumb({
        decimals: 0
      })/*,
      // Show a scale with the slider
      pips: {
        mode: 'range',
        stepped: false,
        density: 10
      }*/
    });
  }

  loadFieldsCreateData(){
    var data = {
      groupname : document.querySelector('#managegroupscreate-groupname').value,
      groupdesc : document.querySelector('#managegroupscreate-groupdesc').value,
      grouptype : document.querySelector('#managegroupscreate-grouptype').value
    };

    if(data.groupname.length < 3){
         throw new GroupNameTooSmallException();
    }

    return data;
  }

  loadFieldsDeleteData(){
    var data = {
      groupname : document.querySelector('#managegroupsdelete-groupname').value
    };

    return data;
  }

  submitCreate(){
    try{
      var data = this.loadFieldsCreateData();
    } catch (error){
      if(error instanceof GroupNameTooSmallException){
        M.toast(
          {
            html : 'Criteri di input non rispettati! Il nome del gruppo deve essere di minimo 3 caratteri.',
            classes: 'rounded'
          }
        );
      }
      return;
    }

    $.post('routines/creategroup.php', data, this.callbackOnCreateSubmit);
  }

  submitDelete(){
    var data = this.loadFieldsDeleteData();

    $.post('routines/deletegroup.php', data, this.callbackOnDeleteSubmit);
  }

  callbackOnCreateSubmit(data){
    try{
      var response = JSON.parse(JSON.stringify(eval("(" + data + ")")));
    } catch (error){
      M.toast({
        html: 'Messaggio di risposta dal database non compatibile!',
        classes: 'rounded'
      })
      return;
    }

    if(response.querystatus == "good"){
      M.toast({
        html: 'Nuovo gruppo creato correttamente!',
        classes: 'rounded'
      });

      ManageGroupsPanel.tableReload();
      ManageGroupsPanel.selectReload();

    } else if(response.querystatus == "bad"){
      M.toast({
        html: 'Impossibile creare il gruppo!',
        classes: 'rounded'
      });
    }
  }

  callbackOnDeleteSubmit(data){
    try{
      var response = JSON.parse(JSON.stringify(eval("(" + data + ")")));
    } catch (error){
      M.toast({
        html: 'Messaggio di risposta dal database non compatibile!',
        classes: 'rounded'
      })
      return;
    }

    if(response.querystatus == "good"){
      M.toast({
        html: 'Gruppo eliminato correttamente!',
        classes: 'rounded'
      });

      ManageGroupsPanel.tableReload();
      ManageGroupsPanel.selectReload();

    } else if(response.querystatus == "bad"){
      M.toast({
        html: 'Impossibile cancellare il gruppo!',
        classes: 'rounded'
      });
    }
  }

  static tableReload(){
    $.post("components/grouptableview.php", { ajaxrefreshrequest : true }, function(data){
      document.querySelector('#managegroups-table').innerHTML = data;
    });
  }

  static selectReload(){
    $.post("components/groupname_select.php", { ajaxrefreshrequest : true }, function(data){
      document.querySelector('#managegroupsdelete-groupname').innerHTML = data;
      M.FormSelect.getInstance(document.querySelector('#managegroupsdelete-groupname')).destroy();
      M.FormSelect.init(document.querySelector('#managegroupsdelete-groupname'));
    });
  }

  openPanel(){
    ManageGroupsPanel.tableReload();
    ManageGroupsPanel.selectReload();
    super.openPanel();
  }
}
