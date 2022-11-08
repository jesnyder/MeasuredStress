d3 =

  Object {
  format: ƒ(t)
  formatPrefix: ƒ(t, n)
  timeFormat: ƒ(t)
  timeParse: ƒ(t)
  utcFormat: ƒ(t)
  utcParse: ƒ(t)
  Adder: class
  Delaunay: class
  FormatSpecifier: ƒ(t)
  InternMap: class
  InternSet: class
  Node: ƒ(t)
  Voronoi: class
  ZoomTransform: ƒ(t, n, e)
  active: ƒ(t, n)
  arc: ƒ()
  area: ƒ(t, n, e)
  areaRadial: ƒ()
  ascending: ƒ(t, n)
  autoType: ƒ(t)
  axisBottom: ƒ(t)
  axisLeft: ƒ(t)
  axisRight: ƒ(t)
  axisTop: ƒ(t)
  bin: ƒ()
  bisect: ƒ(…)
  bisectCenter: ƒ(…)
  bisectLeft: ƒ(…)
  bisectRight: ƒ(…)
  bisector: ƒ(t)
  blob: ƒ(t, n)
  blur: ƒ(t, n)
  blur2: ƒ(…)
  blurImage: ƒ(…)
  brush: ƒ()
  brushSelection: ƒ(t)
  brushX: ƒ()
  brushY: ƒ()
  buffer: ƒ(t, n)
  chord: ƒ()
  … more
}

d3 = require('d3')


size =

  Object {
  width: 600
  height: 400
}


margin =

  Object {
  top: 12
  right: 10
  bottom: 26
  left: 26
}

dataLength = 500

data = Array.from({length: dataLength}, () => ({x: Math.random(), y: Math.pow(Math.random(), 2)}))

xScale = ƒ(n)

yScale = ƒ(n)

xAxis = ƒ(h)

yAxis = ƒ(h)

chroma = require('d3-scale-chromatic')

fillScale = ƒ(n)
