# SMT Wellesely Adventure
This was created as part of our final project for Wellesley CS 340 project. Follows a interactive story where players naviagate through a series of word logic puzzzles.

## How to Use
How to install required tools (you can link to tool pages for the main instructions).

##  Project Goals

This project models and solves classic word logic puzzles using formal verification tools **Z3** and **Alloy**. Our aim is to formally encode each puzzle’s constraints, verify solution correctness with solvers, and explore variations or extensions.

We focus on three categories:

### 1. 🛶 River Crossing Puzzles
These puzzles involve transporting people or items across a river under constraints (e.g., the cabbage can’t be left with the goat).  
🔧 Modeled using **Alloy**  
🔗 [River Crossing Puzzle – Wikipedia](https://en.wikipedia.org/wiki/River_crossing_puzzle)

### 2. 🗣️ Lying and Truth-Teller Puzzles
Characters either lie or tell the truth. The goal is to use logic to deduce each character’s identity.  
🔧 Solved using **Z3**  
🔗 [Knights and Knaves – Wikipedia](https://en.wikipedia.org/wiki/Knights_and_Knaves)

### 3. 🎂 Age Riddles
Puzzles involving relational age clues that require arithmetic reasoning.  
🔧 Solved using **Z3**  
🔗 [Ages of Three Children Puzzle – Wikipedia](https://en.wikipedia.org/wiki/Ages_of_Three_Children_puzzle)

By modeling these puzzle types, we explore how formal logic and constraint solving can address reasoning tasks typically expressed in natural language.

---

## ⚖️ Tradeoffs in Representation

### River Crossing Puzzle

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

---

## 🔍 Scope & Model Limitations

For the **River Crossing Puzzle**, we assumed it was solvable within **100 steps**, despite the fact that the optimal solution only requires **7 steps**.  
We selected 100 arbitrarily to ensure that Alloy’s bounded analysis wouldn’t miss any valid trace.

---

## 🔄 Goal Evolution

We initially thought the **river crossing puzzle** would be too difficult to model, especially in **Z3**, due to challenges in representing step-by-step transitions. However, switching to **Alloy** proved effective, and we learned:

- Z3 is better for arithmetic and propositional logic
- Alloy is more intuitive for modeling sequential, time-based systems

This experience helped us understand the strengths and limitations of different formal verification tools.

---


