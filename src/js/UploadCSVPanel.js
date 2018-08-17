class UploadCSVPanel extends Panel {
  constructor(id){
    super(id);
    this.uploadCSVSelectGroupNameElement = document.querySelector('#uploadcsv-groupname');
    this.uploadCSVSelectGroupNameInstance = M.FormSelect.init(
      this.uploadCSVSelectGroupNameElement
    );


  }

  loadFieldsData(){

    var form = document.querySelector('#uploadcsv-form');
    var formData = new FormData(form);

    formData.append('groupname', document.querySelector("#uploadcsv-groupname").value);
    formData.append('filepath', document.querySelector('#uploadcsv-filepath').files[0]);

    if(formData.get('filepath').name === "" || formData.get('filepath').name === undefined) {
      throw new FilePathTooSmallException();
    }

    return formData;
  }

  submit(){
    try{
      var data = this.loadFieldsData();
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

    M.toast({
      html: 'In attesa di upload completato...',
      classes: 'rounded'
    });

    $.ajax({
        url: 'http://217.182.78.79:80/routine_uploadcsv',
        data: data,
        type: 'POST',
        contentType: false,
        processData: false
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

    if(response.querystatus == "good"){
      M.toast({
        html: 'File caricato correttamente!',
        classes: 'rounded'
      });

      M.toast({
        html: 'Record inseriti correttamente: ' + response.right,
        classes: 'rounded'
      });

      M.toast({
        html: 'Record inseriti erratamente: ' + response.wrong,
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
    $.get("http://217.182.78.79:80/refresh_groupname_select", function(data){
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
