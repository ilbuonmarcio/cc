class GenerateCCPanel extends Panel {
  constructor(id){
    super(id);
    this.groupIDSelectElement = document.querySelector('#generatecc-groupid');
    this.groupIDSelectInstance = M.FormSelect.init(
      this.groupIDSelectElement
    );

    this.configIDSelectElement = document.querySelector('#generatecc-configid');
    this.configIDSelectInstance = M.FormSelect.init(
      this.configIDSelectElement
    );

  }

  loadFieldsData(){

    var data = {
      groupid : document.querySelector("#generatecc-groupid").value,
      configid : document.querySelector('#generatecc-configid').value
    }

    return data;
  }

  submit(){
    try{
      var data = this.loadFieldsData();
    } catch (error){
      M.toast(
        {
          html : 'Errore nell`avvio della composizione classi!',
          classes: 'rounded'
        }
      );
      return;
    }

    M.toast({
      html: 'In attesa di composizione classi...',
      classes: 'rounded'
    });

    $.ajax({
        url: 'http://localhost:5000/get_cc_result',
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
      return;
    }

    M.toast({
      html: response.message,
      classes: 'rounded'
    });
  }

  static selectReload(){
    $.get("http://localhost:5000/refresh_groupid_select", function(data){
      document.querySelector('#generatecc-groupid').innerHTML = data;
      M.FormSelect.getInstance(document.querySelector('#generatecc-groupid')).destroy();
      M.FormSelect.init(document.querySelector('#generatecc-groupid'));
    });

    $.get("http://localhost:5000/refresh_configid_select", function(data){
      document.querySelector('#generatecc-configid').innerHTML = data;
      M.FormSelect.getInstance(document.querySelector('#generatecc-configid')).destroy();
      M.FormSelect.init(document.querySelector('#generatecc-configid'));
    });
  }

  openPanel(){
    GenerateCCPanel.selectReload();
    super.openPanel();
  }
}
