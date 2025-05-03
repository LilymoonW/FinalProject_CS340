from z3 import *
import random
from flask_cors import CORS
from flask import Flask, jsonify, send_from_directory, request

app = Flask(__name__)
CORS(app)

# n = number of people
def generate_instances(n):
    s = Solver()

    bools = [] # maybe rename this
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
    

@app.route('/')
def index():
    return send_from_directory('.', 'lie.html')

@app.route('/generate')
def generate():
    n = random.randint(3,5)
    result = generate_instances(n)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
