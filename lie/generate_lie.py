from z3 import *
import random
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# n = number of people
def generate_instances(n):
    s = Solver()
    ppl = []

    bools = []
    for i in range(n):
        ppl.append(random.choice([True, False]))
        name = "p" + str(i)
        bools.append(Bool(name))

    statements = []

    # number of statements is n?
    for i in range(n):
        person1 = random.choice(bools)
        person2 = random.choice(bools)

        says_is_knave = random.choice([True, False])

        # # if person 1 says that person 2 is a knave
        if says_is_knave:
            t = str(person1) + "says that" + str(person2) + "is a knave"
            s.add(Implies(person1, Not(person2)))
            s.add(Implies(Not(person1), person2))

        # if person 1 says that person 2 is a knight
        else:
            t = str(person1) + "says that" + str(person2) + "is a knight"
            s.add(Implies(person1, person2))
            s.add(Implies(Not(person1), Not(person2)))

        statements.append(t)

    res = s.check()

    if res == sat:
        mod = s.model()
        assignments = {}
        for v in mod:
            assignments[v] = mod[v]
        # print(assignments)
        return statements, assignments
    else:
        return generate_instances(n)
    


@app.route('/generate', methods=['GET'])
def generate_puzzle():
    n = 3  
    statements, assignments = generate_instances(n)
    return jsonify({
        "statements": statements,
        "assignments": assignments
    })

if __name__ == '__main__':
    app.run(debug=True)