from z3 import *

f = Bool('f') # farmer

x = Bool('x') # fox
x_arr = []
g = Bool('g') # goose
g_arr = []
b = Bool('b') # beans
b_arr = []

range = 7
final = {}

s = Solver()


# if move isn't at range, then do something
def move(t):
    s.add(x_arr[0] == False)
    s.add(g_arr[0] == False)
    s.add(b_arr[0] == False)


    