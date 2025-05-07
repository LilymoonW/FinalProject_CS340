

function setup_magic_square() {
        const n = parseInt(document.getElementById("num_squares").value);
        console.log(n)
        if (!n || n < 3 || n > 6) {
            alert("Enter a number between 3 and 5.");
            return;
        }

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
        result.textContent += data.model
        result.style.color = 'green';
    } else {
        result.textContent = 'That\'s not a valid magic square.';
        result.style.color = 'red';
    }
}

