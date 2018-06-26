function generateRandomColor() {
    return '#' + (Math.random().toString(16) + '0000000').slice(2, 8);
};

let color_palette = Array(100);
for(let i = 0; i < 100; i++){
  color_palette[i] = generateRandomColor();
}

var ctx = document.getElementById('myChart').getContext('2d');

var data = {
  labels: ["17219", "17130", "17111"],
  datasets: [
    {
      label: 'Voto Uscita Scuola Secondaria di Primo Grado',
      data: [8.4, 8.7, 8.1],
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

var myBarChart = new Chart(ctx, {
    type: 'bar',
    data: data,
    options: options
});
