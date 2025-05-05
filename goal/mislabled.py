
# Authored By Lilymoon Whalen 
from z3 import *
import random
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