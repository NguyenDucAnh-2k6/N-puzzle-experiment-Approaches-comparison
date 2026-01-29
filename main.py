# puzzle_experiment/main.py
import sys
import os

# 1. Setup path to import local modules from the 'lib' folder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 2. IMPORT CONFIG & SETUP OBJECTS DIRECTLY
# (Do not use json.load anymore)
from config import config
from puzzle_setup import puzzle_setup

# 3. Import Logic
from lib.utils import is_solvable
from lib.heuristics import h_manhattan, h_misplaced
from lib.solvers import (
    solve_bfs, solve_astar, solve_beam_search, solve_rbfs, 
    solve_hill_climbing, solve_random_restart_hill_climbing, 
    solve_simulated_annealing, solve_iddfs
)

def run_pipeline():
    print("\n--- N-Puzzle Solver Pipeline ---")
    
    # --- CHANGE: Access via Dot Notation ---
    # config is now an Object, not a Dictionary
    print(f"Loaded Configuration: Time Limit={config.time_limit}s")
    
    start_state = puzzle_setup.start_state
    goal_state = puzzle_setup.goal_state

    if not is_solvable(start_state, goal_state):
        print("Error: Puzzle is Unsolvable!")
        return

    # Precompute goal map
    goal_map = {}
    n = len(goal_state)
    for r in range(n):
        for c in range(n):
            goal_map[goal_state[r][c]] = (r, c)

    # 4. Define Solvers
    # Pass the 'config' OBJECT to solvers
    solvers = [
        ("BFS", lambda: solve_bfs(start_state, goal_state, goal_map, config)),
        ("IDDFS", lambda: solve_iddfs(start_state, goal_state, goal_map, config)),
        ("A* (Misplaced)", lambda: solve_astar(start_state, goal_state, goal_map, h_misplaced, config)),
        ("A* (Manhattan)", lambda: solve_astar(start_state, goal_state, goal_map, h_manhattan, config)),
        (f"Beam (k={config.beam_width}, Manh)", lambda: solve_beam_search(start_state, goal_state, goal_map, h_manhattan, config)),
        (f"Beam (k={config.beam_width}, Misplaced)", lambda: solve_beam_search(start_state, goal_state, goal_map, h_misplaced, config)),
        ("RBFS (Misplaced)", lambda: solve_rbfs(start_state, goal_state, goal_map, h_misplaced, config)),
        ("RBFS (Manhattan)", lambda: solve_rbfs(start_state, goal_state, goal_map, h_manhattan, config)),
        ("Hill Climbing", lambda: solve_hill_climbing(start_state, goal_state, goal_map, h_manhattan, config)),
        ("Hill Climb (Rnd Restart)", lambda: solve_random_restart_hill_climbing(start_state, goal_state, goal_map, h_manhattan, config)),
        ("Sim. Annealing", lambda: solve_simulated_annealing(start_state, goal_state, goal_map, h_manhattan, config))
    ]

    # 5. Run & Print
    print(f"\n{'-'*120}")
    print(f"{'Algorithm':<22} | {'Status':<10} | {'Moves':<5} | {'Nodes Exp.':<10} | {'Max Mem':<10} | {'Final h':<8} | {'Time (s)':<10}")
    print(f"{'-'*120}")

    for name, func in solvers:
        path, nodes, max_mem, runtime, final_h = func()
        
        if isinstance(runtime, str): 
            status = "FAILED" if runtime != "> Limit" else "TIMEOUT"
            if runtime == "Local Max": status = "STUCK"
            moves = "-"
            time_str = f"{runtime}"
        elif path is None:
            status = "FAILED"
            moves = "-"
            time_str = f"{runtime:.4f}"
        else:
            status = "SOLVED"
            moves = len(path)
            time_str = f"{runtime:.4f}"
            
        print(f"{name:<22} | {status:<10} | {str(moves):<5} | {str(nodes):<10} | {str(max_mem):<10} | {str(final_h):<8} | {time_str:<10}")

    print(f"{'-'*120}")

if __name__ == "__main__":
    run_pipeline()