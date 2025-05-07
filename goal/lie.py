from z3 import *
import random


def make_implications(statements):

    if not statements:
        return BoolVal(True)
    
    implications = []

    for s in statements:
        implications.append(Implies(s[0], s[1]))

    return implications


# A very special island is inhabited only by knights and knaves. 
# Knights always tell the truth, and knaves always lie.

# Alice and Bob are residents of the island of knaves and knights
# Bob says: “We are both knaves”
# Whose the knight and who is a knave?
# solution: Alice = True, Bob = False
def knight_knave1():
    # true means that they are knights

    b = Bool("b") # mel
    a = Bool("a") # zoey

    s = Solver()

    constraints = []
    constraints.append((b, And(Not(b), Not(a))))
    constraints.append((Not(b), Or(b, a)))
    s.add(And(make_implications(constraints)))
    
    res = s.check()

    if res == sat:
        mod = s.model()
        print(mod)
    else:
        print(res)

# knight_knave1()


# You meet two inhabitants: Zoey and Mel. 
# Zoey tells you that Mel is a knave. 
# Mel says, “Neither Zoey nor I are knaves.”
# solution: Z = True, Mel = False
def knight_knave2():
    m = Bool("m") # mel
    z = Bool("z") # zoey

    s = Solver()

    c = [] # constraints

    # zoey's statement
    c.append((z, Not(m)))
    c.append((Not(z), m))

    # mel's statement
    c.append((m, And(z, m)))
    c.append((Not(m), Or(Not(z), Not(m))))

    s.add(And(make_implications(c)))

    res = s.check()

    if res == sat:
        mod = s.model()
        print(mod)
    else:
        print(res)

# knight_knave2()

# Goodman's Variant
# Three inhabitants Hugo, Iris, James meet some day
# 1) Hugo says either “I am a knight” or “I am a knave”, we don't know which 
# 2) Iris says “Hugo said, ‘I am a knave’”
# 3) Iris says “James is a knave”
# 4) James says “Hugo is knight”
# Who is a knave and who is a knight?
# Solution: H = True, I = False, J = True
def knight_knave3():
    h = Bool("h")
    i = Bool("i")
    j = Bool("j")

    s = Solver()

    c = [] # constraints

    # Hugo's statement
    # true = i am knight, false = i am knave
    h_statement = Bool("h_statement") 
    
    # 1
    c.append((h, Implies(h_statement, h)))
    c.append((h, Implies(Not(h_statement), Not(h))))
    c.append((Not(h), Implies(h_statement, Not(h))))
    c.append((Not(h), Implies(Not(h_statement), h)))

    # 2
    c.append((i, Not(h_statement)))
    c.append((Not(i), h_statement))

    # 3
    c.append((i, Not(j)))
    c.append((Not(i), j))

    # 4
    c.append((j, h))
    c.append((Not(j), Not(h)))

    s.add(And(make_implications(c)))

    res = s.check()

    if res == sat:
        mod = s.model()
        print(mod)
    else:
        print(res)

# knight_knave3()

# knight, a knave, or normals (normals can tell lies or truths)

# You meet Kenny, Lily, and Max who are all different classes
# 1) Kenny says “I am the knight,”
# 2) Lily says “I am the knave,”
# 3) Max says “Lily is the knight.”
# Who is the knight, the knave, and the normal?
# solution: K = 1, L = 0, M = -1
def knight_knave4():
    k = Int("k")
    l = Int("l")
    m = Int("m")

    s = Solver()

    # -1 = knave, 0 = normal, 1 = knight
    all_c = [] # all constraints

    # have 
    all_c.append(And(k >= -1, k <= 1))
    all_c.append(And(l >= -1, l <= 1))
    all_c.append(And(m >= -1, m <= 1))

    # all different classes
    all_c.append(Distinct(k,l,m))

    # implications
    i = []

    i.append((k == 1, k == 1))
    i.append((k == -1, k != 1))

    i.append((l == 1, l == -1))
    i.append((l == -1, l != -1))

    i.append((m == 1, l == 1))
    i.append((m == -1, l != 1))

    all_c.extend(make_implications(i))
    s.add(And(all_c))

    res = s.check()

    if res == sat:
        mod = s.model()
        print(mod)
    else:
        print(res)
          
# knight_knave4()


# 5
# 1) Kenny says “I am the knight,”
# 2) Lily says “Kenny is telling the truth,”
# 3) Max says “I am the normal”
# Who is the knight, the knave, and the normal?
# solution: k = 1, l = 0, m = -1
def knight_knave5():
    k = Int("k")
    l = Int("l")
    m = Int("m")

    s = Solver()

    # -1 = knave, 0 = normal, 1 = knight

    all_c = [] # all constraints

    # have 
    all_c.append(And(k >= -1, k <= 1))
    all_c.append(And(l >= -1, l <= 1))
    all_c.append(And(m >= -1, m <= 1))

    # all different classes
    all_c.append(Distinct(k,l,m))

    # implications 
    i = []

    # true = kenny tells truth, false = kenny lies
    k_statement = Bool("k_statement") 
    i.append((k_statement, k == 1))
    i.append((Not(k_statement), k != 1))

    #1
    i.append((k == 1, k == 1))
    i.append((k == -1, Not(k == 1)))

    #2 
    i.append((l == 1, k_statement))
    i.append((l == -1, Not(k_statement)))

    #3
    i.append((m == 1, m == 0))
    i.append((m == -1, Not(m == 0)))

    all_c.extend(make_implications(i))
    s.add(And(all_c))

    res = s.check()

    if res == sat:
        mod = s.model()
        print(mod)
    else:
        print(res)
          
# knight_knave5()


# 6
# Kenny says “I am not the normal,”
# Lily says “I am not the normal,”
# Max says “I am not the normal”
# solution: no solutions
def knight_knave6():
    k = Int("k")
    l = Int("l")
    m = Int("m")

    s = Solver()

    # -1 = knave, 0 = normal, 1 = knight
    all_c = [] # all constraints

    # have 
    all_c.append(And(k >= -1, k <= 1))
    all_c.append(And(l >= -1, l <= 1))
    all_c.append(And(m >= -1, m <= 1))

    # all different classes
    all_c.append(Distinct(k,l,m))

    # implications
    i = []
    i.append((k == 1, k != 0))
    i.append((k == -1, k == 0))

    i.append((l == 1, l != 0))
    i.append((l == -1, l == 0))

    i.append((m == 1, m != 0))
    i.append((m == -1, m == 0))

    all_c.extend(make_implications(i))
    s.add(And(all_c))

    res = s.check()

    if res == sat:
        mod = s.model()
        print(mod)
    else:
        print(res)

knight_knave6() 


# n = number of people
# Generates a random knights and knaves puzzle with 
# n number of people, keeps generating until find 
# an instance of a satisfying puzzle. 
def generate_instances(n):
    s = Solver()

    bools = []
    for i in range(n):
        name = "p" + str(i)
        bools.append(Bool(name))

    # number of statements is n
    for i in range(n):
        person1 = random.choice(bools)
        person2 = random.choice(bools)

        says_is_knave = random.choice([True, False])

        # # if person 1 says that person 2 is a knave
        if says_is_knave:
            print(person1, "says that", person2, "is a knave")
            s.add(Implies(person1, Not(person2)))
            s.add(Implies(Not(person1), person2))

        # if person 1 says that person 2 is a knight
        else:
            print(person1, "says that", person2, "is a knight")
            s.add(Implies(person1, person2))
            s.add(Implies(Not(person1), Not(person2)))

    res = s.check()

    if res == sat:
        mod = s.model()
        print(mod)
    else:
        generate_instances(n)

# generate_instances(random.randint(3,5))