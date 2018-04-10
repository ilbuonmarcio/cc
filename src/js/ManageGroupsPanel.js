class ManageGroupsPanel extends Panel {
  constructor(id){
    super(id);
    this.manageGroupsOnCreateSelectGroupTypeElement = document.querySelector('#managegroupscreate-grouptype');
    this.manageGroupsOnCreateSelectGroupTypeInstance = M.FormSelect.init(
      this.manageGroupsOnCreateSelectGroupTypeElement
    );
    this.manageGroupsOnDeleteSelectGroupNameElement = document.querySelector('#managegroupsdelete-groupname');
    this.manageGroupsOnDeleteSelectGroupNameInstance = M.FormSelect.init(
      this.manageGroupsOnDeleteSelectGroupNameElement
    );
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

    $.post("components/deletegroup_select.php", { ajaxrefreshrequest : true }, function(data){
      document.querySelector('#managegroupsdelete-groupname').innerHTML = data;
      M.FormSelect.getInstance(document.querySelector('#managegroupsdelete-groupname')).destroy();
      M.FormSelect.init(document.querySelector('#managegroupsdelete-groupname'));
    });

  }
}
