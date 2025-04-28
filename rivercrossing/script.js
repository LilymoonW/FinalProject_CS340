let solutionStates = []; // Will store the states from the XML
let currentStep = 0;

// Mapping Alloy names to your frontend names
const nameMapping = {
  "wolf": "fox",
  "goat": "goose",
  "cabbage": "lettuce",
  "farmer": "farmer"
};

fetch('solution.xml')
  .then(response => response.text())
  .then(str => (new window.DOMParser()).parseFromString(str, "application/xml"))
  .then(data => {
    const instances = data.getElementsByTagName('instance');

    for (let instance of instances) {
      let thisSide = [];
      let otherSide = [];

      const thisSideSig = instance.querySelector('sig[label="this/ThisSide"]');
      const otherSideSig = instance.querySelector('sig[label="this/OtherSide"]');

      if (thisSideSig) {
        const atoms = thisSideSig.getElementsByTagName('atom');
        for (let atom of atoms) {
          let rawName = atom.getAttribute('label').toLowerCase().replace('$0', '');
          let mappedName = nameMapping[rawName] || rawName; // Map if needed
          thisSide.push(mappedName);
        }
      }

      if (otherSideSig) {
        const atoms = otherSideSig.getElementsByTagName('atom');
        for (let atom of atoms) {
          let rawName = atom.getAttribute('label').toLowerCase().replace('$0', '');
          let mappedName = nameMapping[rawName] || rawName;
          otherSide.push(mappedName);
        }
      }

      solutionStates.push({ thisSide, otherSide });
    }

    console.log(solutionStates); // You can see what was loaded
  });


// Game state
let leftBank = ["Farmer", "Fox", "Goose", "Lettuce"];
let boat = [];
let rightBank = [];
let boatOnLeft = true;  // true = boat on left side

function moveBoat() {
      // ❗ Check if Farmer is inside the boat
    if (!boat.includes("farmer")) {
        document.getElementById("message").textContent = "You can't move the boat without the Farmer!";
            // Automatically clear the message after 2 seconds
        setTimeout(() => {
            message.textContent = "";
        }, 2000);
        return; // Stop the function
    }
    const boatDiv = document.getElementById("boat");
  
    // Animate boat move
    if (boatOnLeft) {
      boatDiv.style.left = "80%"; // Move to right bank
    } else {
      boatDiv.style.left = "5%";  // Move to left bank
    }
    boatOnLeft = !boatOnLeft;
  
    setTimeout(() => {
      // Drop all items off boat onto the correct bank
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
      boat = []; // Boat becomes empty
      checkSolution();

    }, 500); // wait for boat animation to finish
  }
  
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
    
    if (boat.length < 2) {  // Limit: max 2 items
      document.getElementById("boat").appendChild(item);
      boat.push(data);
  
      // Remove from banks
      leftBank = leftBank.filter(x => x !== data);
      rightBank = rightBank.filter(x => x !== data);
    }
  }
  

function updateBanks() {
  const left = document.getElementById("left-bank");
  const right = document.getElementById("right-bank");
  const boatDiv = document.getElementById("boat");

  // Clear banks
  left.innerHTML = "";
  right.innerHTML = "";

  // Recreate Farmer (he's always with the boat)
  const farmer = document.createElement("div");
  farmer.className = "item";
  farmer.draggable = false;
  const farmerImg = document.createElement("img");
  farmerImg.src = "assets/farmer.png";
  farmer.appendChild(farmerImg);

  // Show items
  leftBank.forEach(name => {
    const div = document.createElement("div");
    div.className = "item";
    div.id = name;
    div.draggable = true;
    div.addEventListener("dragstart", drag);
    const img = document.createElement("img");
    img.src = `assets/${name.toLowerCase()}.png`;
    div.appendChild(img);
    left.appendChild(div);
  });

  rightBank.forEach(name => {
    const div = document.createElement("div");
    div.className = "item";
    div.id = name;
    div.draggable = true;
    div.addEventListener("dragstart", drag);
    const img = document.createElement("img");
    img.src = `assets/${name.toLowerCase()}.png`;
    div.appendChild(img);
    right.appendChild(div);
  });

  // Always add farmer back into boat
  boatDiv.innerHTML = "";
  boatDiv.appendChild(farmerImg);
}

// Set up drag and drop listeners
document.querySelectorAll('.item').forEach(item => {
  item.addEventListener("dragstart", drag);
});

document.getElementById("boat").addEventListener("dragover", allowDrop);
document.getElementById("boat").addEventListener("drop", drop);

function checkSolution() {
    if (currentStep >= solutionStates.length) {
      console.log("No more solution steps to check.");
      return;
    }
  
    const expectedState = solutionStates[currentStep];
    
    // Compare leftBank and expectedState.thisSide
    const leftMatch = arraysEqual(new Set(leftBank), new Set(expectedState.thisSide));
    const rightMatch = arraysEqual(new Set(rightBank), new Set(expectedState.otherSide));
  
    if (leftMatch && rightMatch) {
      console.log("Correct move!");
      currentStep++; // Move to next expected step
      document.getElementById("message").textContent = "Good move!";
      setTimeout(() => {
        document.getElementById("message").textContent = "";
      }, 1500);
    } else {
      console.log("Invalid move!");
      document.getElementById("message").textContent = "That's not the correct move!";
      setTimeout(() => {
        document.getElementById("message").textContent = "";
      }, 2000);
    }
  }
  
  // Helper to compare sets (unordered)
  function arraysEqual(a, b) {
    if (a.size !== b.size) return false;
    for (let item of a) if (!b.has(item)) return false;
    return true;
  }

  function resetGame() {
    // Reset all game state
    leftBank = ["farmer", "fox", "goose", "lettuce"];
    boat = [];
    rightBank = [];
    boatOnLeft = true;
    currentStep = 0;
  
    // Reset boat position
    const boatDiv = document.getElementById("boat");
    boatDiv.style.left = "5%";
  
    // Clear message
    document.getElementById("message").textContent = "";
  
    // Reset the banks visually
    const left = document.getElementById("left-bank");
    const right = document.getElementById("right-bank");
    const boatArea = document.getElementById("boat");
  
    left.innerHTML = "";
    right.innerHTML = "";
    boatArea.innerHTML = '<img src="assets/boat.png" alt="Boat">'; // Reset boat image
  
    // Put all items back on the left bank
    ["farmer", "fox", "goose", "lettuce"].forEach(name => {
      const div = document.createElement("div");
      div.className = "item";
      div.id = name;
      div.draggable = true;
      div.addEventListener("dragstart", drag);
  
      const img = document.createElement("img");
      img.src = `assets/${name.toLowerCase()}.png`;
      div.appendChild(img);
  
      left.appendChild(div);
    });
  }
  
  