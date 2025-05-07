


function load_magic_square() {
    sol = {}
    hidden = []

    fetch('/magic_square')
      .then(response => response.json())
      .then(data => {

        for (const k in data.full) {
            sol[k] = data.full[k]
        }
        console.log(sol)

        for (const k of data.hidden) {
            hidden.push(k)
        }

        const container = document.getElementById('magic-square');
        container.innerHTML = '';
        for (let i = 0; i < 16; i++) {
            const cellId = 's' + i;
            const cellValue = sol[cellId];
            
            if (!(hidden.includes(cellId))) {
                //visible
                const cell = document.createElement('div');
                cell.textContent = cellValue;
                cell.classList.add('input-cell');
                container.appendChild(cell);
            } else {
                //not visible
                const input = document.createElement('input');
                input.type = 'number';
                input.min = 1;
                input.max = 16;
                input.setAttribute('data-key', cellId);
                input.className = 'input-cell';
                container.appendChild(input);
            }
            
            
        }
      });
}
  
window.onload = load_magic_square;

function check_answer() {
    const values = {};

    document.querySelectorAll('#magic-square > div').forEach((div, index) => {
        const key = 's' + index;
        const input = div.querySelector('input');
        values[key] = input ? input.value : div.textContent.trim();
    });

    fetch('/check_magic_square', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(values)
      })
    .then(res => res.json())
    .then(data => {
        const result = document.getElementById('result');
        if (!data.success) {
            result.textContent = data.message;
            result.style.color = 'orange';
        } else if (data.valid) {
            result.textContent = 'You got it!';
            result.style.color = 'green';
        } else {
            result.textContent = 'Incorrect.';
            result.textContent += data.message
            result.style.color = 'red';
        }
    });
}

