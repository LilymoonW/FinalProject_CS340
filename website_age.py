# Authored By Lilymoon Whalen
from flask import Flask, jsonify, render_template, session, request
from z3 import *
import random

app = Flask(__name__, template_folder='website')
app.secret_key = 'super-secret-key'  # Required for session storage


# === Route 1: Age Riddle ===
@app.route('/solve')
def solve():
    result = solve_random_age_riddle()
    return jsonify(result)

def solve_random_age_riddle():
    age1 = Int('age1')
    age2 = Int('age2')
    age3 = Int('age3')

    while True:
        solver = Solver()
        random_product = random.randint(1, 100)
        random_sum = random.randint(3, 50)

        solver.add(age1 > 0, age2 > 0, age3 > 0)
        solver.add(age1 * age2 * age3 == random_product)
        solver.add(age1 + age2 + age3 == random_sum)

        if solver.check() == sat:
            model = solver.model()
            return {
                "product": random_product,
                "sum": random_sum,
                "ages": [model[age1].as_long(), model[age2].as_long(), model[age3].as_long()]
            }


# === Route 2: Mismatched Boxes Setup ===
@app.route('/mismatched')
def mismatched():
    contents = ['Pink Pearls', 'White Pearls', 'Mixed Pearls']
    labels = ['Pink Pearls', 'White Pearls', 'Mixed Pearls']

    box1, box2, box3 = Ints('box1 box2 box3')
    s = Solver()
    s.add(Distinct(box1, box2, box3))
    s.add(And(box1 >= 0, box1 <= 2))
    s.add(And(box2 >= 0, box2 <= 2))
    s.add(And(box3 >= 0, box3 <= 2))

    random_labels = random.sample(range(3), 3)
    s.add(box1 != random_labels[0])
    s.add(box2 != random_labels[1])
    s.add(box3 != random_labels[2])

    if s.check() == sat:
        m = s.model()
        box_assignments = [m[box1].as_long(), m[box2].as_long(), m[box3].as_long()]
        session['true_contents'] = box_assignments
        session['labels'] = random_labels

        return jsonify([
            {"box": i + 1, "label": labels[random_labels[i]]}
            for i in range(3)
        ])
    else:
        return jsonify({"error": "No solution"}), 500


# === Route 3: Peek into a box ===
@app.route('/peek/<int:box_id>')
def peek_box(box_id):
    contents = ['Pink Pearls', 'White Pearls', 'Mixed Pearls']
    true_contents = session.get('true_contents', [None, None, None])

    if 1 <= box_id <= 3 and true_contents[box_id - 1] is not None:
        actual = true_contents[box_id - 1]
        return jsonify({"box": box_id, "actual": contents[actual]})
    return jsonify({"error": "Invalid box ID"}), 400


# === Route 4: Submit guesses ===
@app.route('/submit-guess', methods=['POST'])
def submit_guess():
    contents = ['Pink Pearls', 'White Pearls', 'Mixed Pearls']
    true_contents = session.get('true_contents', [])
    guess = request.json.get('guess', [])

    if not guess or len(guess) != 3 or not true_contents:
        return jsonify({"result": "invalid", "correct": False})

    correct = all(contents[true_contents[i]] == guess[i] for i in range(3))
    return jsonify({"result": "submitted", "correct": correct})


# === Route 5: Home (start game) ===
@app.route('/')
def home():
    return render_template('age.html')


if __name__ == '__main__':
    app.run(debug=True)
