from z3 import *
import random

def combine_implications(statements):

    if not statements:
        return BoolVal(True)
    
    implications = []

    for s in statements:
        implications.append(Implies(s[0], s[1]))

    final = implications[0]
    for i in range(1, len(implications)):
        final = And(final, implications[i])
    
    return final


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

    
    # constraints
    # s.add(Implies(b, And(Not(b), Not(a))))
    # s.add(Implies(Not(b), Or(b, a)))

    constraints = []
    constraints.append((b, And(Not(b), Not(a))))
    constraints.append((Not(b), Or(b, a)))
    s.add(combine_implications(constraints))
    
    res = s.check()

    if res == sat:
        mod = s.model()
        print(mod)
        print(mod.evaluate(a))
        print(mod.evaluate(b))
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
    # s.add(Implies(z, Not(m))) #tell truth
    # s.add(Implies(Not(z), m)) #lying

    # mel's statement
    c.append((m, And(z, m)))
    c.append((Not(m), Or(Not(z), Not(m))))
    # s.add(Implies(m, And(z, m)))
    # s.add(Implies(Not(m), Or(Not(z), Not(m))))

    s.add(combine_implications(c))

    res = s.check()

    if res == sat:
        mod = s.model()
        print(mod)
        print(mod.evaluate(m))
        print(mod.evaluate(z))
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
    # s.add(Or(h_statement, Not(h_statement))) # don't really need but
    
    c.append((h, Implies(h_statement, h)))
    c.append((h, Implies(Not(h_statement), Not(h))))
    # s.add(Implies(h, Implies(h_statement, h)))
    # s.add(Implies(h, Implies(Not(h_statement), Not(h))))

    c.append((Not(h), Implies(h_statement, Not(h))))
    c.append((Not(h), Implies(Not(h_statement), h)))
    # s.add(Implies(Not(h), Implies(h_statement, Not(h))))
    # s.add(Implies(Not(h), Implies(Not(h_statement), h)))

    c.append((i, Not(h_statement)))
    c.append((Not(i), h_statement))
    # s.add(Implies(i, Not(h_statement))) # 2
    # s.add(Implies(Not(i), h_statement)) # 2

    c.append((i, Not(j)))
    c.append((Not(i), j))
    # s.add(Implies(i, Not(j))) # 3
    # s.add(Implies(Not(i), j)) # 3

    c.append((j, h))
    c.append((Not(j), Not(h)))
    # s.add(Implies(j, h)) # 4
    # s.add(Implies(Not(j), Not(h))) # 4

    s.add(combine_implications(c))

    res = s.check()

    if res == sat:
        mod = s.model()
        print(mod)
        print(mod.evaluate(h))
        print(mod.evaluate(i))
        print(mod.evaluate(j))
    else:
        print(res)

knight_knave3()

# knight, a knave, or normals (normals can tell lies or truths)

# You meet Kenny, Lily, and Max who are all different classes
# 1) Kenny says “I am the knight,”
# 2) Lily says “I am the knave,”
# 3) Max says “Lily is the knight.”
# Who is the knight, the knave, and the normal?
# 
def knight_knave4():
    k = Int("k")
    l = Int("l")
    m = Int("m")

    s = Solver()

    # -1 = knave
    # 0 = normal
    # 1 = knight
    s.add(Or(k == -1, Or(k == 0, k == 1)))
    s.add(Or(l == -1, Or(l == 0, l == 1)))
    s.add(Or(m == -1, Or(m == 0, m == 1)))

    # all different ckasses
    s.add(Distinct(k,l,m))

    # constraints
    s.add(Implies(k == 1, k == 1)) # 1
    s.add(Implies(k == -1, k != 1)) # 1

    s.add(Implies(l == 1, l == -1))
    s.add(Implies(l == -1, l != -1))

    s.add(Implies(m == 1, l == 1))
    s.add(Implies(m == -1, l != 1))

    # s.add(Implies(k == 0, Or(k == 1)) # 1
    # s.add(Implies(l == 0, l == -1))
    # s.add(Implies(m == 0, l == 1))

    res = s.check()

    if res == sat:
        mod = s.model()
        print(mod)
        print(mod.evaluate(k))
        print(mod.evaluate(l))
        print(mod.evaluate(m))
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

    # -1 = knave
    # 0 = normal
    # 1 = knight
    s.add(Or(k == -1, Or(k == 0, k == 1)))
    s.add(Or(l == -1, Or(l == 0, l == 1)))
    s.add(Or(m == -1, Or(m == 0, m == 1)))

    # all different classes
    s.add(Implies(k == -1, And(l != -1, m != -1)))
    s.add(Implies(k == 0, And(l != 0, m != 0)))
    s.add(Implies(k == 1, And(l != 1, m != 1)))

    s.add(Implies(l == -1, And(k != -1, m != -1)))
    s.add(Implies(l == 0, And(k != 0, m != 0)))
    s.add(Implies(l == 1, And(k != 1, m != 1)))

    s.add(Implies(m == -1, And(l != -1, k != -1)))
    s.add(Implies(m == 0, And(l != 0, k != 0)))
    s.add(Implies(m == 1, And(l != 1, k != 1)))

    # constraints 
    #1
    s.add(Implies(k == 1, k == 1))
    s.add(Implies(k == -1, Not(k == 1)))

    #2 
    s.add(Implies(l == 1, k == 1))
    s.add(Implies(l == -1, Not(k == 1)))

    #3
    s.add(Implies(m == 1, m == 0))
    s.add(Implies(m == -1, Not(m == 0)))

    res = s.check()

    if res == sat:
        mod = s.model()
        print(mod)
        print(mod.evaluate(k))
        print(mod.evaluate(l))
        print(mod.evaluate(m))
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

    # -1 = knave
    # 0 = normal
    # 1 = knight
    s.add(Or(k == -1, Or(k == 0, k == 1)))
    s.add(Or(l == -1, Or(l == 0, l == 1)))
    s.add(Or(m == -1, Or(m == 0, m == 1)))

    # all dufferent ckasses
    s.add(Implies(k == -1, And(l != -1, m != -1)))
    s.add(Implies(k == 0, And(l != 0, m != 0)))
    s.add(Implies(k == 1, And(l != 1, m != 1)))

    s.add(Implies(l == -1, And(k != -1, m != -1)))
    s.add(Implies(l == 0, And(k != 0, m != 0)))
    s.add(Implies(l == 1, And(k != 1, m != 1)))

    s.add(Implies(m == -1, And(l != -1, k != -1)))
    s.add(Implies(m == 0, And(l != 0, k != 0)))
    s.add(Implies(m == 1, And(l != 1, k != 1)))

    # constrants
    s.add(Implies(k == 1, k != 0))
    s.add(Implies(l == 1, l != 0))
    s.add(Implies(m == 1, m != 0))

    s.add(Implies(k == -1, k == 0))
    s.add(Implies(l == -1, l == 0))
    s.add(Implies(m == -1, m == 0))

    res = s.check()

    if res == sat:
        mod = s.model()
        print(mod)
        print(mod.evaluate(k))
        print(mod.evaluate(l))
        print(mod.evaluate(m))
    else:
        print(res)

# knight_knave6() 


# n = number of people
# Generates a random knights and knaves puzzle with 
# n number of people. 
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