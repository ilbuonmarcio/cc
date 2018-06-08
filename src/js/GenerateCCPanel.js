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
      groupID : document.querySelector("#generatecc-groupid").value,
      configID : document.querySelector('#generatecc-configid').value
    }

    console.log(data);

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
    /*$.post("components/groupname_select.php", { ajaxrefreshrequest : true }, function(data){
      document.querySelector('#uploadcsv-groupname').innerHTML = data;
      M.FormSelect.getInstance(document.querySelector('#uploadcsv-groupname')).destroy();
      M.FormSelect.init(document.querySelector('#uploadcsv-groupname'));
    });*/
  }

  openPanel(){
    GenerateCCPanel.selectReload();
    super.openPanel();
  }
}
