class ConfigureCCPanel extends Panel {
  constructor(id){
    super(id);
    this.configureCCOnLoadSelectConfigNameElement = document.querySelector('#configureccload-configname');
    this.configureCCOnLoadSelectConfigNameInstance = M.FormSelect.init(
      this.configureCCOnLoadSelectConfigNameElement
    );

    this.slider = document.querySelector('#configureccsave-rangeslider');

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
      })/*,
      // Show a scale with the slider
      pips: {
        mode: 'range',
        stepped: false,
        density: 10
      }*/
    });
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
