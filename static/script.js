// --- Game State ---
let leftBank = ["student", "fox", "goose", "lettuce"];
let rightBank = [];
let boat = [];
let boatOnLeft = true; // true = boat on left side
function allowDrop(ev) {
  ev.preventDefault();
}

function drag(ev) {
  ev.dataTransfer.setData("text", ev.target.id);
}

function dropIntoBoat(ev) {
  ev.preventDefault();
  const data = ev.dataTransfer.getData("text");
  const item = document.getElementById(data);

  if (boat.length <= 2) { // Max 2 items in the boat
    document.getElementById("boat").appendChild(item);
    boat.push(data);
    leftBank = leftBank.filter(x => x !== data);
    rightBank = rightBank.filter(x => x !== data);
  }
}

function dropOntoBank(ev) {
  ev.preventDefault();
  const data = ev.dataTransfer.getData("text");
  const item = document.getElementById(data);
  
  if (boat.includes(data)) {
    if (boatOnLeft) {
      document.getElementById("left-bank").appendChild(item);
      leftBank.push(data);
    } else {
      document.getElementById("right-bank").appendChild(item);
      rightBank.push(data);
    }
    boat = boat.filter(x => x !== data);
  }
}
function moveBoat() {
  const boatDiv = document.getElementById("boat");

  if (!boat.includes("student")) {
    document.getElementById("message").textContent = "You can't move the boat without the Student!";
    setTimeout(() => {
      document.getElementById("message").textContent = "";
    }, 2000);
    return;
  }
  if (boatOnLeft) {
    boatDiv.style.left = "80%"; 
  } else {
    boatDiv.style.left = "5%"; 
  }

  boatOnLeft = !boatOnLeft;

  setTimeout(() => {
  
    boat.forEach(itemName => {
      const item = document.getElementById(itemName);
      if (boatOnLeft) {
        document.getElementById("left-bank").appendChild(item);
        leftBank.push(itemName);
      } else {
        document.getElementById("right-bank").appendChild(item);
        rightBank.push(itemName);
      }
    });
  
    boat = []; 
    checkRules();
  }, 500);
  
}
function resetGame() {
  window.location.reload();
}
document.querySelectorAll('.item').forEach(item => {
  item.addEventListener("dragstart", drag);
});

document.getElementById("boat").addEventListener("dragover", allowDrop);
document.getElementById("boat").addEventListener("drop", dropIntoBoat);
document.getElementById("left-bank").addEventListener("dragover", allowDrop);
document.getElementById("left-bank").addEventListener("drop", dropOntoBank);
document.getElementById("right-bank").addEventListener("dragover", allowDrop);
document.getElementById("right-bank").addEventListener("drop", dropOntoBank);



function checkRules() {
  const left = new Set(leftBank);
  const right = new Set(rightBank);
  const dangerZone = boatOnLeft ? right : left;

  if (dangerZone.has("fox") && dangerZone.has("goose")) {
    showWarning("Oh no! You left the fox and the goose alone. The fox ate the goose!");
    return;
  }

  if (dangerZone.has("goose") && dangerZone.has("lettuce")) {
    showWarning("Oh no! You left the goose and the lettuce alone. The goose ate the lettuce!");
    return;
  }
  if (rightBank.includes("student") &&
      rightBank.includes("fox") &&
      rightBank.includes("goose") &&
      rightBank.includes("lettuce")) {
    document.getElementById("message").textContent = "You safely crossed Lake Waban! Alexa is proud of you.";
  }
}

function showWarning(text) {
  const message = document.getElementById("message");
  message.textContent = text;
  message.style.color = "red";
  setTimeout(() => {
    message.textContent = "";
    message.style.color = "black";
    resetGame();
  }, 3000);
}
