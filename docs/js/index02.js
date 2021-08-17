fetch('https://raw.githubusercontent.com/jesnyder/MeasuredStress/main/studies/HI/source/1542117214_A01172/ACC.csv')
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
	
	const col01 = '1542117214.000000';

	let dataAsJson = JSC.csv2Json(text);
	let male = [], female = [];
	dataAsJson.forEach(function (row) {
		//add either to male, female, or discard.
		if (row.race === 'All Races') {
			if (row.sex === 'Male') {
				male.push({x: row.year, y: row[lifeExp]});
			} else if (row.sex === 'Female') {
				female.push({x: row.year, y: row[lifeExp]});
			}
		}
	});
	return [
		{name: 'Male', points: male},
		{name: 'Female', points: female}
	];
}

function renderChart(series) {
	JSC.Chart('chartDiv', {
		series: series
	});
}
