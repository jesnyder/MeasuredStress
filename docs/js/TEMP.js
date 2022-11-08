TESTER = document.getElementById('TEMP');



// set data
let records = PMR.record;
console.log(records);


for (let i = 0; i < records.length; i++) {
  wearables = records[i].wearable;
  console.log("Record number = ");
  console.log(i);

  for (let j = 0; i < wearables.length; i++) {
    wearable = records[i].wearable[j];
    console.log("wearable = ");
    console.log(wearable);

    console.log("TEMP.meas = ");
    console.log(wearable.TEMP.meas);

    console.log("TEMP.tmin = ");
    console.log(wearable.TEMP.tmin);

  }
}

Plotly.newPlot( TESTER, [{



	x: wearable.TEMP.tmin,

	y: wearable.TEMP.meas
 }],

 {
	margin: { t: 0 }
 });
