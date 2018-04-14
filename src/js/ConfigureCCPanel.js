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
      document.querySelector('#configureccsave-numfemales').value = "1";
    } else{
      document.querySelector('#configureccsave-nummales').disabled = false;
      document.querySelector('#configureccsave-numfemales').disabled = true;
      document.querySelector('#configureccsave-numfemales').value = "";
      document.querySelector('#configureccsave-nummales').value = "1";
    }
  }

  fillFieldsDataFromDB(){
    var configid = document.querySelector('#configureccload-configname').value;

    var data = {
      configid : configid
    };

    M.toast({
      html: 'Caricamento configurazione in corso...',
      classes: 'rounded'
    })

    $.post('routines/loadconfig.php', data, this.fillFieldsDataFromDBCallback);
  }

  fillFieldsDataFromDBCallback(data){
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
    document.querySelector('#configureccsave-nummales').value = response.values.numero_maschi;
    document.querySelector('#configureccsave-numfemales').value = response.values.numero_femmine;
    if(response.values.numero_maschi !== "" && response.values.numero_femmine === ""){
      document.querySelector('#configureccsave-checkboxmf').checked = false;
      document.querySelector('#configureccsave-nummales').disabled = false;
      document.querySelector('#configureccsave-numfemales').disabled = true;
    } else if(response.values.numero_maschi === "" && response.values.numero_femmine !== ""){
      document.querySelector('#configureccsave-checkboxmf').checked = true;
      document.querySelector('#configureccsave-nummales').disabled = true;
      document.querySelector('#configureccsave-numfemales').disabled = false;
    } else{
      M.toast({
        html: 'Numero maschi e femmine non consistenti nel database!',
        classes: 'rounded'
      });
    }
    document.querySelector('#configureccsave-numcap').value = response.values.max_per_cap;
    document.querySelector('#configureccsave-num170').value = response.values.num_170;
    document.querySelector('#configureccsave-numnaz').value = response.values.max_naz;
    document.querySelector('#configureccsave-nummaxforeachnaz').value = response.values.max_per_naz;

    M.toast({
      html: 'Dati caricati nel form!',
      classes: 'rounded'
    })
  }

  loadFieldsData(){
    var data = {
      configname : document.querySelector('#configureccsave-configname').value,
      rangeslider_down : this.slider.noUiSlider.get()[0],
      rangeslider_up : this.slider.noUiSlider.get()[1],
      nummales : document.querySelector('#configureccsave-nummales').value,
      numfemales : document.querySelector('#configureccsave-numfemales').value,
      numcap : document.querySelector('#configureccsave-numcap').value,
      num170 : document.querySelector('#configureccsave-num170').value,
      numnaz : document.querySelector('#configureccsave-numnaz').value,
      nummaxforeachnaz : document.querySelector('#configureccsave-nummaxforeachnaz').value
    };

    if(
      data.configname === "" ||
      data.rangeslider_up === "" || data.rangeslider_up > 35 || data.rangeslider_up < data.rangeslider_down ||
      data.rangeslider_down === "" || data.rangeslider_down < 10 || data.rangeslider_down > data.rangeslider_up ||
      data.numcap === "" ||
      data.num170 === "" ||
      data.numnaz === "" ||
      data.nummaxforeachnaz === "") {
        throw new EmptyFieldsOnConfigureCCPanelUpload();
    }

    if(
      document.querySelector('#configureccsave-checkboxmf').checked &&
      document.querySelector('#configureccsave-numfemales').value === ""){
        throw new EmptyFieldsOnConfigureCCPanelUpload();
    }

    if(
      !document.querySelector('#configureccsave-checkboxmf').checked &&
      document.querySelector('#configureccsave-nummales').value === ""){
        throw new EmptyFieldsOnConfigureCCPanelUpload();
    }

    return data;
  }

  submit(){
    try{
      var data = this.loadFieldsData();
    } catch (error){
      if(error instanceof EmptyFieldsOnConfigureCCPanelUpload){
        M.toast(
          {
            html : 'Sono presenti dei campi vuoti!',
            classes: 'rounded'
          }
        );
      }
      return;
    }

    $.post('routines/createconfig.php', data, this.callbackOnSubmit);
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
        html: 'Configurazione inserita e/o aggiornata correttamente!',
        classes: 'rounded'
      });

    } else if(response.querystatus == "bad"){
      M.toast({
        html: 'Errore di query del database!',
        classes: 'rounded'
      });
    }
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
