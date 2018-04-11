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

    console.log(formData);

    if(formData.get('filepath').name === "" || formData.get('filepath') === undefined) {
      throw new FilePathTooSmallException();
    }

    return formData;
  }

  submit(){
    try{
      var data = this.loadFieldsData();
      console.log("Sending UploadCSVPanel submit with this data object:");
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

    $.ajax({
        url: 'routines/uploadcsv.php',
        data: data,
        type: 'POST',
        contentType: false,
        processData: false,
    }).always(
      this.callbackOnSubmit
    );

    // $.post('routines/uploadcsv.php', data, this.callbackOnSubmit);
  }

  callbackOnSubmit(data){
    try{
      var response = JSON.parse(JSON.stringify(eval("(" + data + ")")));
      console.log(response);
    } catch (error){
      console.log(data);
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
