// Program constants
/** The preset link to the server */
const serverLink = "https://rollenbollen.azurewebsites.net/";
/** The preset link to the api on the server */
const apiLink = serverLink + "api/";
const MIN_SPEED = 5.0;
const minSpeedSq = MIN_SPEED ** 2;

const floorPlan = [
  [
    { n: 0, ne: 0, e: 0, se: 0, s: 0, sw: 0, w: 0, nw: 0 },
    { n: 0, ne: 0, e: 0, se: 0, s: 0, sw: 0, w: 0, nw: 0 },
    { n: 0, ne: 0, e: 0, se: 0, s: 0, sw: 0, w: 0, nw: 0 },
    { n: 0, ne: 0, e: 0, se: 0, s: 0, sw: 0, w: 0, nw: 0 },
  ],
  [
    { n: 0, ne: 0, e: 0, se: 0, s: 0, sw: 0, w: 0, nw: 0 },
    { n: 0, ne: 0, e: 0, se: 0, s: 0, sw: 0, w: 0, nw: 0 },
    { n: 0, ne: 0, e: 0, se: 0, s: 0, sw: 0, w: 0, nw: 0 },
    { n: 0, ne: 0, e: 0, se: 0, s: 0, sw: 0, w: 0, nw: 0 },
  ],
  [
    { n: 0, ne: 0, e: 0, se: 0, s: 0, sw: 0, w: 0, nw: 0 },
    { n: 0, ne: 0, e: 0, se: 0, s: 0, sw: 0, w: 0, nw: 0 },
    { n: 0, ne: 0, e: 0, se: 0, s: 0, sw: 0, w: 0, nw: 0 },
    { n: 0, ne: 0, e: 0, se: 0, s: 0, sw: 0, w: 0, nw: 0 },
  ],
  [
    { n: 0, ne: 0, e: 0, se: 0, s: 0, sw: 0, w: 0, nw: 0 },
    { n: 0, ne: 0, e: 0, se: 0, s: 0, sw: 0, w: 0, nw: 0 },
    { n: 0, ne: 0, e: 0, se: 0, s: 0, sw: 0, w: 0, nw: 0 },
    { n: 0, ne: 0, e: 0, se: 0, s: 0, sw: 0, w: 0, nw: 0 },
  ],
];
const speedOffset = 1;
registerMatrixAnimation({
  frames: [
    [
      [1, 1, 11, 11, 1, 1, 1, 1],
      [1, 11, 1, 11, 1, 1, 1, 1],
      [11, 1, 1, 11, 1, 1, 1, 1],
      [1, 1, 1, 11, 1, 1, 1, 1],
      [1, 1, 1, 11, 1, 1, 1, 1],
      [1, 1, 1, 11, 1, 1, 1, 1],
      [1, 1, 1, 11, 1, 1, 1, 1],
      [1, 1, 1, 11, 1, 1, 1, 1],
    ],
  ],
  palette: [
    { r: 255, g: 255, b: 255 },
    { r: 0, g: 0, b: 0 },
    { r: 255, g: 0, b: 0 },
    { r: 255, g: 64, b: 0 },
    { r: 255, g: 128, b: 0 },
    { r: 255, g: 191, b: 0 },
    { r: 255, g: 255, b: 0 },
    { r: 185, g: 246, b: 30 },
    { r: 0, g: 255, b: 0 },
    { r: 185, g: 255, b: 255 },
    { r: 0, g: 255, b: 255 },
    { r: 0, g: 0, b: 255 },
    { r: 145, g: 0, b: 211 },
    { r: 157, g: 48, b: 118 },
    { r: 255, g: 0, b: 255 },
    { r: 204, g: 27, b: 126 },
  ],
  fps: 10,
  transition: MatrixAnimationTransition.None,
});
registerMatrixAnimation({
  frames: [
    [
      [1, 1, 11, 11, 11, 11, 1, 1],
      [1, 11, 1, 1, 1, 11, 1, 1],
      [1, 11, 1, 1, 11, 1, 1, 1],
      [1, 1, 1, 11, 1, 1, 1, 1],
      [1, 1, 11, 1, 1, 1, 1, 1],
      [1, 11, 1, 1, 1, 1, 1, 1],
      [1, 11, 1, 1, 1, 1, 1, 1],
      [1, 11, 11, 11, 11, 11, 11, 1],
    ],
  ],
  palette: [
    { r: 255, g: 255, b: 255 },
    { r: 0, g: 0, b: 0 },
    { r: 255, g: 0, b: 0 },
    { r: 255, g: 64, b: 0 },
    { r: 255, g: 128, b: 0 },
    { r: 255, g: 191, b: 0 },
    { r: 255, g: 255, b: 0 },
    { r: 185, g: 246, b: 30 },
    { r: 0, g: 255, b: 0 },
    { r: 185, g: 255, b: 255 },
    { r: 0, g: 255, b: 255 },
    { r: 0, g: 0, b: 255 },
    { r: 145, g: 0, b: 211 },
    { r: 157, g: 48, b: 118 },
    { r: 255, g: 0, b: 255 },
    { r: 204, g: 27, b: 126 },
  ],
  fps: 10,
  transition: MatrixAnimationTransition.None,
});
registerMatrixAnimation({
  frames: [
    [
      [1, 1, 11, 11, 11, 11, 1, 1],
      [1, 1, 1, 1, 1, 11, 1, 1],
      [1, 1, 1, 1, 1, 11, 1, 1],
      [1, 1, 11, 11, 11, 11, 1, 1],
      [1, 1, 1, 1, 1, 11, 1, 1],
      [1, 1, 1, 1, 1, 11, 1, 1],
      [1, 1, 1, 1, 1, 11, 1, 1],
      [1, 1, 11, 11, 11, 11, 1, 1],
    ],
  ],
  palette: [
    { r: 255, g: 255, b: 255 },
    { r: 0, g: 0, b: 0 },
    { r: 255, g: 0, b: 0 },
    { r: 255, g: 64, b: 0 },
    { r: 255, g: 128, b: 0 },
    { r: 255, g: 191, b: 0 },
    { r: 255, g: 255, b: 0 },
    { r: 185, g: 246, b: 30 },
    { r: 0, g: 255, b: 0 },
    { r: 185, g: 255, b: 255 },
    { r: 0, g: 255, b: 255 },
    { r: 0, g: 0, b: 255 },
    { r: 145, g: 0, b: 211 },
    { r: 157, g: 48, b: 118 },
    { r: 255, g: 0, b: 255 },
    { r: 204, g: 27, b: 126 },
  ],
  fps: 10,
  transition: MatrixAnimationTransition.None,
});
registerMatrixAnimation({
  frames: [
    [
      [1, 1, 1, 1, 11, 1, 1, 1],
      [1, 1, 1, 11, 11, 1, 1, 1],
      [1, 1, 11, 1, 11, 1, 1, 1],
      [1, 11, 11, 11, 11, 11, 11, 1],
      [1, 1, 1, 1, 11, 1, 1, 1],
      [1, 1, 1, 1, 11, 1, 1, 1],
      [1, 1, 1, 1, 11, 1, 1, 1],
      [1, 1, 1, 1, 11, 1, 1, 1],
    ],
  ],
  palette: [
    { r: 255, g: 255, b: 255 },
    { r: 0, g: 0, b: 0 },
    { r: 255, g: 0, b: 0 },
    { r: 255, g: 64, b: 0 },
    { r: 255, g: 128, b: 0 },
    { r: 255, g: 191, b: 0 },
    { r: 255, g: 255, b: 0 },
    { r: 185, g: 246, b: 30 },
    { r: 0, g: 255, b: 0 },
    { r: 185, g: 255, b: 255 },
    { r: 0, g: 255, b: 255 },
    { r: 0, g: 0, b: 255 },
    { r: 145, g: 0, b: 211 },
    { r: 157, g: 48, b: 118 },
    { r: 255, g: 0, b: 255 },
    { r: 204, g: 27, b: 126 },
  ],
  fps: 10,
  transition: MatrixAnimationTransition.None,
});
registerMatrixAnimation({
  frames: [
    [
      [1, 11, 11, 11, 11, 11, 1, 1],
      [1, 11, 1, 1, 1, 1, 1, 1],
      [1, 11, 1, 1, 1, 1, 1, 1],
      [1, 11, 11, 11, 11, 11, 1, 1],
      [1, 1, 1, 1, 1, 11, 1, 1],
      [1, 1, 1, 1, 1, 11, 1, 1],
      [1, 1, 1, 1, 1, 11, 1, 1],
      [1, 11, 11, 11, 11, 11, 1, 1],
    ],
  ],
  palette: [
    { r: 255, g: 255, b: 255 },
    { r: 0, g: 0, b: 0 },
    { r: 255, g: 0, b: 0 },
    { r: 255, g: 64, b: 0 },
    { r: 255, g: 128, b: 0 },
    { r: 255, g: 191, b: 0 },
    { r: 255, g: 255, b: 0 },
    { r: 185, g: 246, b: 30 },
    { r: 0, g: 255, b: 0 },
    { r: 185, g: 255, b: 255 },
    { r: 0, g: 255, b: 255 },
    { r: 0, g: 0, b: 255 },
    { r: 145, g: 0, b: 211 },
    { r: 157, g: 48, b: 118 },
    { r: 255, g: 0, b: 255 },
    { r: 204, g: 27, b: 126 },
  ],
  fps: 10,
  transition: MatrixAnimationTransition.None,
});
registerMatrixAnimation({
  frames: [
    [
      [1, 11, 11, 11, 11, 11, 1, 1],
      [1, 11, 1, 1, 1, 1, 1, 1],
      [1, 11, 1, 1, 1, 1, 1, 1],
      [1, 11, 1, 1, 1, 1, 1, 1],
      [1, 11, 11, 11, 11, 11, 1, 1],
      [1, 11, 1, 1, 1, 11, 1, 1],
      [1, 11, 1, 1, 1, 11, 1, 1],
      [1, 11, 11, 11, 11, 11, 1, 1],
    ],
  ],
  palette: [
    { r: 255, g: 255, b: 255 },
    { r: 0, g: 0, b: 0 },
    { r: 255, g: 0, b: 0 },
    { r: 255, g: 64, b: 0 },
    { r: 255, g: 128, b: 0 },
    { r: 255, g: 191, b: 0 },
    { r: 255, g: 255, b: 0 },
    { r: 185, g: 246, b: 30 },
    { r: 0, g: 255, b: 0 },
    { r: 185, g: 255, b: 255 },
    { r: 0, g: 255, b: 255 },
    { r: 0, g: 0, b: 255 },
    { r: 145, g: 0, b: 211 },
    { r: 157, g: 48, b: 118 },
    { r: 255, g: 0, b: 255 },
    { r: 204, g: 27, b: 126 },
  ],
  fps: 10,
  transition: MatrixAnimationTransition.None,
});
registerMatrixAnimation({
  frames: [
    [
      [1, 1, 11, 11, 11, 11, 1, 1],
      [1, 1, 1, 1, 1, 11, 1, 1],
      [1, 1, 1, 1, 1, 11, 1, 1],
      [1, 1, 1, 1, 1, 11, 1, 1],
      [1, 1, 1, 1, 1, 11, 1, 1],
      [1, 1, 1, 1, 1, 11, 1, 1],
      [1, 1, 1, 1, 1, 11, 1, 1],
      [1, 1, 1, 1, 1, 11, 1, 1],
    ],
  ],
  palette: [
    { r: 255, g: 255, b: 255 },
    { r: 0, g: 0, b: 0 },
    { r: 255, g: 0, b: 0 },
    { r: 255, g: 64, b: 0 },
    { r: 255, g: 128, b: 0 },
    { r: 255, g: 191, b: 0 },
    { r: 255, g: 255, b: 0 },
    { r: 185, g: 246, b: 30 },
    { r: 0, g: 255, b: 0 },
    { r: 185, g: 255, b: 255 },
    { r: 0, g: 255, b: 255 },
    { r: 0, g: 0, b: 255 },
    { r: 145, g: 0, b: 211 },
    { r: 157, g: 48, b: 118 },
    { r: 255, g: 0, b: 255 },
    { r: 204, g: 27, b: 126 },
  ],
  fps: 10,
  transition: MatrixAnimationTransition.None,
});
registerMatrixAnimation({
  frames: [
    [
      [1, 1, 11, 11, 11, 11, 1, 1],
      [1, 11, 1, 1, 1, 1, 11, 1],
      [1, 11, 1, 1, 1, 1, 11, 1],
      [1, 11, 11, 11, 11, 11, 11, 1],
      [1, 11, 1, 1, 1, 1, 11, 1],
      [1, 11, 1, 1, 1, 1, 11, 1],
      [1, 11, 1, 1, 1, 1, 11, 1],
      [1, 1, 11, 11, 11, 11, 1, 1],
    ],
  ],
  palette: [
    { r: 255, g: 255, b: 255 },
    { r: 0, g: 0, b: 0 },
    { r: 255, g: 0, b: 0 },
    { r: 255, g: 64, b: 0 },
    { r: 255, g: 128, b: 0 },
    { r: 255, g: 191, b: 0 },
    { r: 255, g: 255, b: 0 },
    { r: 185, g: 246, b: 30 },
    { r: 0, g: 255, b: 0 },
    { r: 185, g: 255, b: 255 },
    { r: 0, g: 255, b: 255 },
    { r: 0, g: 0, b: 255 },
    { r: 145, g: 0, b: 211 },
    { r: 157, g: 48, b: 118 },
    { r: 255, g: 0, b: 255 },
    { r: 204, g: 27, b: 126 },
  ],
  fps: 10,
  transition: MatrixAnimationTransition.None,
});
registerMatrixAnimation({
  frames: [
    [
      [1, 1, 11, 11, 11, 11, 1, 1],
      [1, 11, 1, 1, 1, 1, 11, 1],
      [1, 11, 1, 1, 1, 1, 11, 1],
      [1, 1, 11, 11, 11, 11, 11, 1],
      [1, 1, 1, 1, 1, 1, 11, 1],
      [1, 1, 1, 1, 1, 1, 11, 1],
      [1, 1, 1, 1, 1, 1, 11, 1],
      [1, 11, 11, 11, 11, 11, 1, 1],
    ],
  ],
  palette: [
    { r: 255, g: 255, b: 255 },
    { r: 0, g: 0, b: 0 },
    { r: 255, g: 0, b: 0 },
    { r: 255, g: 64, b: 0 },
    { r: 255, g: 128, b: 0 },
    { r: 255, g: 191, b: 0 },
    { r: 255, g: 255, b: 0 },
    { r: 185, g: 246, b: 30 },
    { r: 0, g: 255, b: 0 },
    { r: 185, g: 255, b: 255 },
    { r: 0, g: 255, b: 255 },
    { r: 0, g: 0, b: 255 },
    { r: 145, g: 0, b: 211 },
    { r: 157, g: 48, b: 118 },
    { r: 255, g: 0, b: 255 },
    { r: 204, g: 27, b: 126 },
  ],
  fps: 10,
  transition: MatrixAnimationTransition.None,
});
// User functions
/**
 * calculate angle which the BOLT has to turn
 * @param {int} opposite The opposite side of the triangle.
 * @param {int} adjacent The adjacent side of the triangle.
 * @return {int} The precise angle which the BOLT has to turn
 */
function calcAngle(opposite, adjacent) {
  if (0 == adjacent) {
    if (opposite > 0) {
      return 90;
    } else {
      return 270;
    }
  }
  let angle = Math.atan(opposite / adjacent) / (Math.PI / 180);
  if (opposite < 0) {
    angle += 360;
  }
  if (adjacent < 0) {
    angle += 180;
  }
  angle = angle % 360;
  return angle;
}
/**
 * calculate the distance between two points, in a 2D plain.
 * @param {int} opposite The opposite side of the triangle.
 * @param {int} adjacent The adjacent side of the triangle.
 * @return {int} total distance via the pythagorean theorem.
 */
function calcDistance(opposite, adjacent) {
  return Math.sqrt(opposite ** 2 + adjacent ** 2);
}
const boltIdLink = () => apiLink + "bolt/" + boltId + "/";

// User classes
/**
 * The Sphero BOLT with all it's data
 */
class Bolt {
  /**
   * Create a Sphero object
   */
  constructor() {
    this.position = {
      x: 0,
      y: 0,
    };
  }
  /**
   * Check if a move is possible
   * @return {boolean}, it's possible or it isn't
   */
  possibleMoves() {
    return floorPlan[this.position.y][this.position.x];
  }
  /**
   * Drive the BOLT to the given point in space from the current space.
   * @param {int} x The _x_ position in a 2D field.
   * @param {int} y The _y_ position in a 2D field.
   */
  async drive(x, y) {
    const dx = x - this.position.x;
    const dy = y - this.position.y;
    const angle = calcAngle(dx, dy);
    const distance = calcDistance(dx, dy);

    await this.roll(angle, distance);
    this.position.x = x;
    this.position.y = y;
  }

  /**
   * Roll the bolt a certain distance at the given angle.
   * @param {int} angle The angle the BOLT has to turn.
   * @param {int} distance The distance the BOLT has to roll.
   */
  async roll(angle, distance) {
    await roll(angle, 45 * speedOffset, (2 * distance) / speedOffset);
    await delay(1);
  }
}
// Program variables
/** This var will keep a record of the id of the BOLT */
var boltId = -1;
let running = true;
const bolt = new Bolt();
// main function
/**
 * This is the main function withing Sphero Edu
 */
async function startProgram() {
  await registerBolt();
  playMatrixAnimation(boltId - 1);
  while (running) {
    await getNextMove();
    await delay(0.1);
  }
  exitProgram();
}

// async user function
/**
 * Make a call to the register API interface
 */
async function registerBolt() {
  const response = await fetch(apiLink + "register");
  const id = await response.json();
  boltId = id;
  await speak("Bolt id is " + boltId);
}
/**
 * Make a call to the web-API for the next move
 */
async function getNextMove() {
  const response = await fetch(boltIdLink() + "command");
  const move = await response.json();
  const x = move.x;
  const y = move.y;
  await bolt.drive(x, y);
  if (-1 == x && -1 == y) {
    running = false;
  }
}

// Register events
registerEvent(EventType.onCollision, async () => {
  await speak("Oof!");
});
