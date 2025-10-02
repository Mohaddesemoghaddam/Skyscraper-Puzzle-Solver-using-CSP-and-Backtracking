# Skyscraper Puzzle Solver with CSP & Heuristics

This project implements a solver for the **Skyscraper Puzzle** using 
Constraint Satisfaction Problem (CSP) techniques and heuristic strategies.

The **Skyscraper Puzzle** is a logic-based grid game where each row and 
column must contain unique values from `1` to the grid size. Clues around 
the grid indicate how many buildings are visible from that side. Taller 
buildings block shorter ones behind them. The solution must satisfy both 
**uniqueness** and **visibility** constraints.

---

Installation
------------

Clone the repository and install the dependencies:

```bash
pip install -r requirements.txt
```

---

Project Structure
-----------------

* **CSP.py** → Defines the CSP class and helper functions for CSP problems  
* **Solver.py** → Algorithms and heuristics for solving the puzzle  
* **graphics.py** → Visualization functions for displaying solutions  
* **test_case_generator.py** → Generates puzzle grids of arbitrary size  
* **main.py** → Entry point to run the solver with user-defined parameters  

---

Parameters
----------

* `-m, --map` → Specifies the puzzle map to solve  
* `-lcv, --lcv` → Enable **Least Constraining Value (LCV)** heuristic  
* `-mrv, --mrv` → Enable **Minimum Remaining Values (MRV)** heuristic  
* `-MAC, --maintaining_arc_consistency` → Enforce arc consistency by pruning invalid values  

---

Usage
-----

Run the solver via `main.py` with custom parameters.

### Example 1: Solve map 3 with LCV and MRV
```bash
python3 main.py -m3 -lcv -mrv
```

### Example 2: Solve map 2 with LCV, MRV, and Arc Consistency
```bash
python3 main.py -m2 -lcv -mrv -MAC
```

After each run, the number of assignments is displayed, allowing you to  
compare the effectiveness of different heuristics.

---

Key Features
------------

* CSP-based solver with heuristics (LCV, MRV)  
* Support for arc consistency to reduce search space  
* Visualization of solutions  
* Test case generator for arbitrary grid sizes  

---
