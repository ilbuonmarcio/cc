function generateRandomColor() {
    return '#' + (Math.random().toString(16) + '0000000').slice(2, 8);
};

let color_palette = Array(100);
for(let i = 0; i < 100; i++){
  color_palette[i] = generateRandomColor();
}

function getParamFromURL(name) {
    return (location.search.split(name + '=')[1] || '').split('&')[0];
}

$.ajaxSetup({
   async: false
});

var studentId = null;
$.getJSON(
	"http://127.0.0.1:5000/get_charts_data?groupid=" 
	+ getParamFromURL('groupid') 
	+ "&configid="
	+ getParamFromURL('configid'), 
	
	function(result){
    studentId = result;
});

$.ajaxSetup({
   async: true
});

function getValues(json_data){
	var class_array = [];
	var serials_array = [];
	var marks_array = [];
	
	$.each(json_data, function(class_id, value){
		//console.log(class_id);
		var serial_array = [];
		var mark_array = [];
			
		class_array.push(class_id);
			
		$.each(value, function(serial, mark){
			//console.log(serial, mark);
			serial_array.push(serial);
			mark_array.push(mark);
		});
		serials_array.push(serial_array);
		marks_array.push(mark_array);
		//console.log(serials_array);
	});
	var all_array = [];
	all_array.push(class_array, serials_array, marks_array);
	return all_array;
}

var json_data = getValues(studentId);




var class_chart_canvases = Array(json_data[0].length);
for(let i = 0; i < json_data[0].length; i++){
	class_chart_canvases[i] = document.getElementById('class-chart-' + String(i+1)).getContext('2d');
}

var data_array = Array(json_data[0].length);
for(let i = 0; i < json_data[0].length; i++){
	//console.log(json_data[1][i]);
	var data = {
	  labels: json_data[1][i], // ["17219", "17130"],
	  datasets: [
		{
		  label: "Classe " + (i + 1), // 'Voto Uscita Scuole Medie',
		  data: json_data[2][i], // [8.4, 8.7],
		  backgroundColor: color_palette
		}
	  ]
	};
	data_array.push(data);
}

//console.log(data_array[14]);


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

var classes_charts = Array(json_data[0].length);
for(let i = 0; i < json_data[0].length; i++){
	classes_charts[i] = new Chart(class_chart_canvases[i], {
        type: 'bar',
        data: data_array[14 + i],
        options: options
    });
};
