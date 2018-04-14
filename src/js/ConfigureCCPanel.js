class ConfigureCCPanel extends Panel {
  constructor(id){
    super(id);
    this.configureCCOnLoadSelectConfigNameElement = document.querySelector('#configureccload-configname');
    this.configureCCOnLoadSelectConfigNameInstance = M.FormSelect.init(
      this.configureCCOnLoadSelectConfigNameElement
    );

    this.slider = document.getElementById('configureccsave-rangeslider');

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
      }),
      pips: {
        mode: 'range',
        stepped: false,
        density: 10
      }
    });
  }

  toggleMFSwitch(){
    if(document.querySelector('#configureccsave-checkboxmf').checked){
      document.querySelector('#configureccsave-nummales').disabled = true;
      document.querySelector('#configureccsave-numfemales').disabled = false;
      document.querySelector('#configureccsave-nummales').value = "";
    } else{
      document.querySelector('#configureccsave-nummales').disabled = false;
      document.querySelector('#configureccsave-numfemales').disabled = true;
      document.querySelector('#configureccsave-numfemales').value = "";
    }
  }

  loadFieldsLoadData(){
    var configid = document.querySelector('#configureccload-configname').value;

    var data = {
      configid : configid
    };

    M.toast({
      html: 'Caricamento configurazione in corso...',
      classes: 'rounded'
    })

    $.post('routines/loadconfig.php', data, this.loadDataIntoFieldsCallback);
  }

  loadDataIntoFieldsCallback(data){
    try{
      var response = JSON.parse(JSON.stringify(eval("(" + data + ")")));
    } catch (error){
      M.toast({
        html: 'Impossibile caricare la configurazione!',
        classes: 'rounded'
      })
      return;
    }

    // Caricare i dati disponibili nel form
    document.querySelector('#configureccsave-configname').value = response.values.configname;
    document.querySelector('#configureccsave-rangeslider').noUiSlider.set([response.values.min_alunni, response.values.max_alunni]);
    if(response.values.numero_maschi !== "" && response.values.numero_femmine === ""){
      document.querySelector('#configureccsave-checkboxmf').checked = false;
    } else if(response.values.numero_maschi === "" && response.values.numero_femmine !== ""){
      document.querySelector('#configureccsave-checkboxmf').checked = true;
    } else{
      M.toast({
        html: 'Numero maschi e femmine non consistenti nel database!',
        classes: 'rounded'
      });
    }
    document.querySelector('#configureccsave-nummales').value = response.values.numero_maschi;
    document.querySelector('#configureccsave-numfemales').value = response.values.numero_femmine;
    document.querySelector('#configureccsave-numcap').value = response.values.max_per_cap;
    document.querySelector('#configureccsave-num170').value = response.values.num_170;
    document.querySelector('#configureccsave-numnaz').value = response.values.max_naz;
    document.querySelector('#configureccsave-nummaxforeachnaz').value = response.values.max_per_naz;

    M.toast({
      html: 'Dati caricati nel form!',
      classes: 'rounded'
    })
  }

  submitLoad(){
    this.loadFieldsLoadData();
  }

  static selectReload(){
    $.post("components/configname_select.php", { ajaxrefreshrequest : true }, function(data){
      document.querySelector('#configureccload-configname').innerHTML = data;
      M.FormSelect.getInstance(document.querySelector('#configureccload-configname')).destroy();
      M.FormSelect.init(document.querySelector('#configureccload-configname'));
    });
  }

  openPanel(){
    ConfigureCCPanel.selectReload();
    super.openPanel();
  }
}
