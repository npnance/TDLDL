
var scaleFactor;

var scaleToWorld = function (a, b) {
    if (a instanceof box2d.b2Vec2) {
        var newv = new box2d.b2Vec2();
        newv.x = (a.x) / scaleFactor;
        newv.y = (a.y) / scaleFactor;
        return newv;
    } else if ("undefined" != typeof b) {
        var newv = new box2d.b2Vec2();
        newv.x = (a) / scaleFactor;
        newv.y = (b) / scaleFactor;
        return newv;
    } else {
        return a / scaleFactor;
    }
};

var scaleToPixels = function (a, b) {
    if (a instanceof box2d.b2Vec2) {
        var newv = new box2d.b2Vec2();
        newv.x = a.x * scaleFactor;
        newv.y = a.y * scaleFactor;
        return newv;
    } else if ("undefined" != typeof b) {
        var newv = new box2d.b2Vec2();
        newv.x = a * scaleFactor;
        newv.y = b * scaleFactor;
        return newv;
    } else {
        return a * scaleFactor;
    }
};

var createWorld = function () {

    var worldAABB = new box2d.b2AABB();
    worldAABB.lowerBound.SetXY(-this.bounds, -this.bounds);
    worldAABB.upperBound.SetXY(this.bounds, this.bounds);
    var gravity = new box2d.b2Vec2(0, 20);
    var doSleep = true;

    scaleFactor = 10;

    return new box2d.b2World(gravity, doSleep);
};

var debugDraw = function (canvas, scale, world) {

    var context = canvas.getContext('2d');
    context.fillStyle = '#DDD';
    context.fillRect(0, 0, canvas.width, canvas.height);

    // Draw joints
    for (var j = world.m_jointList; j; j = j.m_next) {
        context.lineWidth = 0.25;
        context.strokeStyle = '#00F';
        drawJoint(context, scale, world, j);
    }

    // Draw body shapes
    for (var b = world.m_bodyList; b; b = b.m_next) {
        for (var f = b.GetFixtureList(); f !== null; f = f.GetNext()) {
            context.lineWidth = 0.5;
            context.strokeStyle = '#F00';
            drawShape(context, scale, world, b, f);
        }
    }
};

var drawJoint = function (context, scale, world, joint) {
    context.save();
    context.scale(scale, scale);
    context.lineWidth /= scale;

    var b1 = joint.m_bodyA;
    var b2 = joint.m_bodyB;
    var x1 = b1.GetPosition();
    var x2 = b2.GetPosition();
    var p1 = joint.GetAnchorA();
    var p2 = joint.GetAnchorB();

    context.beginPath();
    switch (joint.m_type) {
        case box2d.b2Joint.e_distanceJoint:
            context.moveTo(p1.x, p1.y);
            context.lineTo(p2.x, p2.y);
            break;
        default: {
            if (b1 == world.m_groundBody) {
                context.moveTo(p1.x, p1.y);
                context.lineTo(x2.x, x2.y);
            }
            else if (b2 == world.m_groundBody) {
                context.moveTo(p1.x, p1.y);
                context.lineTo(x1.x, x1.y);
            }
            else {
                context.moveTo(x1.x, x1.y);
                context.lineTo(p1.x, p1.y);
                context.lineTo(x2.x, x2.y);
                context.lineTo(p2.x, p2.y);
            }
        } break;
    }
    context.closePath();
    context.stroke();
    context.restore();
};

var drawShape = function (context, scale, world, body, fixture) {

    context.save();
    context.scale(scale, scale);

    var bPos = body.GetPosition();
    context.translate(bPos.x, bPos.y);
    context.rotate(body.GetAngleRadians());

    context.beginPath();
    context.lineWidth /= scale;

    var shape = fixture.m_shape;
    switch (shape.m_type) {
        case box2d.b2ShapeType.e_circleShape: {
            var r = shape.m_radius;
            var segments = 16.0;
            var theta = 0.0;
            var dtheta = 2.0 * Math.PI / segments;

            context.moveTo(r, 0);
            for (var i = 0; i < segments; i++) {
                context.lineTo(r + r * Math.cos(theta), r * Math.sin(theta));
                theta += dtheta;
            }
            context.lineTo(r, 0);
        } break;

        case box2d.b2ShapeType.e_polygonShape:
        case box2d.b2ShapeType.e_chainShape: {

            var vertices = shape.m_vertices;
            var vertexCount = shape.m_count;
            if (!vertexCount) return;

            context.moveTo(vertices[0].x, vertices[0].y);
            for (var i = 0; i < vertexCount; i++)
                context.lineTo(vertices[i].x, vertices[i].y);
        } break;
    }

    context.closePath();
    context.stroke();
    context.restore();
};

// The Nature of Code
// Daniel Shiffman
// http://natureofcode.com

// A boundary is a simple rectangle with x,y,width,and height

class Boundary {
    constructor(x, y, w, h) {
        this.x = x;
        this.y = y;
        this.w = w;
        this.h = h;

        let fd = new box2d.b2FixtureDef();
        fd.density = 1.0;
        fd.friction = 0.5;
        fd.restitution = 0.2;

        let bd = new box2d.b2BodyDef();

        bd.type = box2d.b2BodyType.b2_staticBody;
        bd.position.x = scaleToWorld(this.x);
        bd.position.y = scaleToWorld(this.y);
        fd.shape = new box2d.b2PolygonShape();
        fd.shape.SetAsBox(this.w / (scaleFactor * 2), this.h / (scaleFactor * 2));
        this.body = world.CreateBody(bd).CreateFixture(fd);
    }

    display() {
        fill("blue");
        stroke(0);
        rectMode(CENTER);
        rect(this.x, this.y, this.w, this.h);
    }
}

// The Nature of Code
// Daniel Shiffman
// http://natureofcode.com

// A rectangular box

class Box {
    constructor(x, y, w, h) {
        this.w = w;
        this.h = h;

        this.c = random(0, 255);

        // Define a body
        let bd = new box2d.b2BodyDef();
        bd.type = box2d.b2BodyType.b2_dynamicBody;
        bd.position = scaleToWorld(x, y);

        // Define a fixture
        let fd = new box2d.b2FixtureDef();
        // Fixture holds shape
        fd.shape = new box2d.b2PolygonShape();
        fd.shape.SetAsBox(scaleToWorld(this.w / 2), scaleToWorld(this.h / 2));

        // Some physics
        fd.density = 1.0;
        fd.friction = 0.5;
        fd.restitution = 0.2;

        // Create the body
        this.body = world.CreateBody(bd);
        // Attach the fixture
        this.body.CreateFixture(fd);

        // mySound.play();
        // Some additional stuff
        this.body.SetLinearVelocity(new box2d.b2Vec2(random(-5, 5), random(-15, 0)));
        this.body.SetAngularVelocity(random(-5, 5));
    }

    // This function removes the particle from the box2d world
    killBody() {
        world.DestroyBody(this.body);
    }

    // Is the particle ready for deletion?
    done() {
        // Let's find the screen position of the particle
        let pos = scaleToPixels(this.body.GetPosition());
        // Is it off the bottom of the screen?
        if (pos.y > height + this.w * this.h) {
            this.killBody();
            return true;
        }
        return false;
    }

    // Drawing the box
    display() {        
        let pos = scaleToPixels(this.body.GetPosition());        
        let angle = this.body.GetAngleRadians();
        
        rectMode(CENTER);
        push();
        translate(pos.x, pos.y);
        rotate(angle);
        fill(this.c);
        
        stroke("red");
        strokeWeight(2);
        
        rect(0, 0, this.w, this.h);
        pop();
    }
}

let ballX;
let ballY;
let speedX = 1;
let speedY = 1;
let mySound;
let c, cStroke;
let margin = 15;
let cSize = 5;

// A list we'll use to track fixed objects
let boundaries = [];

// A list for all of our rectangles
let boxes = [];

let world;

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
    c = color(0, random(0, 100), 100);
    cStroke = color(0, random(0, 100), random(0, 100));
}

function setup() {
    const canvasHolder = select('#canvasHolder'),
        canvasWidth = canvasHolder.width,
        canvasHeight = canvasHolder.height;

    createCanvas(canvasWidth, canvasHeight).parent('canvasHolder');

    world = createWorld();

    // listener = new JSContactListener();
    // listener.BeginContact = function (contactPtr) {
    //     var contact = Box2D.wrapPointer( contactPtr, b2Contact );
    //     var fixtureA = contact.GetFixtureA();
    //     var fixtureB = contact.GetFixtureB();
    
    // }
    
    // // Empty implementations for unused methods.
    // listener.EndContact = function() {};
    // listener.PreSolve = function() {};
    // listener.PostSolve = function() {};
    
    // world.SetContactListener( listener );

    /*
    boundaries.push(new Boundary(width / 4, height - 5, width / 2 - 50, 10));
    boundaries.push(new Boundary(3 * width / 4, height - 50, width / 2 - 50, 10));
    */

    let z = 0;
    for (var y = height / 2; y < height; y += 30) {
        let x = width / 3;

        if (z % 2 == 0) {
            x = (width / 3) * 2;
        }

        boundaries.push(new Boundary(x - (2*z), y, width / 6 + (z*8), 10))
        z++;
    }

    let b = new Box(width / 2, 30, 10, 10);
    boxes.push(b);

    //   ballX = random(30, width - 30);
    //   ballY = random(30, height - 30);

    //   changeDirection();

    //   colorMode(HSB);  
}

function bounce() {
    mySound.play();
    cSize += 5;

    changeBallColor();
}

function draw() {
    background("black");

    // We must always step through time!
    let timeStep = 1.0 / 30;

    // 2nd and 3rd arguments are velocity and position iterations
    world.Step(timeStep, 10, 10);

    // Boxes fall from the top every so often
    if (random(1) < 0.2) {
        let b = new Box(width / 2, 30, 10, 10);
        boxes.push(b);
    }

    // Display all the boundaries
    for (let i = 0; i < boundaries.length; i++) {
        boundaries[i].display();
    }

    // Display all the boxes
    for (let i = boxes.length - 1; i >= 0; i--) {
        boxes[i].display();
        if (boxes[i].done()) {
            boxes.splice(i, 1);
        }
    }
}

function drawOld() {
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