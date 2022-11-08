import Interactive from "https://vectorjs.org/interactive.js";

// Construct an interactive within the HTML element with the id "my-interactive"
let myInteractive = new Interactive("my-interactive");
myInteractive.border = true;

// Construct a control point at the the location (100, 100)
let control = myInteractive.control(100, 100);

let ellipse = interactive.ellipse( 100, 75, 80, 40);


let interactive = new Interactive('my-id',{
  width: 600,
  height: 300,
  originX: 300,
  originY: 150
});


// Print the two objects to the console
console.log( control, myInteractive);
