function draw1(canvas, multp)
{
  var canvas = document.getElementById(canvas);
  if (canvas.getContext)
  {
    var context = canvas.getContext('2d');
    context.beginPath();
   // Outer circle
    context.arc(multp*75,75,50,0,Math.PI*2,true);
    context.moveTo(110,75);
    // Mouth
    context.arc(multp*75,75,35,0,Math.PI,false);
    // Lefy and Right eye
    context.moveTo(multp*55,65);
    context.arc(60,65,5,0,Math.PI*2,true);
    context.arc(90,65,5,0,Math.PI*2,true);
    context.stroke();
  }
};

function draw2(canvas, multp)
{
  var canvas = document.getElementById(canvas);
  if (canvas.getContext)
  {
    var context = canvas.getContext('2d');
    context.beginPath();
   // Outer circle
    context.arc(multp*75,75,50,0,Math.PI*2,true);
    context.moveTo(110,75);
    // Mouth
    context.arc(multp*75,75,35,0,Math.PI,false);
    // Lefy and Right eye
    context.moveTo(multp*55,65);
    context.arc(60,65,5,0,Math.PI*2,true);
    context.arc(90,65,5,0,Math.PI*2,true);
    context.stroke();
  }
};


function makeFace001(){draw1('canvas001', 5);}
function makeFace002(){draw2('canvas002', 10);}
function makeFace003(){draw1('canvas003', 15);}
