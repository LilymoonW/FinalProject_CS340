# Authored By Lilymoon Whalen 
from flask import Flask, jsonify
from z3 import *
import random

app = Flask(__name__, template_folder='website')


def solve_random_age_riddle():
    age1 = Int('age1')
    age2 = Int('age2')
    age3 = Int('age3')
    solver = Solver()

    while True:  # Keep trying until we find a SAT solution
        random_product = random.randint(1, 100)
        random_sum = random.randint(3, 50)

        solver.push()
        solver.add(age1 > 0, age2 > 0, age3 > 0)
        solver.add(age1 * age2 * age3 == random_product)
        solver.add(age1 + age2 + age3 == random_sum)

        if solver.check() == sat:
            model = solver.model()
            result = {
                "product": random_product,
                "sum": random_sum,
                "ages": [model[age1].as_long(), model[age2].as_long(), model[age3].as_long()]
            }
            solver.pop()  # Clean up
            return result
        else:
            solver.pop()  # No solution, undo and try again


@app.route('/solve')
def solve():
    result = solve_random_age_riddle()
    return jsonify(result)

from flask import render_template

@app.route('/')
def home():
    return render_template('age.html')


if __name__ == '__main__':
    app.run(debug=True)
    