This project aims to model and solve classic word logic puzzles using formal
verification tools Z3 and Alloy. Our goal is to formally encode each puzzle’s
constraints, verify their solutions’ correctness using the solvers, and explore
possible variations or extensions. More specifically, we want to model 3 word
logic puzzles. The first is the river crossing problem, the second is the lying
and truth-teller puzzles, and the third is age riddles. We will focus on three
categories, but may add more if time permits:


• River Crossing Puzzles – These involve transporting people or items
across a river with specific constraints (e.g., the Cabbage can’t be left with
the Goat). We will model variations of these problems and verify valid
sequences of moves using Alloy
https://en.wikipedia.org/wiki/River%20crossing%20puzzle


• Lying and Truth-teller Puzzles – In these puzzles, characters make
statements and may either lie or tell the truth. We will use Z3 to reason
about the consistency of their statements and determine each character’s
role.
https://en.wikipedia.org/wiki/Knights%20and%20Knaves


• Age Riddles – These include relational age clues and require arithmetic
reasoning. We will model these constraints using z3 to deduce the solution.
https://en.wikipedia.org/wiki/Ages%20of%20Three%20Children%20puzzle
By modeling each type of puzzle, we aim to explore how formal logic and
constraint solving can be used to verify and solve reasoning tasks commonly
expressed in natural language
