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

function orderStudentsByMark(students, marks){
	var studentsByMarks = {
		"6" : [],
		"7" : [],
		"8" : [],
		"9" : [],
		"10" : []
	};

	for(var i = 0; i < students.length; i++) {
		studentsByMarks[String(marks[i])].push(students[i]);
	}

	var resultObject = {
		"students" : [],
		"marks" : []
	}

	for(var i = 6; i <= 10; i++) {
		studentsByMarks[String(i)].forEach(studentMark => {
			resultObject["students"].push(studentMark);
			resultObject["marks"].push(i);
		});
	}

	return resultObject;
}

function getNumberOfValuesJson(json_data) {
	var result = {};
	
	for(var i = 0; i < json_data.length; i++){
		
		if(!result[json_data[i]]){
			result[json_data[i]] = 1;
		}else{
			result[json_data[i]] = result[json_data[i]] + 1;
		}
	}
	
	return result;
}

function getNumberOfMalesFemales(json_data) {
	var result = {};
	result['m'] = 0;
	result['f'] = 0;
	
	for(var i = 0; i < json_data.length; i++){
		
		if(!result[json_data[i]]){
			result[json_data[i]] = 1;
		}else{
			result[json_data[i]] = result[json_data[i]] + 1;
		}
	}
	
	return result;
}

$.ajaxSetup({
   async: false
});

var studentMark = null;
$.getJSON(
	"http://217.182.78.79:80/get_charts_data?groupid=" 
	+ getParamFromURL('groupid') 
	+ "&configid="
	+ getParamFromURL('configid'), 
	
	function(result){
    studentMark = result;
});

var studentCap = null;
$.getJSON(
	"http://217.182.78.79:80/get_charts_data_cap?groupid=" 
	+ getParamFromURL('groupid') 
	+ "&configid="
	+ getParamFromURL('configid'), 
	
	function(result){
    studentCap = result;
});

var studentNaz = null;
$.getJSON(
	"http://217.182.78.79:80/get_charts_data_naz?groupid=" 
	+ getParamFromURL('groupid') 
	+ "&configid="
	+ getParamFromURL('configid'), 
	
	function(result){
    studentNaz = result;
});

var studentMaleFemale = null;
$.getJSON(
	"http://217.182.78.79:80/get_charts_data_male_female?groupid=" 
	+ getParamFromURL('groupid') 
	+ "&configid="
	+ getParamFromURL('configid'), 
	
	function(result){
    studentMaleFemale = result;
});

$.ajaxSetup({
   async: true
});

// Get usable json
var json_data_mark = getValues(studentMark);
var json_data_cap = getValues(studentCap);
var json_data_naz = getValues(studentNaz);
var json_data_male_female = getValues(studentMaleFemale);

// Get the number of total classes
var number_of_classes = json_data_mark[0].length;

// Writing on the canvases of the html
var class_chart_canvases_mark = Array(number_of_classes);
for(let i = 0; i < number_of_classes; i++){
	class_chart_canvases_mark[i] = document.getElementById('class-chart-' + String(i+1)).getContext('2d');
}

var class_chart_canvases_cap = Array(number_of_classes);
for(let i = 0; i < number_of_classes; i++){
	class_chart_canvases_cap[i] = document.getElementById('class-chart-' + String(i+1+number_of_classes)).getContext('2d');
}

var class_chart_canvases_naz = Array(number_of_classes);
for(let i = 0; i < number_of_classes; i++){
	class_chart_canvases_naz[i] = document.getElementById('class-chart-' + String(i+1+(number_of_classes*2))).getContext('2d');
}

var class_chart_canvases_male_female = Array(number_of_classes);
for(let i = 0; i < number_of_classes; i++){
	class_chart_canvases_male_female[i] = document.getElementById('class-chart-' + String(i+1+(number_of_classes*3))).getContext('2d');
}

var class_chart_canvases_classes_mark = document.getElementById('class-chart-' + String(1+(number_of_classes*4))).getContext('2d');

// Creating the data to use in charts
var data_array_mark = Array(number_of_classes);
for(let i = 0; i < number_of_classes; i++){
	var orderedData = orderStudentsByMark(json_data_mark[1][i], json_data_mark[2][i]);
	var studentIDs = orderedData["students"];
	var studentMarks = orderedData["marks"];
	var data = {
	  labels: studentIDs, // ["17219", "17130"],
	  datasets: [
		{
		  label: "Classe " + (i + 1), // 'Voto Uscita Scuole Medie',
		  data: studentMarks, // [8.4, 8.7],
		  backgroundColor: color_palette
		}
	  ]
	};
	data_array_mark.push(data);
}


var data_array_cap = Array(number_of_classes);
for(let i = 0; i < number_of_classes; i++){
	var dataCaps = getNumberOfValuesJson(json_data_cap[2][i]);
	var data = {
	  labels: Object.keys(dataCaps), // ["17219", "17130"],
	  datasets: [
		{
		  label: "Classe " + (i + 1), // 'Cap per Classe',
		  data: Object.values(dataCaps), // [21234, 31312],
		  backgroundColor: color_palette
		}
	  ]
	};
	data_array_cap.push(data);
}

var data_array_naz = Array(number_of_classes);
for(let i = 0; i < number_of_classes; i++){
	var dataNazs = getNumberOfValuesJson(json_data_naz[2][i]);
	var data = {
	  labels: Object.keys(dataNazs), // ["17219", "17130"],
	  datasets: [
		{
		  label: "Classe " + (i + 1), // 'Cap per Classe',
		  data: Object.values(dataNazs), // [21234, 31312],
		  backgroundColor: color_palette
		}
	  ]
	};
	data_array_naz.push(data);
}

var data_array_male_female = Array(number_of_classes);
for(let i = 0; i < number_of_classes; i++){
	var dataMalesFemales = getNumberOfMalesFemales(json_data_male_female[2][i]);
	var data = {
	  labels: [
		'Maschi',
		'Femmine'
	  ],
	  datasets: [
		{
		  data: Object.values(dataMalesFemales), // [26, 2]
		  backgroundColor: color_palette
		}
	  ]
	};
	data_array_male_female.push(data);
}


var data_array_classes_mark;
console.log(json_data_mark);
var average = Array();


for(let i = 0; i < number_of_classes; i++){
	var sum = 0;
	
	for(var l = 0; l < json_data_mark[2][i].length; l++){
		
		sum += json_data_mark[2][i][l]
		
	}
	
	average.push(sum/json_data_mark[2][i].length);
}

var data_array_classes_mark_min_thresold = 10;
var data_array_classes_mark_max_thresold = 0;

for(avg of average) {
	if(avg < data_array_classes_mark_min_thresold) {
		data_array_classes_mark_min_thresold = avg;
	}
	if(avg > data_array_classes_mark_max_thresold) {
		data_array_classes_mark_max_thresold = avg;
	}
}

data_array_classes_mark_min_thresold -= 0.1;
data_array_classes_mark_max_thresold += 0.1;


var data = {
		labels: json_data_mark[0], // ["17219", "17130"],
		datasets: [
		{
			label: "Media Voti Classi", // 'Cap per Classe',
			data: average, // [21234, 31312],
			backgroundColor: color_palette
		}
	]
};
data_array_classes_mark = data;


// Option of the charts
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

// Creating the chart
var classes_charts_mark = Array(number_of_classes);
for(let i = 0; i < number_of_classes; i++){
	classes_charts_mark[i] = new Chart(class_chart_canvases_mark[i], {
        type: 'bar',
        data: data_array_mark[number_of_classes + i],
        options: options
    });
};

var classes_charts_cap = Array(number_of_classes);
for(let i = 0; i < number_of_classes; i++){
	classes_charts_cap[i] = new Chart(class_chart_canvases_cap[i], {
        type: 'bar',
        data: data_array_cap[number_of_classes + i],
        options: options
    });
};

var classes_charts_naz = Array(number_of_classes);
for(let i = 0; i < number_of_classes; i++){
	classes_charts_naz[i] = new Chart(class_chart_canvases_naz[i], {
        type: 'bar',
        data: data_array_naz[number_of_classes + i],
        options: options
    });
};

var classes_charts_male_female = Array(number_of_classes);
for(let i = 0; i < number_of_classes; i++){
	classes_charts_male_female[i] = new Chart(class_chart_canvases_male_female[i], {
        type: 'pie',
        data: data_array_male_female[number_of_classes + i],
        options: Chart.defaults.pie
    });
};

var options = {
	scales: {
		  yAxes: [{
			  display: true,
			  ticks: {
				  suggestedMin: data_array_classes_mark_min_thresold,
				  suggestedMax: data_array_classes_mark_max_thresold
			  }
		  }]
	  }
  };

var classes_charts_classes_mark = new Chart(class_chart_canvases_classes_mark, {
    type: 'bar',
    data: data_array_classes_mark,
    options: options
});