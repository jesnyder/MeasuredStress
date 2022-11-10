var canvases = document.getElementsByTagName('canvas');

  for( var i=0; i<canvases.length; i++){
       ctx = canvases[i].getContext('2d');

       ctx.arc(50, 50, 50, 0, 1.5*Math.PI);
       ctx.lineWidth = 15;

       ctx.strokeStyle = 'black';
       ctx.stroke();
};
