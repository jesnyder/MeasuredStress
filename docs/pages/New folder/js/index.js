function draw()
{
  var canvas = document.getElementById('canvas');
  if (canvas.getContext)
  {
    var context = canvas.getContext('2d');

    context.beginPath();
    context.moveTo(5,75);
    context.lineTo(10,105);
    context.lineTo(20,25);
    context.fill();
  }


}
