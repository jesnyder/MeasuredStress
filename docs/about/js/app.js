function drawCircle(x, y, radiusX, radiusY, rotation) {


    context.beginPath();
    context.ellipse(x, y, radiusX, radiusY, rotation, 0, 2 * Math.PI);
    context.stroke();
}

function drawLine(x, y, xdel, ydel, rotation) {
  // set line stroke and line width

  const ctx = canvas.getContext('2d');

  ctx.strokeStyle = 'green';
  ctx.lineWidth = 5;

  // draw a red line
  ctx.beginPath();
  ctx.moveTo(x, y);
  ctx.lineTo(xdel, ydel);
  ctx.stroke();
}

function drawArc() {
  //var canvas = document.getElementById('myCanvas');
  //var context = canvas.getContext('2d');
  context.beginPath();
  context.arc(100, 100, 50, 0, Math.PI*6/4, false);
  context.arc(50, 0, 25, 0, Math.PI*6/4, false);
  context.closePath();
  context.lineWidth = 5;
  context.fillStyle = 'yellow';
  context.fill();
  context.strokeStyle = '#550000';
  context.stroke();
}

function draw() {
    const canvas = document.querySelector('#canvas');

    if (!canvas.getContext) {
        return;
    }
    const ctx = canvas.getContext('2d');

    // set line stroke and line width
    ctx.strokeStyle = 'green';
    ctx.lineWidth = 5;

    // draw a red line
    ctx.beginPath();
    ctx.moveTo(50, 100);
    ctx.lineTo(300, 200);
    ctx.lineTo(300, 100);
    ctx.lineTo(200, 100);
    ctx.stroke();

}
draw();

var canvas = document.getElementById('canvas');
var context = canvas.getContext('2d');

var deg = 0;
var rad = deg * (Math.PI / 180.0);
drawCircle(100, 100, 60, 40, rad);
drawLine(100, 100, 60, 40, rad);
drawCircle(300, 100, 80, 40, rad);
drawLine(300, 100, 80, 40, rad);
drawArc();
