let ballX;
let ballY;
let speedX = 1;
let speedY = 1;
let mySound;
let c, cStroke;
let margin = 15;
let cSize = 5;

function preload() {
  soundFormats('mp3', 'ogg');
  mySound = loadSound("/assets/bounce.mp3");
}

function changeDirection() {
  speedX = random(2, 17) * (speedX / speedX);
  speedY = random(2, 18) * (speedY / speedY);
  changeBallColor();
}

function changeBallColor() {
  c = color(0, random(0,100), 100);
  cStroke = color(0, random(0,100), random(0,100));
}

function setup() {
  const canvasHolder = select('#canvasHolder'),
    canvasWidth = canvasHolder.width,
    canvasHeight = canvasHolder.height;

  createCanvas(canvasWidth, canvasHeight).parent('canvasHolder');

  ballX = random(30, width - 30);
  ballY = random(30, height - 30);

  changeDirection();

  colorMode(HSB);  
}

function bounce() {
  mySound.play();
  cSize += 5;

  changeBallColor();
}

function draw() {
  background("black");
  
  stroke(cStroke);
  fill(c);
 
  circle(ballX, ballY, cSize);

  let centerX = width / 2;
  let centerY = height / 2;

  if (ballX < margin || ballX > width - margin) {
    speedX *= -1;
    bounce();
  }

  if (ballY < margin || ballY > height - margin) {
    speedY *= -1;
    bounce();
  }

  ballY += speedY;
  ballX += speedX;

  //adding the vectors

  scalar = 15;

  // stroke("white")
  // strokeWeight(5)
  // line(ballX,ballY,ballX+speedX*scalar,ballY)
  // line(ballX,ballY,ballX,ballY+speedY*scalar)
  // stroke("orange")
  // line(ballX,ballY,ballX+speedX*scalar,ballY+speedY*scalar)

  drawArrow(createVector(ballX, ballY), createVector(speedX * scalar, 0), "red")
  drawArrow(createVector(ballX, ballY), createVector(0, speedY * scalar), "green")
  drawArrow(createVector(ballX, ballY), createVector(speedX * scalar, speedY * scalar), "blue")
}

function drawArrow(base, vec, myColor) {
  push();

  stroke(myColor);
  strokeWeight(3);
  fill(myColor);

  translate(base.x, base.y);
  line(0, 0, vec.x, vec.y);

  rotate(vec.heading());

  let arrowSize = 7;

  translate(vec.mag() - arrowSize, 0);
  triangle(0, arrowSize / 2, 0, -arrowSize / 2, arrowSize, 0);

  pop();
}

function mouseReleased() {
  changeDirection();
}