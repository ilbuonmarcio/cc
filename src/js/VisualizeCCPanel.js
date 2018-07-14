class VisualizeCCPanel extends Panel {
  constructor(id){
    super(id);
  }

  static tableReload(){
    $.get("http://localhost:5000/refresh_visualizecc_table", function(data){
      document.querySelector('#visualizecc-table').innerHTML = data;
      M.FormSelect.getInstance(document.querySelector('#visualizecc-table'));
    });
  }

  openPanel(){
    VisualizeCCPanel.tableReload();
    super.openPanel();
  }
}
