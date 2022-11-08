//Read the data
d3.json("js/PMR.json", function(d) {

  records = d.record;
  // console.log('records = ');
  // console.log(records
  // read each record
  for (let i = 0; i < records.length; i++) {

    // for each sensor make a plot
    let sensors = ['ACC', 'BVP', 'EDA', 'HR', 'TEMP'];

    for (let k = 0; k < sensors.length; k++) {

      let sensor = sensors[k];

      // read the wearable for each record

      wearables = records[i].wearable;
      var traces = [];
      for (let j = 0; j < wearables.length; j++) {

        wearable = records[i].wearable[j];
        console.log("wearable = ");
        console.log(wearable);

        var trace1 = {
            x:  wearable[sensors[k]].tmin,
            y:  wearable[sensors[k]].meas,
            mode: 'markers',
            name: wearable["wearable_id"],
            marker: {
              size: 10,
              color: wearable[sensors[k]].color_fill,
            }
        };

        traces.push(trace1);
      };

      //var data = [trace1];
      var data = traces;
      console.log('traces = ')
      console.log(traces)

      var layout = {
          title: sensor,
          legend: {
              y: 0.5,
              yref: 'paper',
              font: {
                family: 'Arial, sans-serif',
                size: 15,
                color: 'grey',
              }
          },
      };

      //let divName = ("myDiv" + sensor);
      //console.log('divName = ');
      //console.log(divName);
      Plotly.newPlot(sensor, data, layout);

    };
  //};
  };
});
