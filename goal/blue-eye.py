"""The Blue-Eyed Islander Problem: Unsuccesful Attempt to model in Z3"""
from z3 import*
import random
# Inductive Proof of the Blue-Eyed Islander Problem:

# Setup:
# - There are n perfect logicians on an island.
# - k of them have blue eyes, but no one knows their own eye color.
# - Each person can see others' eye colors but not their own.
# - A visitor publicly announces: "At least one of you has blue eyes."
# - Each day, islanders have the chance to leave the island with a sailor if they can deduce their eye color.
# - Everyone is perfectly logical and knows everyone else is too.

# Inductive Reasoning:

# Base Case (k = 1):
# - The single blue-eyed person sees 0 others with blue eyes.
# - They reason: "If I did not have blue eyes, then no one would have blue eyes.
#   But the visitor said at least one person does, so it must be me."
# - So they leave on Day 1.

# Inductive Step (Assume true for k = n - 1):
# - Suppose there are k = n blue-eyed people.
# - Each blue-eyed person sees (n - 1) others with blue eyes.
# - They initially assume: "Maybe I have brown eyes, and the n - 1 people I see are the only blue-eyed ones."
# - Under this assumption, those n - 1 people should leave on Day (n - 1), since each would see (n - 2) blue-eyed individuals.
# - When no one leaves on Day (n - 1), this disproves the assumption.
# - Therefore, each of the n blue-eyed islanders realizes they must also have blue eyes.
# - All n blue-eyed people leave on Day n.

# Why brown-eyed people leave:
# - Brown-eyed people see k blue-eyed individuals.
# - They assume: "If I had blue eyes, others would see k - 1 blue-eyed people."
# - But because blue-eyed people do leave on Day k, the brown-eyed people observe this and safely conclude
#   they must not be among the blue-eyed group.
# - Hence, brown-eyed people leave on the next day .

# Summary:
# - All blue-eyed islanders leave on Day k (where k is the number of blue-eyed people).
# - Brown-eyed islanders never leave.

# This code simulates the blue-eyed islander problem using Z3 to verify the inductive proof.
from z3 import *
import random

def blue_eyed_islander():
    n = 5
    k = 3
    max_days = k + 2  # simulate through day k+1

    blue_eyed = [Bool(f"blue_{i}") for i in range(n)] # blue-eyed islanders
    leaves = [[Bool(f"leaves_{i}_d{d}") for d in range(max_days)] for i in range(n)] # leaving days

    s = Solver()

    # Exactly k blue-eyed islanders
    s.add(Sum([If(blue_eyed[i], 1, 0) for i in range(n)]) == k)

    for i in range(n): 
        seen_blue = Sum([If(blue_eyed[j], 1, 0) for j in range(n) if j != i]) # count of blue-eyed seen by i

        # Once you leave, you stay gone
        for day in range(max_days):
            if day > 0:
                s.add(Implies(leaves[i][day - 1], leaves[i][day]))
        
        # Deductive Rule:
        # If I see k others with blue eyes, and all of them leave on day k, and I haven't left before,
        # I deduce I must be brown-eyed too and leave on day k
        # if I see seen_blue == i blue-eyed eyed people and they don't leave on day seen_blue day
        # then I must be blue-eyed too and leave on day seen_blue+1
        # if I see seen_blue == i and they all leave on day seen_blue then I must be brown-eyed too and leave on day seen_blue+1

        for k_guess in range(1, max_days - 1):  # Ensure k+1 fits in range
            # Check if the islander sees exactly k_guess blue-eyed individuals
            seen_k = (seen_blue == k_guess) 

            # Ensure the islander has not left yet (up to and including day k_guess)
            not_left_yet = And([Not(leaves[i][d]) for d in range(k_guess + 1)]) 

            # Check if all blue-eyed individuals seen by the islander have left on day k_guess
            all_seen_left_on_k = And([
                Implies(blue_eyed[j], leaves[j][k_guess]) for j in range(n) if j != i 
            ])

            # If the islander sees exactly k_guess blue-eyed individuals, all of them left on day k_guess,
            # and the islander has not left yet, they deduce they must leave on day k_guess + 1
            s.add(Implies(
                And(seen_k, all_seen_left_on_k, not_left_yet),
                leaves[i][k_guess + 1]
            ))

            # Check if at least one blue-eyed individual seen by the islander has not left on day k_guess
            some_not_left_on_k = Or([
                And(blue_eyed[j], Not(leaves[j][k_guess])) for j in range(n) if j != i
            ])

            # If the islander sees exactly k_guess blue-eyed individuals, at least one of them has not left on day k_guess,
            # and the islander has not left yet, they deduce they must leave on day k_guess + 1
            s.add(Implies(
                And(seen_k, some_not_left_on_k, not_left_yet),
                leaves[i][k_guess + 1]
            ))


    # Solve and print results
    if s.check() == sat:
        m = s.model()
        print(f"Simulation (n={n}, k={k}):")
        timeline = [[] for _ in range(max_days)]
        blue_count = 0

        for i in range(n):
            is_blue = is_true(m.evaluate(blue_eyed[i], model_completion=True))
            if is_blue:
                blue_count += 1
            print(f"  Islander {i}: {'blue' if is_blue else 'brown'}")
            for day in range(max_days):
                if is_true(m.evaluate(leaves[i][day], model_completion=True)):
                    print(f"    Leaves on Day {day+1}")
                    timeline[day].append(i)
                    break

        print("\nTimeline:")
        for day in range(max_days):
            if timeline[day]:
                print(f"  Day {day+1}: Islanders {', '.join(map(str, timeline[day]))} leave")
            else:
                print(f"  Day {day+1}: No one leaves")

        print(f"\nSummary: {blue_count} blue-eyed left on day {k}, {n - blue_count} brown-eyed left on day {k + 1}")
    else:
        print("Unsatisfiable (contradiction in constraints)")

blue_eyed_islander()