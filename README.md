2. Running the ExperimentTo run the full pipeline of solvers on the current configuration:Bashpython main.py
⚙️ ConfigurationThis project avoids hardcoded values by using two external configuration files. You can modify these files to change the experiment setup without touching the core logic.1. Modifying the Puzzle (puzzle_setup.py)Edit this file to set your Start State and Goal State.Validation: The system automatically checks if the board is a perfect square (NxN) and contains a valid sequence of numbers (0 to $N^2-1$).Python# puzzle_setup.py
puzzle_setup = PuzzleSetup(
    start_state=[
        [7, 2, 4],
        [5, 0, 6],
        [8, 3, 1]
    ],
    goal_state=[
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8]
    ]
)
2. Tuning Algorithms (config.py)Edit this file to tweak search parameters like time limits, beam width, or cooling rates.Validation: Pydantic ensures values are the correct type (e.g., preventing string inputs for integers).Python# config.py
config = PuzzleConfig(
    time_limit=1000,   # Max runtime in seconds
    beam_width=100,    # Nodes to keep in memory for Beam Search

    # Nested configuration for specific algorithms
    simulated_annealing=SimulatedAnnealingConfig(
        target_iterations=500000,
        start_temp=100.0
    ),
    hill_climbing=HillClimbingConfig(
        max_restarts=1000  # Number of random restarts if stuck
    )
)
📂 Project StructurePlaintextpuzzle_experiment/
├── config.py           # Algorithm parameter configuration (Pydantic)
├── puzzle_setup.py     # Board state configuration (Pydantic)
├── main.py             # Entry point script
├── lib/
│   ├── solvers.py      # Implementation of all search algorithms
│   ├── heuristics.py   # Manhattan and Misplaced tile functions
│   ├── puzzle_state.py # State representation class
│   └── utils.py        # Helper functions
└── README.md           # Documentation
# N‑Puzzle Solver Framework

A modular Python framework for benchmarking search algorithms on the N‑Puzzle (8‑puzzle, 15‑puzzle, etc.). The project includes uninformed, informed (heuristic), and local search strategies and a Pydantic-based configuration system for safe, editable experiment setups.

## Features

- **Solver suite:** BFS, IDDFS, A*, Beam Search, RBFS, Hill Climbing, Simulated Annealing.
- **Metrics:** Execution time, nodes expanded, peak memory usage, solution path length.
- **Type-safe configuration:** Uses Pydantic to validate algorithm and puzzle settings.
- **Modular codebase:** Solvers, heuristics, and state logic are separated under `lib/`.

## Algorithms (brief)

- **BFS (Breadth‑First Search)** — level‑by‑level search. Pros: optimal. Cons: high memory usage ($O(b^d)$).
- **IDDFS (Iterative Deepening DFS)** — repeated DFS with increasing depth limits. Pros: optimal, low memory ($O(bd)$). Cons: repeated expansions.
- **A\*** — best‑first with $f(n)=g(n)+h(n)$. Uses Manhattan or Misplaced Tiles heuristics. Pros: optimal with admissible heuristic. Cons: can use lots of memory.
- **Beam Search** — keeps the best $k$ nodes per level (beam width). Pros: fast, low memory. Cons: not optimal or complete.
- **RBFS (Recursive Best‑First Search)** — A* variant that uses linear space. Pros: lower memory. Cons: may re‑generate nodes frequently.
- **Hill Climbing** — greedy local search. Pros: very fast. Cons: can get stuck in local optima.
- **Simulated Annealing** — probabilistic local search accepting worse moves to escape optima. Pros: can escape local optima. Cons: slower and typically suboptimal solutions.

## Installation

Requires Python 3.8+. Install runtime dependency used for validation:

```bash
pip install pydantic
```

Optionally create a `requirements.txt` if you want a pinned environment.

## Running the experiment

Run the full pipeline with the repository's entrypoint:

```bash
python main.py
```

The script reads configuration from the project files and runs the configured solvers on the puzzle specified in the setup.

## Configuration

All experiment parameters live in two editable files at the repository root:

- Puzzle definition: [puzzle_setup.py](puzzle_setup.py)
- Algorithm parameters: [config.py](config.py)

Edit these files to change behavior — Pydantic models validate input and will raise helpful errors when values are invalid.

### Puzzle example (`puzzle_setup.py`)

Set the start and goal board states as nested lists. The system checks that the board is square and contains the correct tile set (0..N^2-1):

```python
from puzzle_setup import PuzzleSetup

puzzle_setup = PuzzleSetup(
    start_state=[
        [7, 2, 4],
        [5, 0, 6],
        [8, 3, 1]
    ],
    goal_state=[
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8]
    ]
)
```

### Algorithm tuning (`config.py`)

Adjust global limits and per‑algorithm settings here. Example:

```python
from config import PuzzleConfig, SimulatedAnnealingConfig, HillClimbingConfig

config = PuzzleConfig(
    time_limit=1000,        # seconds
    beam_width=100,         # for Beam Search

    simulated_annealing=SimulatedAnnealingConfig(
        target_iterations=500000,
        start_temp=100.0,
    ),

    hill_climbing=HillClimbingConfig(
        max_restarts=1000,
    ),
)
```

Pydantic type validation helps prevent misconfiguration (for example, strings for numeric fields).

## Project structure

```
puzzle_experiment/
├── config.py           # Algorithm parameter configuration (Pydantic)
├── puzzle_setup.py     # Board state configuration (Pydantic)
├── main.py             # Entry point script
├── lib/
│   ├── solvers.py      # Search algorithm implementations
│   ├── heuristics.py   # Manhattan / Misplaced heuristics
│   ├── puzzle_state.py # State representation, moves, goal test
│   └── utils.py        # Helpers and metrics
└── README.md           # This documentation
```

## Tips & next steps

- For quick experiments, reduce `time_limit` and prefer Beam or Hill Climbing to get results fast.
- Add a `requirements.txt` if you plan to share the environment or run in CI.
- If you want, I can add a small example `puzzle_setup.py` and a `requirements.txt` and then run `python main.py` to smoke‑test the pipeline.

---

If you want any wording changed or extra examples (visualization, logging, CI), tell me which and I will add them.