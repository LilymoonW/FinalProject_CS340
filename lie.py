from z3 import *

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



#A very special island is inhabited only by knights and knaves. 
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

def knight_knave3():
    h = Bool("h")
    i = Bool("i")
    j = Bool("j")

    s = Solver()

    s.add(Or(h, Not(h))) # 1
    s.add(Implies(i, Implies(h, Not(h)))) # 2
    s.add(Implies(i, Not(j))) # 3
    s.add(Implies(j, h)) # 4

    s.add(Implies(Not(h), Not(Or(h, Not(h))))) # not 
    s.add(Implies(Not(i), Implies(h, h)))


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
