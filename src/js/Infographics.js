function generateRandomColor() {
    return '#' + (Math.random().toString(16) + '0000000').slice(2, 8);
};

let color_palette = Array(100);
for(let i = 0; i < 100; i++){
  color_palette[i] = generateRandomColor();
}

var class_chart_canvases = Array(5);
for(let i = 0; i < 6; i++){
  class_chart_canvases[i] = document.getElementById('class-chart-' + String(i+1)).getContext('2d');
}

var data = {
  labels: ["17219", "17130", "17111", "1", "2", "3", "4", "5", "2", "4"],
  datasets: [
    {
      label: 'Voto Uscita Scuole Medie',
      data: [8.4, 8.7, 8.1, 9.3, 6.6, 7.3, 6.8, 6.1, 6.7, 8.8],
      backgroundColor: color_palette
    }
  ]
};

var options = {
  scales: {
        yAxes: [{
            display: true,
            ticks: {
                suggestedMin: 0,
                suggestedMax: 10,
                beginAtZero: true   // minimum value will be 0.
            }
        }]
    }
};

var classes_charts = Array(5);
for(let i = 0; i < 6; i++){
  classes_charts[i] = new Chart(class_chart_canvases[i], {
      type: 'bar',
      data: data,
      options: options
  });
};
