class VisualizeCCPanel extends Panel {
  constructor(id){
    super(id);
  }

  static tableReload(){
    $.get("http://217.182.78.79:80/refresh_visualizecc_table", function(data){
      document.querySelector('#visualizecc-table').innerHTML = data;
      M.FormSelect.getInstance(document.querySelector('#visualizecc-table'));
    });
  }

  openPanel(){
    VisualizeCCPanel.tableReload();
    super.openPanel();
  }
}
