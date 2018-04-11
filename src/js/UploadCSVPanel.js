class UploadCSVPanel extends Panel {
  constructor(id){
    super(id);
    this.uploadCSVSelectGroupNameElement = document.querySelector('#uploadcsv-groupname');
    this.uploadCSVSelectGroupNameInstance = M.FormSelect.init(
      this.uploadCSVSelectGroupNameElement
    );


  }

  loadFieldsData(){

    var data = {
      groupname: document.querySelector('#uploadcsv-groupname').value,
      csv: document.querySelector('#uploadcsv-filepath').value
    };

    console.log(data);

    return;

    if(data.csv === "") {
      throw new FilePathTooSmallException();
    }

    return data;
  }

  submit(){
    try{
      var data = this.loadFieldsData();
      console.log(data);
    } catch (error){
      if(error instanceof FilePathTooSmallException){
        M.toast(
          {
            html : 'Nessun file selezionato!',
            classes: 'rounded'
          }
        );
      }
      return;
    }

    $.post('routines/uploadcsv.php', data, this.callbackOnSubmit);
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

    if(response.querystatus == "good"){
      M.toast({
        html: 'File caricato correttamente!',
        classes: 'rounded'
      });

    } else if(response.querystatus == "bad"){
      M.toast({
        html: 'Errore di query!',
        classes: 'rounded'
      });
    }
  }

  static selectReload(){
    $.post("components/groupname_select.php", { ajaxrefreshrequest : true }, function(data){
      document.querySelector('#uploadcsv-groupname').innerHTML = data;
      M.FormSelect.getInstance(document.querySelector('#uploadcsv-groupname')).destroy();
      M.FormSelect.init(document.querySelector('#uploadcsv-groupname'));
    });
  }

  openPanel(){
    UploadCSVPanel.selectReload();
    super.openPanel();
  }
}
