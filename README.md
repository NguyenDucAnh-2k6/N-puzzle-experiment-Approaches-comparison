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