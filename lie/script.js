

const realRoles = {
    c1: "Clam",   // Truth-teller
    c2: "Scallop",  // Liar
    c3: "Clam"    // Truth-teller
};
//randomize this later
  
// Submit button calls this
function submitChoices() {
    const clam1Guess = document.getElementById('clam1').value;
    const clam2Guess = document.getElementById('clam2').value;
    const clam3Guess = document.getElementById('clam3').value;

    makeGuess(clam1Guess, clam2Guess, clam3Guess);
}

// Compares the guesses to the real answers
function makeGuess(c1, c2, c3) {
    const resultElement = document.getElementById('result');

    if (c1 === realRoles.c1 && c2 === realRoles.c2 && c3 === realRoles.c3) {
        resultElement.textContent = "🎉 Correct! You figured out all the clams and scallops!";
        resultElement.style.color = "green";
    } else {
        resultElement.textContent = "❌ Not quite. Try again!";
        resultElement.style.color = "red";
    }
}



// fix this bottom

let realAssignments = {};

async function getPuzzle() {
    try {
      const response = await fetch('http://127.0.0.1:5000/generate');
      const data = await response.json();
      console.log('Puzzle:', data);
  
      // Save real answers
      realAssignments = data.assignments;
  
      // Replace statements
      const statementsDiv = document.getElementById('statements');
      statementsDiv.innerHTML = '';
      data.statements.forEach(statement => {
        const p = document.createElement('p');
        p.textContent = statement;
        statementsDiv.appendChild(p);
      });
  
      // Reset dropdowns to default
      document.getElementById('clam1').value = "Clam";
      document.getElementById('clam2').value = "Clam";
      document.getElementById('clam3').value = "Clam";
  
      // Clear result text
      document.getElementById('result').textContent = '';
  
    } catch (error) {
      console.error('Error getting puzzle:', error);
    }
  }
  

function submitChoices() {
  const amariGuess = document.getElementById('clam1').value;
  const beaGuess = document.getElementById('clam2').value;
  const claraGuess = document.getElementById('clam3').value;

  // Mapping guessess
  const userAssignments = {
    p0: amariGuess === 'Clam',
    p1: beaGuess === 'Clam',
    p2: claraGuess === 'Clam'
  };

  let correct = true;
  for (let key in realAssignments) {
    if (realAssignments[key] !== userAssignments[key]) {
      correct = false;
      break;
    }
  }

  const resultElement = document.getElementById('result');
  if (correct) {
    resultElement.textContent = "🎉 Correct!";
    resultElement.style.color = "green";
  } else {
    resultElement.textContent = "❌ Try again!";
    resultElement.style.color = "red";
  }
}

// Load puzzle when page opens
window.onload = getPuzzle;

