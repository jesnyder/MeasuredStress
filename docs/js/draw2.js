
  // example https://www.w3resource.com/javascript-exercises/javascript-drawing-exercises.php

  var canvases = document.getElementsByTagName('canvas');

    for( var i=0; i<canvases.length; i++){
         ctx = canvases[i].getContext('2d');

         multp = i*1

         

         // Outer circle
         ctx.arc(75+multp*10,75+multp*10,50+multp*10,0,Math.PI*2,true);
         ctx.moveTo(110,75);

         ctx.stroke();
         ctx.lineWidth = 10;

         ctx.strokeStyle = 'black';
         ctx.stroke();
  }
