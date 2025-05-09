
from z3 import *
import random

# Fill the grid with the digits 1 to 9, each used once. Every row, column, and diagonal must sum to 15.
# [s0 s1 s2]
# [s3 s4 s5]
# [s6 s7 s8]
# Gives one correct instance of the magic square
def magic_square1():

    ts = 15 # total sum

    squares = []
    for i in range(9):
        name = "s" + str(i)
        squares.append(Int(str(name)))

    s = Solver()

    for sqr in squares:
        s.add(sqr <= 9)
        s.add(sqr >= 1)

    s.add(Distinct(squares))

    for i in range(3):
        # horizontal
        s.add((squares[3 * i] + squares[3 * i + 1] + squares[3 * i + 2]) == ts)

        # vertical
        s.add((squares[i] + squares[i + 3] + squares[i + 6]) == ts)

    # diagonal
    s.add((squares[0] + squares[4] + squares[8]) == ts)
    s.add((squares[6] + squares[4] + squares[2]) == ts)

    res = s.check()

    if res == sat:
        mod = s.model()
        print(mod)
    else:
        print(res)

# magic_square1()

# Generate instances of a magic square with n rows 
# and n columns. The grid should be filled with the digits 1 
# to n^2, each used once. Every row, column, and diagonal 
# should sum to (n * (n^2 + 1) / 2).
# n = number of boxes for each square
def generate_square(n):

    squares = []
    for i in range((n * n)):
        name = "s" + str(i)
        squares.append(Int(str(name)))

    s = Solver()

    magic_sum = (n * (n * n + 1)) / 2

    # each num should be between 1 and n^2
    for sqr in squares:
        s.add(sqr <= n * n)
        s.add(sqr >= 1)

    # each square's number should be different
    s.add(Distinct(squares))

    # rows and columns sum must add to magic_sum
    for i in range(n):
        hor_vals = []
        ver_vals = []
        for j in range(n):
            hor_vals.append(squares[n * i + j])
            ver_vals.append(squares[i + n * j])

        s.add(sum(hor_vals) == magic_sum)
        s.add(sum(ver_vals) == magic_sum)

    # main diagonals
    diag1 = []
    diag2 = []

    # add main diagonals value to list and check their sum
    for i in range(n):
        diag1.append(squares[i * (n + 1)])

    for i in range(n):
        diag2.append(squares[(n - 1) * (i + 1)])

    s.add(Sum(diag1) == magic_sum)
    s.add(Sum(diag2) == magic_sum)
        
    res = s.check()

    if res == sat:
        mod = s.model()
        print(mod)
    else:
        print(res)

    # return s

# generate_square(4)

# generate all instances of 4x4 magic squares by adding 
# past instances of magic squares found to the solver so it
# avoids those instances and tries to find new ones instead.
def all_models(solver):
    all_models = []

    while solver.check() == sat:
        mod = solver.model()
        all_models.append(mod)

        already_found = []
        for var in mod:
            already_found.append(var() != mod[var])
        solver.add(Or(already_found))
    
    return all_models

# writes all instances of the 4x4 magic puzzle onto magic_squares_4x4.txt
def get_instances_4by4():
    sol = generate_square(4)
    all_mod = all_models(sol)

    # f = open("magic_squares_4x4.txt", "w")

    for mo in all_mod:
        m = str(mo)
        m = m.replace("[", "")
        m = m.replace("]", "")
        m = m.replace("\n", "")
        m = m.replace(" ", "")
        m = m.replace(",", " ")
        # f.write(str(m) + "\n")

# get a random 4x4 magic square from the txt file
def get_4x4_square():
    f = open("magic_squares_4x4.txt", "r")
    puzzles = f.readlines()

    puz = random.choice(puzzles)
    puz = puz.replace("\n", "")

    items = puz.split(" ")

    answer = {}

    for sq in items:
        a = sq.split("=")
        answer[a[0]] = a[1]
    
    print(answer) 

# get_4x4_square()
