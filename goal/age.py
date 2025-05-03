# Authored By Lilymoon Whalen 
from z3 import *

import random

def solve_random_age_riddle():
    # Define variables for the ages of three children
    age1 = Int('age1')
    age2 = Int('age2')
    age3 = Int('age3')

    # Create a solver instance
    solver = Solver()

    # Inline generator to create random variations of the problem
    for _ in range(100):
        random_product = random.randint(1, 100)  # Random product of ages
        random_sum = random.randint(3, 50)      # Random sum of ages

        solver.push()  # Save the current state of the solver
        solver.add(age1 > 0, age2 > 0, age3 > 0)  # Ages must be positive integers
        solver.add(age1 * age2 * age3 == random_product)      # Product of ages
        solver.add(age1 + age2 + age3 == random_sum)      # Sum of ages

        if solver.check() == sat:
            model = solver.model()
            print(f"Found satisfying instance with product = {random_product} and sum = {random_sum}: "
                  f"age1 = {model[age1]}, age2 = {model[age2]}, age3 = {model[age3]}")
            break
        else:
            print("No satisfying instance found for generated random variations.")
            print(f"Product: {random_product}, Sum: {random_sum}")
        solver.pop()  # Restore the solver state
    
##############################
####### Riddle Solver  #######
##############################

# This code solves a riddle where the ages of three children satisfy certain conditions:
# 1. The product of their ages is 36.
# 2. The sum of their ages is 13.
# The goal is to find the possible ages of the children using a constraint solver.
# Define variables for the ages of three children
def solve_age_riddle():
    age1 = Int('age1')
    age2 = Int('age2')
    age3 = Int('age3')

    # Create a solver instance
    solver = Solver()
    

    # Add constraints based on the riddle
    # Example: The product of their ages is 36, and the sum of their ages is 13
   # Ages must be between 1 and 12 (inclusive)
    solver.add(age1 > 0, age1 < 13)
    solver.add(age2 > 0, age2 < 13)
    solver.add(age3 > 0, age3 < 13)
        
    solver.add(age1 * age2 * age3 == 36)      # Product of ages
    solver.add(age1 + age2 + age3 == 13)      # Sum of ages
    solver.add(age1 <= age2, age2 <= age3)

    # Solve the puzzle
    if solver.check() == sat:
        model = solver.model()
        print(f"Solution: age1 = {model[age1]}, age2 = {model[age2]}, age3 = {model[age3]}")
    else:
        print("No solution found.")


solve_age_riddle()
solve_random_age_riddle()
