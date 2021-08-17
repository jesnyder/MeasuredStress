url = "https://raw.githubusercontent.com/jesnyder/MeasuredStress/main/studies/HI/source/1542117214_A01172/ACC.csv"
 
async function getData() {
	const response = await fetch(`HR.csv`);
	const table = await response.text();
}


for(var i = 0, size = records.length; i < size ; i++){
   //var item = src_list[i];
	 src_link = link_prefix + study_name + '/' + format + '/' + records[i] + '/' + sensor + '.csv';
	 plot(src_link, i);
}


function plot(src, i) {
	fetch(src)
		.then(function (response) {
			return response.text();
		})
		.then(function (text) {
			let series = csvToSeries(text);
			renderChart(series, i);
		})
		.catch(function (error) {
			//Something went wrong
			console.log(error);
		});
	}


function csvToSeries(text) {
	const lifeExp = 'average_life_expectancy';
	const time = 'timeMinutes';
	const meas = 'measurement';
	let dataAsJson = JSC.csv2Json(text);
	let source = [];
	dataAsJson.forEach(function (row) {
		source.push({x: row[time], y: row[meas]});
		//add either to male, female, or discard.

	});
	return [
		{name: 'Source', points: source},
		//{name: 'Source', points: source}
	];
}

function renderChart(series, i){
	const chartDiv = 'chartDiv' + i
	JSC.Chart(chartDiv, {
		title_label_text: 'Record: ' + i,
		annotations: [{
			label_text: 'Source: Empatica E4 Wearables',
			position: 'bottom left'
		}],
        legend_visible: false,
		defaultSeries_lastPoint_label_text: '<b>%seriesName</b>',
		//defaultPoint_tooltip: '%seriesName <b>%yValue</b> degrees',
		defaultPoint_tooltip: '<b>%yValue</b> degrees',
		xAxis_crosshair_enabled: true,
		series: series
	});


}
