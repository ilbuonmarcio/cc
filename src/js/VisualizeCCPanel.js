class VisualizeCCPanel extends Panel {
  constructor(id){
    super(id);
    this.groupIDSelectElement = document.querySelector('#visualizecc-groupid');
    this.groupIDSelectInstance = M.FormSelect.init(
      this.groupIDSelectElement
    );

    this.configIDSelectElement = document.querySelector('#visualizecc-configid');
    this.configIDSelectInstance = M.FormSelect.init(
      this.configIDSelectElement
    );
  }

  loadFieldsData(){

    var data = {
      groupid : document.querySelector("#visualizecc-groupid").value,
      configid : document.querySelector("visualizecc-configid").value
    }

    return data;
  }

  submit(){
    try{
      var data = this.loadFieldsData();
    } catch (error){
      M.toast(
        {
          html : 'Errore nell`avvio visualizzazione composizione classi!',
          classes: 'rounded'
        }
      );
      return;
    }

    M.toast({
      html: 'In attesa di caricamento composizione classi...',
      classes: 'rounded'
    });

    $.ajax({
        url: 'http://localhost:5000/get_cc_visualization',
        data: data,
        type: 'POST',
    }).always(
      this.callbackOnSubmit
    );
  }

  callbackOnSubmit(data){
    try{
      var response = JSON.parse(JSON.stringify(eval("(" + data + ")")));
    } catch (error){
      M.toast({
        html: 'Messaggio di risposta dal database non compatibile!',
        classes: 'rounded'
      })
    }

    M.toast({
      html: response.message,
      classes: 'rounded'
    });
  }

  static selectReload(){
    $.get("http://localhost:5000/refresh_groupid_select", function(data){
      document.querySelector('#visualizecc-groupid').innerHTML = data;
      M.FormSelect.getInstance(document.querySelector('#visualizecc-groupid')).destroy();
      M.FormSelect.init(document.querySelector('#visualizecc-groupid'));
    });

    $.get("http://localhost:5000/refresh_configid_select", function(data){
      document.querySelector('#visualizecc-configid').innerHTML = data;
      M.FormSelect.getInstance(document.querySelector('#visualizecc-configid')).destroy();
      M.FormSelect.init(document.querySelector('#visualizecc-configid'));
    });
  }

  openPanel(){
    VisualizeCCPanel.selectReload();
    super.openPanel();
  }
}
