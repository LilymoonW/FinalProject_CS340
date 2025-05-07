# Authored By Lilymoon Whalen
from flask import Flask, jsonify, render_template, session, request
from z3 import *
import random
import math

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



# === Lie Puzzle ===
# === Route 5: generate lie puzzles===
@app.route('/generate')
def generate():
    n = random.randint(3,5)
    result = generate_instances(n)
    return jsonify(result)

# n = number of people
def generate_instances(n):
    s = Solver()

    bools = []
    for i in range(n):
        name = "Shellfish" + str(i)
        bools.append(Bool(name))

    statements = []

    # number of statements is n
    for i in range(n):
        person1 = random.choice(bools)
        person2 = random.choice(bools)

        says_is_knave = random.choice([True, False])

        # if person 1 says that person 2 is a scallop (lie)
        if says_is_knave:
            t = str(person1) + " says that " + str(person2) + " is a Scallop."
            s.add(Implies(person1, Not(person2)))
            s.add(Implies(Not(person1), person2))

        # if person 1 says that person 2 is a clam (truth)
        else:
            t = str(person1) + " says that " + str(person2) + " is a Clam."
            s.add(Implies(person1, person2))
            s.add(Implies(Not(person1), Not(person2)))

        statements.append(t)

    res = s.check()

    if res == sat:
        mod = s.model()
        assignments = {}
        for v in mod:
            assignments[str(v)] = str(mod[v])

        for i in range(n):
            n = "Shellfish" + str(i)
            if(n not in assignments.keys()):
                assignments[n] = "Both"
        result = {
            "statements": statements,
            "assignments": assignments
        }
        return result
    else:
        return generate_instances(n)


# === Route 6: magic square puzzle ===
@app.route('/magic_square')
def get_4x4_square():

    file_path = os.path.join(app.root_path, 'static', 'magic_squares_4x4.txt')

    f = open(file_path, "r")
    puzzles = f.readlines()

    puz = random.choice(puzzles)
    puz = puz.replace("\n", "")

    items = puz.split(" ")

    one_answer = {}

    for sq in items:
        a = sq.split("=")
        one_answer[a[0]] = a[1]
    
    hidden = random.sample(list(one_answer.keys()), random.randint(1, 16))

    res = {
        "full": one_answer,
        "hidden": hidden
    }
    
    return res

@app.route('/check_magic_square', methods=['POST'])
def check_magic_square():

    data = request.get_json()

    if not data:
        return jsonify({"success": False, "message": "No data received."})
    try:
        values = [int(data[f's{i}']) for i in range(16)]
    except Exception:
        return jsonify({"success": False, "message": "All 16 values must be integers."})

    magic_sum = 34

    if (len(values) != len(set(values))):
        return jsonify({"success": True, "valid": False, "message": " Duplicate Value"})

    box = []
    for i in range(4):
        row = []
        for j in range(4):
            if (1 <= values[i * 4 + j] and 16 >= values[i * 4 + j]):
                row.append(values[i * 4 + j])
            else:
                return jsonify({"success": True, "valid": False, "message": " Some Value not between 1 and 16"})
            
        box.append(row)

    # row
    for i in range(4):
        if (sum(box[i]) != magic_sum):
            return jsonify({"success": True, "valid": False, "message": " Wrong Sum"})

    # column
    for i in range(4):
        col = []
        for j in range(4):
            col.append(box[i][j])
                
        if (sum(box[i]) != magic_sum):
            return jsonify({"success": True, "valid": False, "message": " Wrong Sum"})

    # diagonals
    diag1 = []
    diag2 = []
    for i in range(4):
        diag1.append(box[i][i])
        diag2.append(box[i][3 - i])

    if (sum(diag1) != magic_sum or sum(diag2) != magic_sum):
        return jsonify({"success": True, "valid": False, "message": " Wrong Sum"})

    return jsonify({"success": True, "valid": True})

# === Route 7: Check User generated magic square puzzle ===
# Checks whether user's inputs could be made into a valid
# magic square
@app.route('/check_gen_ms', methods=['POST'])
def check_valid_square():

    data = request.get_json()

    if not data:
        return jsonify({"success": False, "message": "No data received."})
    
    v = list(data.values()) # values
    sqr_ints = list(data) # names

    n = int(math.sqrt(len(v)))

    squares = []
    for i in range((n * n)):
        name = sqr_ints[i]
        squares.append(Int(str(name)))

    s = Solver()

    for i in range(len(v)):
        if v[i] is not None:
            s.add(squares[i] == int(v[i]))

    magic_sum = (n * (n * n + 1)) // 2

    for sqr in squares:
        s.add(sqr <= n * n)
        s.add(sqr >= 1)

    s.add(Distinct(squares))

    # rows and columns
    for i in range(n):
        hor_vals = []
        ver_vals = []
        for j in range(n):
            hor_vals.append(squares[n * i + j])
            ver_vals.append(squares[i + n * j])

        s.add(Sum(hor_vals) == magic_sum)
        s.add(Sum(ver_vals) == magic_sum)

    # diagonals
    diag1 = []
    diag2 = []

    for i in range(n):
        diag1.append(squares[i * (n + 1)])

    for i in range(n):
        diag2.append(squares[(n - 1) * (i + 1)])

    s.add(Sum(diag1) == magic_sum)
    s.add(Sum(diag2) == magic_sum)

    res = s.check()

    if res == sat:
        mod = s.model()
        return jsonify({"success": True, "valid": True, "model": str(mod)})
    else:
        return jsonify({"success": True, "valid": False})

# === Flow: Home (start game) ===
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/home')
def returnHome():
    return render_template('index.html') 

@app.route('/intro')
def changeToIntro():
    return render_template('alexa.html')

@app.route('/river')
def changeToPuzzle1():
    return render_template('rivercrossing.html')

@app.route('/age')
def changeToPuzzle2():
    return render_template('age.html')

@app.route('/lie-intro')
def changeToPuzzle3Intro():
    return render_template('lie_intro.html')

@app.route('/lie')
def changeToPuzzle3():
    return render_template('lie.html')

@app.route('/magic-sqr')
def changeToPuzzle4():
    return render_template('magic_square.html')

@app.route('/magic-sqr-user')
def changeToPuzzle5():
    return render_template('magic_square_user.html')

@app.route('/end')
def changeToEnd():
    return render_template('end.html')

if __name__ == '__main__':
    app.run(debug=True)
