# Word Riddles Final Project CS340

## Project Goals
This project aims to model and solve classic word logic puzzles using formal 
verification tools Z3 and Alloy. Our goal is to formally encode each puzzle’s
   constraints, verify their solutions’ correctness using the solvers, and explore
   possible variations or extensions. More specifically, we want to model 3 word
   logic puzzles. The first is the river crossing problem, the second is the lying
   and truth-teller puzzles, and the third is age riddles. We will focus on three
   categories, but may add more if time permits:
### River Crossing Puzzles – These involve transporting people or items
   across a river with specific constraints (e.g., the Cabbage can’t be left with
   the Goat). We will model variations of these problems and verify valid
   sequences of moves using Alloy
   https://en.wikipedia.org/wiki/River%20crossing%20puzzle
### Lying and Truth-teller Puzzles – In these puzzles, characters make
   statements and may either lie or tell the truth. We will use Z3 to reason
   about the consistency of their statements and determine each character’s
   role.
   https://en.wikipedia.org/wiki/Knights%20and%20Knaves
### Age Riddles – These include relational age clues and require arithmetic
   reasoning. We will model these constraints using z3 to deduce the solution.
   https://en.wikipedia.org/wiki/Ages%20of%20Three%20Children%20puzzle
   By modeling each type of puzzle, we aim to explore how formal logic and
   constraint solving can be used to verify and solve reasoning tasks commonly
   expressed in natural language

### What tradeoffs did you make in choosing your representation? What else did you try that didn’t work as well?
   River problem: We were originally going to model the river crossing problem in z3. But we realized this may be a lot harder so we chose to do our representation in Alloy instead because we thought the modling would be a lot more clear. Because of the built in features of temporal logic within alloy, we believed it would be so much easier. It was hard for us to decide how exactly we wanted to represent everything when we initially tried in z3. We weren't sure whether to keep a list for each of the farmer, cabbage, wolf, and goat at each time step and iterate through that loop indefinitely. While it would not be impossible to use z3 we had the idea to instead use Alloy because we got so much practice using temporal operators when working with threads, the ring election lab, or even when looking at the restoring and delting files example from the classroom. The model we ended up using for the river problem took a lot of the logic from the restore and delete files, and especially the logic behind the preconditions when it came to crossing the river forward or backwards (where both the farmer and the other item had to start on the same side), and especially having an init statement as well as the valid traces. Another tecnique we pulled from class was the fact that progress has to be made at every step and only when they are all at the other side we do nothing. Similar to the thread example we are forcing progress to be made, meaning the farmer must go back and forth and can't just chill on one side of the bridge doing nothing.

### What assumptions did you make about scope? What are the limits of your model?
   River crossing problem: we made the assumption that this was a solvable problem and could be solved within 100 stpes. Because alloy needs to be given a scope to check over we decided on 100 randomly, but this puzzle can be solved in 7 steps.
   
### Did your goals change at all from your proposal? Did you realize anything you planned was unrealistic, or that anything you thought was unrealistic was doable?

River problem: At first with the river problem we thought it would be impossible to model because we were having a hard time figuring out how we wanted to mdoel everything in Z3.

