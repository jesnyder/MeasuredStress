//Read the data
d3.json("js/PMR.json", function(d) {

  records = d.record

  // read each record
  for (let i = 0; i < records.length; i++) {

    // read the wearable for each record
    wearables = records[i].wearable;
    for (let j = 0; j < wearables.length; j++) {
      wearable = records[i].wearable[j];
      console.log("wearable = ");
      console.log(wearable);

      data = wearable.EDA
      console.log("data = ");
      console.log(data);

      xx = data.tmin
      console.log("xx = ");
      console.log(xx);

      yy = data.meas
      console.log("yy = ");
      console.log(yy);

      color_fill = data["color_fill"]
      console.log("color_fill = ");
      console.log(data["color_fill"]);

}


// set the dimensions and margins of the graph
var margin = {top: 10, right: 30, bottom: 30, left: 60},
    width = 460 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

// append the svg object to the body of the page
var svg = d3.select("#my_dataviz")
    .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");


      // const ymax = Math.max(yy);
      // console.log('ymax = ');
      // console.log(ymax);

      let data = []
      let myJson;
      for(let k = 0; k < xx.length; k++){

        myJson = { "x": xx[k], "y": yy[k], "color": color_fill[k] };
        data.push(myJson);

        // Add X axis
        var x = d3.scaleLinear()
            .domain([0, 2 ])
            .range([ 0, width ]);

        svg.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x));

        // Add Y axis
        var y = d3.scaleLinear()
            .domain([0, 10 ])
            .range([ height, 0]);
          svg.append("g")
            .call(d3.axisLeft(y));

        // Add dots
          svg.append('g')
            .selectAll("dot")
            .data(data)
            .enter()
            .append("circle")
            //.attr("cx", function (data) { return x(data.x); } )
            .attr("cx", xx[k] )
            //.attr("cy", function (data) { return y(data.y); } )
            .attr("cx", yy[k] )
            .attr("r", 1.5)
            .style("fill", color_fill[k])



      }

        console.log('list = ');
        console.log(list);

        var data = list;

        console.log('list/data = ');
        console.log(data);



        console.log('data.x = ');
        console.log(data.x);

        console.log('data.color = ');
        console.log(data.color);



      }

  }
