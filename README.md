# ⋆˚⋆❀ 🐚🫧𓇼 ˖°SMT Wellesley Adventure ⋆｡˚❀ 🐚🫧𓇼°
<p align="center">
  <img src="https://github.com/user-attachments/assets/af51e851-bdbf-4fa7-a19d-401240af876d" width="300"/>
</p>

This was created as part of our final project for Wellesley CS 340 project. Follows a interactive story where players navigate through a series of word logic puzzles. We model the word puzzles through formal verification tools Z3 and Alloy. Our aim is to formally encode each puzzle’s constraints, verify solution correctness with solvers. At the end of the journey you are greeted with goose which will give you a **Pearl of Undecidability**.
   <img 
    src="https://github.com/user-attachments/assets/7b923448-b616-4467-ae06-9dafdc64ccc1" 
    alt="goose" 
    width="60"
  />
##  How to Use

We modeled puzzles using **Z3** and **Alloy**, and built an interactive front-end using **Flask** with connected HTML assets.

###  ────୨ৎ──── Requirements ────୨ৎ────

- Python 3.7+
- [Z3 Solver](https://github.com/Z3Prover/z3)
  ```bash
  pip install z3-solver
  ```
- [Alloy Analyzer](https://alloytools.org/) — required to run `.als` models

---

### ────୨ৎ──── Running Puzzle Solvers ────୨ৎ────

Navigate to the `goals/` folder to run individual logic puzzles modeled in **Z3** or Alloy:

```
FinalProject_CS340/
└── goals/
    ├── age.py            # Age riddle in Z3
    ├── lie.py            # Truth-teller puzzle in Z3
    ├── mislabled.py      # Mislabeled box puzzle in Z3
    └── river.als         # River crossing puzzle in Alloy
    └── blue-eye.py       # Blue-eyed islanders puzzle in Z3
    └── magicsquare.py    # Magic Square puzzle in Z3
```

To run a Z3 puzzle:
```bash
python goals/age.py
```

To run the river crossing puzzle:
- Download and open `river.als` in the Alloy Analyzer (requires installation of Alloy).
---

### ────୨ৎ──── Running the Interactive Game ────୨ৎ────

Deployed using render: https://finalproject-cs340.onrender.com

To play our interactive logic-based game built in **Flask**:

1. Navigate to the project root.
2. Run:

```bash
python website_storyline.py
```

3. Open your browser and go to:
```
http://127.0.0.1:5000
```

You’ll be able to interact with a story-driven puzzle experience combining logic, visuals, and dialogue.


---

## ⋆.˚ ☼⋆𓇼｡𖦹˙༄.° Project Goals ⋆.˚ ☼⋆𓇼｡𖦹˙༄.°


We focus on four categories:

### 1. ﹏𓊝﹏☼⋆.˚ River Crossing Puzzles ﹏𓊝﹏☼⋆.˚

These puzzles involve transporting people or items across a river under constraints (e.g., the cabbage can’t be left with the goat).  
🔧 Modeled using **Alloy**  
🔗 [River Crossing Puzzle – Wikipedia](https://en.wikipedia.org/wiki/River_crossing_puzzle)

<p align="center">
  <img src="https://github.com/user-attachments/assets/278f7b61-6f46-4e49-a0e3-5216d3353bfa" width="100"/>
  <img src="https://github.com/user-attachments/assets/8c1f688e-c99d-4bfe-8ef6-40424ca6536f" alt="farmer" width="100"/>
  <img src="https://github.com/user-attachments/assets/ac659e38-08a4-4e34-89e4-431345a92ecc" alt="fox" width="100"/>
  <img src="https://github.com/user-attachments/assets/ba109b69-ef32-453e-a720-b7337dfe7794" alt="goose" width="100"/>
  <img src="https://github.com/user-attachments/assets/3ad30c48-a19c-4667-89b8-063c3360916a" alt="lettuce" width="100"/>
</p>

### 2. ⋆༺𓆩⚔𓆪༻⋆ Lying and Truth-Teller Puzzles ⋆༺𓆩⚔𓆪༻⋆
Characters either lie or tell the truth. The goal is to use logic to deduce each character’s identity.  
🔧 Solved using **Z3**  
🔗 [Knights and Knaves – Wikipedia](https://en.wikipedia.org/wiki/Knights_and_Knaves)

### 3. (❀ˆᴗˆ)(•́ᴗ•̀✿) Age Riddles (❀ˆᴗˆ)(•́ᴗ•̀✿)
Puzzles involving relational age clues that require arithmetic reasoning.  
🔧 Solved using **Z3**  
🔗 [Ages of Three Children Puzzle – Wikipedia](https://en.wikipedia.org/wiki/Ages_of_Three_Children_puzzle)

### 4. ˙ ✩°˖🍊 ⋆｡˚꩜ Mislabeled Boxes ˙ ✩°˖ 🍎 ⋆｡˚꩜
Puzzle involves logical constraints, each box is assigned a label which does not match the actual value. You can peek inside one box, and the goal is to use logic to figure out what each box actually contains.
🔧 Solved using **Z3**  
🔗 [ Mislabeled Boxes - Mind Your Decisions](https://mindyourdecisions.com/blog/2025/02/16/apple-interview-question-mislabeled-boxes/).

### 5. Magic Squares
Squares with the sum of the rows, columns, and the main diagonals all equating the same number. You can fill in the blanks in a semi-revealed square, or try making your own and verifying it. 
🔧 Solved using **Z3** 

https://en.wikipedia.org/wiki/Magic_square

## Tradeoffs in Representation

###  ﹏𓊝﹏☼⋆.˚ River Crossing Puzzles ﹏𓊝﹏☼⋆.˚

We initially attempted to model this in **Z3**, but found it challenging to handle the state transitions clearly. Instead, we switched to **Alloy**, which allowed us to:

- Leverage temporal logic for time-based transitions
- Reuse patterns from classroom examples like:
  - Thread scheduling
  - Ring election protocol
  - Restore/delete file logic

Our Alloy model includes:
- Preconditions for crossing (farmer and item must be on the same side)
- An `init` state and valid trace logic
- Enforced progress (farmer must continue moving across the river)

This design prevents non-progressive behavior and ensures solution correctness.

### ⋆༺𓆩⚔𓆪༻⋆ Lying and Truth-Teller Puzzles ⋆༺𓆩⚔𓆪༻⋆
We used Z3 for the lying and truth-teller puzzles because they involve logical implications which are avaliable in Z3. 
- why not Alloy? Because Alloy mainly involves using sets which is not necessary for simply logic puzzles such as this one. 

###  (❀ˆᴗˆ)(•́ᴗ•̀✿) Age Riddles (❀ˆᴗˆ)(•́ᴗ•̀✿)
We chose Z3 for age riddles because they involve arithmetic constraints like sums, products, and inequalities between variables (e.g., "The sum of their ages is 13").
- Why Z3? It excels at solving numerical relationships using its built-in support for integer arithmetic and constraint solving.
- Why not Alloy? Alloy’s modeling of integers is limited and more cumbersome for arithmetic-heavy problems.

### 4. ˙ ✩°˖🍊 ⋆｡˚꩜ Mislabeled Boxes ˙ ✩°˖ 🍎 ⋆｡˚꩜
This puzzle is purely logical, with constraints like "the label is always wrong" and deduction from a single observation.
- Why Z3? It allows for clean, propositional logic modeling. We could express conditions like "label ≠ content" and apply constraints systematically.
- Why not Alloy? While Alloy can handle logic well, Z3’s first-order logic and solver feedback make it easier to express and verify small-scale logical deduction puzzles.

### 5. Magic Squares
We used Z3 for this model as it involves arithmetic operations on integers, whereas integer operations are rather limited in Alloy. 

---

##  Scope & Model Limitations

For the **River Crossing Puzzle**, we assumed it was solvable within **100 steps**, despite the fact that the optimal solution only requires **7 steps**.  
We selected 100 arbitrarily to ensure that Alloy’s bounded analysis wouldn’t miss any valid trace.

For the **Lying puzzle**, we limited the scope to only generate puzzles with the number of people between and including 3 and 5. Additionally, for each random variation of the puzzle generated with n people, we only generated n statements. These both limit the number of puzzles we are able to generate.

For the **Age puzzle**, we assumed that the product is between 1 to 100 and the sum of ages to be between 2 and 50. This limits the scope of the number of random problems our model can find. Additionally, when generating random variations, I limited the steps to 100—Z3* must find a solvable sum and product within this limit, or it will return undefined.

For the **Magic Squares** puzzle, we limited the size of a magic square a user can generate to 5, as having more rows and columns would take a while to generate. Additionally, for the generation of magic squares for users to solve, we limited the size of the square to 4, as similar to the user generated magic squares, it would take a while to generate all instances of the magic squares for us to grab and use as puzzles.

---

##  ⋆.˚ ☼⋆𓇼｡𖦹˙༄.° Goal Evolution ⋆.˚ ☼⋆𓇼｡𖦹˙༄.°
Initially we were only planning on adding 3 riddles but added another mislabled boxes to expand on the complexity of our project.

We initially thought the **river crossing puzzle** would be too difficult to model, especially in **Z3**, due to challenges in representing step-by-step transitions. However, switching to **Alloy** proved effective, and we learned:

- Z3 is better for arithmetic and propositional logic
- Alloy is more intuitive for modeling sequential, time-based systems

This experience helped us understand the strengths and limitations of different formal verification tools.


---

##  ˙༄.° Failed Attempts ⋆.˚ ☼⋆𓇼
We attempted to model the **water jug** puzzle in Alloy. This proved to be a difficult feat as there was kind of awkward arithmetic as the puzzle relies on being able to subtract and add amounts together pretty frequenetly and Alloy uses bounded integers as well so there was a small range of integers we could model. In the future this could be more easily modeled in Z3. Initially the thought was that this could be better for modeling the water jugs over time because of its use of time traces and its temporal logic capabilities. 

We also attempted to model **Blue eyed** puzzle in Z3. This proved to be difficult as it was akward to try to model logical reasoning and how beliefs changed, and representing what each person believes others believe. It's dynamic inference which makes it hard to model in z3. Direct rule (e.g., “leave on day k”) is easy to add, but it misses the point of the puzzle. Perhaps modeling in alloy would make it easier. For this particular puzzle it could have been easier to use Alloy because the model visualizations would have been more visually clear. An instance of the Alloy model would have shown the individuals on the island on the nth day, making it easier to visualze the day by day makeup of the island until the nth day. 

---

##  ˙༄.° Acknowledgements ⋆.˚ ☼⋆𓇼
The website creation process used generative AI. More specifically, the rivercrossing.html, style.css, and script.js, age.html, age.css used what was generated by GPT as a framework. It was used as a copiolet to code the outline of the website. The ideas we thought of ourselves, the execution step was aided by GPT where edits were made after by us like to the font, color, sizing, methods, time etc. 

---

