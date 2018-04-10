class ManageGroupsPanel extends Panel {
  constructor(id){
    super(id);
  }

  loadFieldsCreateData(){
    var data = {

    };

    return data;
  }

  loadFieldsDeleteData(){
    var data = {

    };

    return data;
  }

  submitCreate(){
    try{
      var data = this.loadFieldsCreateData();
    } catch (error){
      if(error instanceof InvalidUsernameOrPasswordLengthException){
        M.toast(
          {
            html : 'Criteri di input non rispettati!',
            classes: 'rounded'
          }
        );
      }
      return;
    }

    $.post('routines/creategroup.php', data, this.callbackOnCreateSubmit);
  }

  submitDelete(){
    try{
      var data = this.loadFieldsDeleteData();
    } catch (error){
      if(error instanceof InvalidUsernameOrPasswordLengthException){
        M.toast(
          {
            html : 'Criteri di input non rispettati!',
            classes: 'rounded'
          }
        );
      }
      return;
    }

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

    } else if(response.querystatus == "bad"){
      M.toast({
        html: 'Impossibile cancellare il gruppo!',
        classes: 'rounded'
      });
    }
  }
}
