let urlPrefix = 'https://raw.githubusercontent.com/jesnyder/MeasuredStress/main/studies/HI/source/1542117214_A01172/';
let urlSuffix = '.csv'

//let studyList = ['HI', 'PMR'];
let analysisList = ['source'];
let sensorList = ['ACC', 'BVP', 'HR', 'EDA', 'TEMP'];

for(var i = 0, size = analysisList.length; i < size ; i++){
for(var j = 0, size = sensorList.length; j < size ; j++){

	 var analysis = analysisList[i];
	 var sensor = sensorList[j];

	 csvUrl = urlPrefix + sensor + urlSuffix
	 console.log(csvUrl)

	 fetch(csvUrl)
 	.then(function (response) {
 		return response.text();
 	})
 	.then(function (text) {
 		let series = csvToSeries(text);
 		renderChart(series);
 	})
 	.catch(function (error) {
 		//Something went wrong
 		console.log(error);
 	});

 	function csvToSeries(text) {

 	var inc = 1;

 	let dataAsJson = JSC.csv2Json(text);
 	let time = [], meas = [];
 	dataAsJson.forEach(function (row) {

 		//console.log(row)
 		//console.log(row[1])

 		if (row[1] < 10000){
 		meas.push({x: inc, y: row[0]});
 		inc = inc+1;
 		//console.log(inc)
 		}

 	});

 	//console.log(meas)

 	return [
 		{name: 'Meas', points: meas},
 		{name: 'Meas 2', points: sensor}
 	];
 	}

 	function renderChart(series) {
 	JSC.Chart('chartDiv', {
 		series: series
 	});
 	}






 }}
