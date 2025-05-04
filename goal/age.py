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
    
#########################################
####### Riddle Solver Age Riddle  #######
#########################################

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


#solve_age_riddle()
#solve_random_age_riddle()




#########################################
#####  Apple orange misslabled boxes ###
#########################################


### This code solves a riddle where three boxes are labeled incorrectly.
###In front of you are 3 boxes. One box contains only apples, another box contains only oranges, and the last contains both apples and oranges.
### Each box is labeled, but all the labels are incorrect. You can pick one fruit from one box to determine the contents of all three boxes.
def mismatched_boxes():
    contents = ['Apples', 'Oranges', 'Mixed']

    # Create integer variables for the actual contents of each box
    # 0: Apples, 1: Oranges, 2: Mixed
    box1 = Int('box1')
    box2 = Int('box2')
    box3 = Int('box3')

    # Create a solver instance
    s = Solver()

    # Each box must have a unique content
    s.add(Distinct(box1, box2, box3))

    # Each box's content must be one of the three options
    s.add(And(box1 >= 0, box1 <= 2))
    s.add(And(box2 >= 0, box2 <= 2))
    s.add(And(box3 >= 0, box3 <= 2))

    # Randomly assign incorrect labels to the boxes
    labels = ['Apples', 'Oranges', 'Mixed']
    random_labels = random.sample(range(3), 3)  # Generate a random permutation of labels
    # Since all labels are incorrect, the content must not match the random label
    s.add(box1 != random_labels[0])  # Box1 content must not match its random label
    s.add(box2 != random_labels[1])  # Box2 content must not match its random label
    s.add(box3 != random_labels[2])  # Box3 content must not match its random label

    print(f"Random labels assigned: Box1 = {labels[random_labels[0]]}, "
          f"Box2 = {labels[random_labels[1]]}, Box3 = {labels[random_labels[2]]}")
    # Check for a solution
    if s.check() == sat:
        m = s.model()
        
        box_contents = [m[box1].as_long(), m[box2].as_long(), m[box3].as_long()]
        
        for i, content in enumerate(random_labels):
            print(f"Box {i+1} is labeled '{labels[content]}' and contains: {contents[box_contents[i]]}")
    else:
        print("No solution found.")


mismatched_boxes()