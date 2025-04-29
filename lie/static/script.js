
const assignments = {}

async function fetchPuzzle() {
    try {
        const response = await fetch('http://127.0.0.1:5000/generate');
        const data = await response.json();

        const statementsDiv = document.getElementById('statements');
        const clamContainer = document.getElementById('clamContainer');
        document.getElementById('result').innerHTML = '';

        statementsDiv.innerHTML = '<h2>Statements:</h2><ul>' +
            data.statements.map(s => `<li>${s}</li>`).join('') +
            '</ul>';
        
        // get the assignments
        for (const k in data.assignments) {
            assignments[k] = data.assignments[k]
        }

        let count = 0;
        clamContainer.innerHTML = '';
        for (const key in assignments) {
            const clamDiv = document.createElement('div')
            clamDiv.className = 'clam'

            const img = document.createElement('img')
            const clamImages = ['clam-pink.png', 'clam-blue.png', 'clam-purple.png', 'clam-yellow.png', 'clam-green.png']
            const clamsImage = clamImages[count]
            img.src = '/static/' + clamsImage;
            img.alt = 'Clam'
            count = count + 1;

            const nameP = document.createElement('p');
            nameP.innerText = key;

            const select = document.createElement('select')
            select.id = key; // name of the clam

            const option1 = document.createElement('option');
            option1.value = 'Clam';
            option1.innerText = 'Clam';

            const option2 = document.createElement('option');
            option2.value = 'Scallop';
            option2.innerText = 'Scallop';

            select.appendChild(option1);
            select.appendChild(option2);

            clamDiv.appendChild(img);
            clamDiv.appendChild(nameP);
            clamDiv.appendChild(select);
            clamContainer.appendChild(clamDiv);
        }

    } catch (error) {
        console.error('Error fetching puzzle:', error);
    }
}

// Submit button calls to check the guesses. 
function submitChoices() {
    let guesses = {}
    
    for (const k in assignments) {
        const guess = document.getElementById(k).value;
        if (guess == 'Clam') {
            guesses[k] = 'True';
        } else {
            guesses[k] = 'False'
        }
    }
    makeGuess(guesses);
}

// Compares the guesses to the correct assignments
function makeGuess(guesses) {
    const resultElement = document.getElementById('result');

    // console.log('assignments', assignments)
    // console.log('guesses', guesses)

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
    } else {
        resultElement.textContent = "Incorrect. Try again!";
        resultElement.style.color = "red";
    }
}

function seeSolution() {
    const assignmentsDiv = document.getElementById('assignments');

    assignmentsDiv.innerHTML = '<h2>Assignments:</h2><ul>' +
    Object.entries(assignments)
        .map(([person, value]) => `<li>${person}: ${value}</li>`)
        .join('') +
    '</ul>';
}

function hideSolution() {
    document.getElementById('assignments').innerHTML = '';
    // assignmentsDiv.innerHTML = ''

    document.getElementById('result').innerHTML = '';
}

// Call it when page loads
fetchPuzzle();