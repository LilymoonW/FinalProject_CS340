
const assignments = {}

const clamImages = {
    blue: '/static/clam-blue.png',
    pink: '/static/clam-pink.png',
    yellow: '/static/clam-yellow.png',
    green: '/static/clam-green.png',
    purple: '/static/clam-purple.png'
};

const scallopImages = {
    blue: '/static/scallop-blue.png',
    pink: '/static/scallop-pink.png',
    yellow: '/static/scallop-yellow.png',
    green: '/static/scallop-green.png',
    purple: '/static/scallop-purple.png'
};

const colors = ['blue', 'pink', 'yellow', 'green', 'purple'];

async function fetchPuzzle() {
    try {
        const response = await fetch('http://127.0.0.1:5000/generate');
        const data = await response.json();

        const statementsDiv = document.getElementById('statements');
        document.getElementById('assignments').innerHTML = '';
        document.getElementById('result').innerHTML = '';

        statementsDiv.innerHTML = '<h3>Statements:</h3><ul>' +
            data.statements.map(s => `<li>${s}</li>`).join('') +
            '</ul>';
        
        // get the assignments
        for (const k in data.assignments) {
            assignments[k] = data.assignments[k]
        }

        displayShellfish(Object.keys(assignments))
        console.log(assignments)

    } catch (error) {
        console.error('Error fetching puzzle:', error);
    }
}

function displayShellfish(names) {
    const container = document.getElementById('clamContainer');
    container.innerHTML = '';
    let count = 0;
    for (const name of names) {
        const div = document.createElement('div');
        div.className = 'clam';

        const img = document.createElement('img');
        const color = colors[count];
        count = count + 1

        img.src = clamImages[color];  // starts as a clam
        img.dataset.name = name;
        img.dataset.guess = 'clam';
        img.dataset.color = color; // color for toggling
        img.addEventListener('click', toggleShellfish);

        const label = document.createElement('div');
        label.textContent = name;

        div.appendChild(img);
        div.appendChild(label);
        container.appendChild(div);
    }
}

// Toggles between clam and scallop image
function toggleShellfish(event) {
    const img = event.target;
    const color = img.dataset.color;

    if (img.dataset.guess === 'clam') {
        img.src = scallopImages[color];
        img.dataset.guess = 'scallop';
    } else {
        img.src = clamImages[color];
        img.dataset.guess = 'clam';
    }
}

// Submit button calls to check the guesses. 
function submitChoices() {
    const container = document.getElementById('clamContainer');
    const images = container.getElementsByTagName('img');

    let guesses = {}
    
    for (const img of images) {
        const name = img.dataset.name;
        const guess = img.dataset.guess; 

        if (guess == 'clam') {
            guesses[name] = 'True';
        } else {
            guesses[name] = 'False'
        }
    }
    makeGuess(guesses);
}

// Compares the guesses to the correct assignments
function makeGuess(guesses) {
    const resultElement = document.getElementById('result');

    let correct = true;
    for (const k in assignments) {
        if (assignments[k] == 'Both') {
            continue
        }
        if (guesses[k] != assignments[k]) {
            correct = false
            break;
        }
    }
    if (correct) {
        resultElement.textContent = "Correct! You figured it out!";
        resultElement.style.color = "green";

        const bg = document.querySelector('.background-div-lie');
        bg.classList.add('successful');

        document.getElementById("successBox").style.display = "block";

        const main = document.querySelector('main');
        main.style.display = 'none';        
    } else {
        resultElement.textContent = "Incorrect. Try again!";
        resultElement.style.color = "red";

        const bg = document.querySelector('.background-div-lie');
        bg.classList.add('game-over');

        const main = document.querySelector('main');
        main.style.display = 'none';

        setTimeout(() => {
            window.location.href = '/'; // goes back to start page
        }, 2000);
    }
}

function changeToAge() {
    fetch('/next_from_lie', { method: 'POST' })
        .then(() => window.location.href = '/age');
}

function playGifAndRedirect() {
    // Hide everything
    document.querySelector('main').style.display = 'none';
    document.getElementById('successBox').style.display = 'none';

    // Swap background to GIF
    const bg = document.querySelector('.background-div-lie');
    bg.classList.add('transition-gif');

    setTimeout(() => {
        window.location.href = '/age'; // redirect to age puzzle
    }, 1500);
}

fetchPuzzle();