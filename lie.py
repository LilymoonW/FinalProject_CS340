from z3 import *
import random

#

# Alice and Bob are residents of the island of knaves and knights
# Bob says: “We are both knaves”
# Whose the knight and who is a knave?

def knight_knave1():
    # true means that they are knights

    b = Bool("b") # mel
    a = Bool("a") # zoey

    s = Solver()

    s.add(Implies(b, And(Not(b), Not(a))))
    s.add(Implies(Not(b), Or(b, a)))

    res = s.check()

    if res == sat:
        mod = s.model()
        print(mod)
        print(mod.evaluate(a))
        print(mod.evaluate(b))
    else:
        print(res)

# knight_knave1()



# A very special island is inhabited only by knights and knaves. 
# Knights always tell the truth, and knaves always lie.

#You meet two inhabitants: Zoey and Mel. 
# Zoey tells you that Mel is a knave. 
# Mel says, “Neither Zoey nor I are knaves.”

#Can you determine who is a knight and who is a knave?

def knight_knave2():
    # true means that they are knights

    m = Bool("m") # mel
    z = Bool("z") # zoey

    s = Solver()

    s.add(Implies(z, Not(m))) # zoey's statement
    s.add(Implies(m, And(z, m)))

    # what does one telling truth imply about the other
    s.add(Implies(Not(m), Or(Not(z), Not(m))))
    s.add(Implies(Not(z), m))

    res = s.check()

    if res == sat:
        mod = s.model()
        print(mod)
        print(mod.evaluate(m))
        print(mod.evaluate(z))
    else:
        print(res)

# knight_knave2()


# Three inhabitants Hugo, Iris, James meet some day
# 1) Hugo says either “I am a knight” or “I am a knave”, we don't know which 
# 2) Iris says “Hugo said, ‘I am a knave’”
# 3) Iris says “James is a knave”
# 4) James says “Hugo is knight”
# Who is a knave and who is a knight?

# finish

def knight_knave3():
    h = Bool("h")
    i = Bool("i")
    j = Bool("j")

    s = Solver()

    # s.add(Or(h, Not(h))) # 1
    s.add(Implies(i, Implies(h, Not(h)))) # 2
    s.add(Implies(i, Implies(Not(h), h)))
    s.add(Implies(i, Not(j))) # 3
    s.add(Implies(j, h)) # 4

    # s.add(Implies(Not(h), Not(Or(h, Not(h))))) # useless
    s.add(Implies(Not(i), Implies(h, h))) # 2
    s.add(Implies(Not(i), Implies(Not(h), Not(h)))) # 2
    s.add(Implies(Not(i), j)) # 3
    s.add(Implies(Not(j), Not(h))) # 4


    res = s.check()

    if res == sat:
        mod = s.model()
        print(mod)
        print(mod.evaluate(h))
        print(mod.evaluate(i))
        print(mod.evaluate(j))
    else:
        print(res)

# knight_knave3()

# knight, a knave, or normals (normals can tell lies or truths)

# You meet Kenny, Lily, and Max who are all different classes
# 1) Kenny says “I am the knight,”
# 2) Lily says “I am the knave,”
# 3) Max says “Lily is the knight.”
# Who is the knight, the knave, and the normal?

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

    # all dufferebt ckasses
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
    s.add(Implies(k == 1, k == 1)) # 1
    s.add(Implies(l == 1, l == -1))
    s.add(Implies(m == 1, l == 1))

    s.add(Implies(k == -1, k != 1)) # 1
    s.add(Implies(l == -1, l != -1))
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



# FIX THIS
# 5
# 1) Kenny says “I am the knight,”
# 2) Lily says “Kenny is telling the truth,”
# 3) Max says “I am the normal”
# Who is the knight, the knave, and the normal

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

    # all dufferebt ckasses
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
    s.add(Implies(k == 1, k == 1)) # 1
    s.add(Implies(l == 1, k == 1))
    s.add(Implies(m == 1, Or(m == 1, m == -1)))

    s.add(Implies(k == -1, k != 1)) # 1
    s.add(Implies(l == -1, k != 1))
    s.add(Implies(m == -1, Not(Or(m == 1, m == -1))))

    res = s.check()

    if res == sat:
        mod = s.model()
        print(mod)
        print(mod.evaluate(k))
        print(mod.evaluate(l))
        print(mod.evaluate(m))
    else:
        print(res)
          
# knight_knave5() # fix this


# 6
# Kenny says “I am not the normal,”
# Lily says “I am not the normal,”
# Max says “I am not the normal”
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

    # all dufferebt ckasses
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

generate_instances(random.randint(3,5))