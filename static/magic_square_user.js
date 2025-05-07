

function setup_magic_square() {
        const n = parseInt(document.getElementById("num_squares").value);
        console.log(n)
        if (!n || n < 3 || n > 6) {
            alert("Enter a number between 3 and 5.");
            return;
        }

        document.getElementById("solution-area").style.display = "none" //close solution
        document.getElementById("result").style.display = "none"
        document.getElementById("solution-output").style.display = "none"
        const container = document.getElementById("magic-square-user");
        container.innerHTML = '';

        container.style.gridTemplateColumns = `repeat(${n}, 50px)`;
        container.style.gridTemplateRows = `repeat(${n}, 50px)`;

        for (let i = 0; i < n * n; i++) {
            const cell = document.createElement("div");
            const input = document.createElement("input");
            input.type = "number";
            input.className = "input-cell";
            input.min = 1;
            input.max = n * n;
            input.setAttribute("data-key", `s${i}`);
            cell.appendChild(input);
            container.appendChild(cell);
        }

        document.querySelectorAll("p")[0].textContent = `The sum of all rows, columns, and diagonals should equal ${n * (n * n + 1) / 2}.`;
        document.querySelectorAll("p")[1].textContent = `All values are distinct, and each must be between 1 and ${n * n}.`;
}


async function check_valid_puzzle() {
    const inputs = document.querySelectorAll('#magic-square-user input');
    const values = {};

    const spinner = document.getElementById("spinner");
    const result = document.getElementById("result");
    result.style.display = "block"
    document.getElementById("solution-area").style.display = "none"
    document.getElementById("solution-output").style.display = "none"
    spinner.style.display = "block";
    result.innerText = "";

    inputs.forEach(input => {
        const key = input.getAttribute('data-key');
        const value = input.value.trim();
        values[key] = value === "" ? null : parseInt(value); // null if empty
    });

    const response = await fetch('/check_gen_ms', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(values)
    });

    const data = await response.json();
    spinner.style.display = "none";

    if (!data.success) {
        result.textContent = data.message;
        result.style.color = 'orange';
    } else if (data.valid) {
        result.textContent = 'That is a valid magic square!';
        result.style.color = 'green';

        window.magicModel = data.model
        document.getElementById("solution-area").style.display = "block"
    } else {
        result.textContent = 'That\'s not a valid magic square.';
        result.style.color = 'red';
    }
}

function show_solution() {
    const output = document.getElementById("solution-output")
    output.style.display = "block"
    if (window.magicModel) {
        let text = JSON.stringify(window.magicModel);
        text = text.replace(/\\n/g, ' ');
        text = text.replace(/[\[\]"]/g, '') 

        // to sort by index
        let pairs = text.split(',').map(p => p.trim()).filter(p => p);

        // Sort by numeric index in sX
        pairs.sort((a, b) => {
            const aIndex = parseInt(a.match(/s(\d+)/)[1]);
            const bIndex = parseInt(b.match(/s(\d+)/)[1]);
            return aIndex - bIndex;
        });

        const values = pairs.map(p => p.split('=')[1].trim());
        const n = Math.sqrt(values.length);

        // Build a grid string
        let gridText = '';
        for (let i = 0; i < n; i++) {
            gridText += values.slice(i * n, (i + 1) * n).join('\t') + '\n';
        }
        output.innerText = gridText.trim();

    } else {
        output.innerText = "⚠️ No solution available.";
    }
}

