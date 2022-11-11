// https://stackoverflow.com/questions/31791955/add-href-to-canvas-element

var canvas=document.getElementById("canvas");
var ctx=canvas.getContext("2d");
var cw=canvas.width;
var ch=canvas.height;
function reOffset(){
  var BB=canvas.getBoundingClientRect();
  offsetX=BB.left;
  offsetY=BB.top;
}
var offsetX,offsetY;
reOffset();
window.onscroll=function(e){ reOffset(); }
window.onresize=function(e){ reOffset(); }

var isDown=false;
var startX,startY;

var hexes=[];
hexes.push({
  points:[{x:57.5,y:63},{x:42.5,y:63},{x:35,y:50},{x:42.5,y:37},{x:57.5,y:37},{x:65,y:50}],
  url:'http://stackoverflow.com',
});

draw();

$("#canvas").mousedown(function(e){handleMouseDown(e);});

function draw(){
  for(var i=0;i<hexes.length;i++){
    var h=hexes[i];
    ctx.beginPath();
    ctx.moveTo(h.points[0].x,h.points[0].y);
    for(var j=1;j<h.points.length;j++){
      ctx.lineTo(h.points[j].x,h.points[j].y);
    }
    ctx.closePath();
    ctx.stroke();
  }
}


function handleMouseDown(e){
  // tell the browser we're handling this event
  e.preventDefault();
  e.stopPropagation();

  mouseX=parseInt(e.clientX-offsetX);
  mouseY=parseInt(e.clientY-offsetY);

  for(var i=0;i<hexes.length;i++){
    var h=hexes[i];
    ctx.beginPath();
    ctx.moveTo(h.points[0].x,h.points[0].y);
    for(var j=1;j<h.points.length;j++){
      ctx.lineTo(h.points[j].x,h.points[j].y);
    }
    ctx.closePath();
    //if(ctx.isPointInPath(mouseX,mouseY)){ window.open(h.url, '_blank'); }
    if(ctx.isPointInPath(mouseX,mouseY)){ alert('Navigate to: '+h.url); }
  }
}
