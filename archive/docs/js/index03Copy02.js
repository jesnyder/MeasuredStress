plotFromCSV();


// Plot data retrieved from git hub repo
function plotFromCSV() {
	console.log('plotFromCSV running')
	let urlPrefix = 'https://raw.githubusercontent.com/jesnyder/MeasuredStress/main/studies/HI/source/1542117214_A01172/';
	let urlSuffix = '.csv';
	let sensorList = ['ACC', 'BVP', 'HR', 'EDA', 'TEMP'];

	for(var j = 0, size = sensorList.length; j < size ; j++){
		var sensor = sensorList[j];
		console.log(sensor);
		csvUrl = urlPrefix + sensor + urlSuffix;
		console.log(csvUrl);

		fetch(csvUrl).then(function (response) {
			console.log('fetching csvURL for ' + sensor + ' using ' + csvUrl);
			return response.text();
	 	})
	 	.then(function (text) {
			console.log(text.length);
			let series = csvToSeries(text, sensor);
			renderChart(series, sensor, j);
	 	})
	 	.catch(function (error) {
		 	//Something went wrong
		 	console.log(error);
	 	});
	}

}



// create series to be plotted from the retrieved data
function csvToSeries(text, sensor) {
	console.log(text.length);
	var inc = 1;
	let dataAsJson = JSC.csv2Json(text);
	let meas = [];
	dataAsJson.forEach(function (row) {
		if (inc > 2){
			meas.push({x: inc, y: row[0]});
		}
		inc = inc+1;
	});
console.log(meas.length)
return [{name: 'Source ' + sensor, points: meas}];
}


// build the chart from series
function renderChart(series, sensor, j) {
	chartDivNum = 'chartDiv' + j.toString();
	console.log('chartDiv')
	JSC.Chart(chartDivNum , {
 		series: series
	});
}
