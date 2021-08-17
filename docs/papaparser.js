
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
	$('#files').parse({
		config: {
			delimiter: "auto",
			complete: displayHTMLTable,
		},
		before: function(file, inputElem)
		{
			//console.log("Parsing file...", file);
		},
		error: function(err, file)
		{
			//console.log("ERROR:", err, file);
		},
		complete: function()
		{
			//console.log("Done with all files");
		}
	});
