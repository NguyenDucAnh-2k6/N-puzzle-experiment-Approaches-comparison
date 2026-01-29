import heapq
import time
import random
import math
from collections import deque
from .puzzle_state import PuzzleState
from .utils import reconstruct_path

# --- SOLVERS ---

def solve_bfs(start_board, goal_board, goal_map, config):
    # CHANGE: Use dot notation for Pydantic model
    time_limit = config.time_limit 
    start_time = time.time()
    start_node = PuzzleState(start_board)
    
    queue = deque([start_node])
    visited = {tuple(tuple(r) for r in start_board)}
    
    nodes_expanded = 0
    max_memory = 0 
    
    while queue:
        current_mem = len(queue) + len(visited)
        if current_mem > max_memory: max_memory = current_mem

        current = queue.popleft()
        nodes_expanded += 1
        
        if current.board == goal_board:
            return reconstruct_path(current), nodes_expanded, max_memory, time.time() - start_time, 0
            
        if time.time() - start_time > time_limit:
            return None, nodes_expanded, max_memory, "> Limit", float('inf')

        for neighbor in current.get_neighbors():
            board_tuple = tuple(tuple(r) for r in neighbor.board)
            if board_tuple not in visited:
                visited.add(board_tuple)
                queue.append(neighbor)
                
    return None, nodes_expanded, max_memory, time.time() - start_time, float('inf')

def solve_astar(start_board, goal_board, goal_map, heuristic_func, config):
    # CHANGE: Dot notation
    time_limit = config.time_limit
    start_time = time.time()
    
    h_val = heuristic_func(start_board, goal_map)
    start_node = PuzzleState(start_board, h=h_val)
    
    open_list = []
    heapq.heappush(open_list, start_node)
    closed_set = set()
    
    nodes_expanded = 0
    max_memory = 0
    min_h = h_val

    while open_list:
        current_mem = len(open_list) + len(closed_set)
        if current_mem > max_memory: max_memory = current_mem

        current = heapq.heappop(open_list)
        nodes_expanded += 1
        if current.h < min_h: min_h = current.h

        if current.board == goal_board:
            return reconstruct_path(current), nodes_expanded, max_memory, time.time() - start_time, 0

        if time.time() - start_time > time_limit:
            return None, nodes_expanded, max_memory, "> Limit", current.h

        board_tuple = tuple(tuple(r) for r in current.board)
        if board_tuple in closed_set:
            continue
        closed_set.add(board_tuple)
        
        for neighbor in current.get_neighbors():
            neighbor_tuple = tuple(tuple(r) for r in neighbor.board)
            if neighbor_tuple not in closed_set:
                neighbor.h = heuristic_func(neighbor.board, goal_map)
                neighbor.f = neighbor.g + neighbor.h
                heapq.heappush(open_list, neighbor)
                
    return None, nodes_expanded, max_memory, time.time() - start_time, min_h

# --- BEAM SEARCH ---
def solve_beam_search(start_board, goal_board, goal_map, heuristic_func, config):
    # CHANGE: Dot notation
    time_limit = config.time_limit
    beam_width = config.beam_width
    start_time = time.time()
    
    h_val = heuristic_func(start_board, goal_map)
    start_node = PuzzleState(start_board, h=h_val)
    
    current_level = [start_node]
    visited = {tuple(tuple(r) for r in start_board)}
    
    nodes_expanded = 0
    max_memory = 0
    min_h = h_val
    
    while current_level:
        current_mem = len(current_level) + len(visited)
        if current_mem > max_memory: max_memory = current_mem

        best_in_level = min(current_level, key=lambda x: x.h)
        if best_in_level.h < min_h: min_h = best_in_level.h

        if time.time() - start_time > time_limit:
             return None, nodes_expanded, max_memory, "> Limit", min_h
             
        next_level_candidates = []
        
        for node in current_level:
            nodes_expanded += 1
            if node.board == goal_board:
                return reconstruct_path(node), nodes_expanded, max_memory, time.time() - start_time, 0
            
            for neighbor in node.get_neighbors():
                neighbor_tuple = tuple(tuple(r) for r in neighbor.board)
                if neighbor_tuple not in visited:
                    visited.add(neighbor_tuple)
                    neighbor.h = heuristic_func(neighbor.board, goal_map)
                    neighbor.f = neighbor.g + neighbor.h
                    next_level_candidates.append(neighbor)
        
        if not next_level_candidates:
            break

        next_level_candidates.sort(key=lambda x: x.f)
        current_level = next_level_candidates[:beam_width]
        
    return None, nodes_expanded, max_memory, time.time() - start_time, min_h

# --- RBFS ---
class RBFS_Stats:
    def __init__(self):
        self.nodes_expanded = 0
        self.max_memory = 0
        self.start_time = 0
        self.found = None
        self.min_h = float('inf')

def solve_rbfs(start_board, goal_board, goal_map, heuristic_func, config):
    stats = RBFS_Stats()
    stats.start_time = time.time()
    # CHANGE: Dot notation
    time_limit = config.time_limit
    
    h_val = heuristic_func(start_board, goal_map)
    stats.min_h = h_val
    start_node = PuzzleState(start_board, h=h_val)
    
    try:
        _rbfs_recursive(start_node, goal_board, goal_map, float('inf'), heuristic_func, stats, 0, time_limit)
    except RecursionError:
        return None, stats.nodes_expanded, stats.max_memory, "Rec. Error", stats.min_h
    
    if stats.found:
        return reconstruct_path(stats.found), stats.nodes_expanded, stats.max_memory, time.time() - stats.start_time, 0
    
    status = "> Limit" if (time.time() - stats.start_time > time_limit) else "FAILED"
    return None, stats.nodes_expanded, stats.max_memory, status, stats.min_h

def _rbfs_recursive(node, goal_board, goal_map, f_limit, h_func, stats, depth, time_limit):
    if time.time() - stats.start_time > time_limit:
        return None, float('inf')
    
    stats.nodes_expanded += 1
    if depth > stats.max_memory: stats.max_memory = depth

    if node.h < stats.min_h: stats.min_h = node.h
    if node.board == goal_board:
        stats.found = node
        return node, node.f

    neighbors = node.get_neighbors()
    if not neighbors: return None, float('inf')

    for child in neighbors:
        child.h = h_func(child.board, goal_map)
        child.f = max(child.g + child.h, node.f)
    
    neighbors.sort(key=lambda x: x.f)
    
    while True:
        if time.time() - stats.start_time > time_limit: return None, float('inf')

        best = neighbors[0]
        if best.f > f_limit: return None, best.f
        
        alternative = neighbors[1].f if len(neighbors) > 1 else float('inf')
        result, best.f = _rbfs_recursive(best, goal_board, goal_map, min(f_limit, alternative), h_func, stats, depth+1, time_limit)
        
        if result is not None: return result, best.f
        neighbors.sort(key=lambda x: x.f)

# --- HILL CLIMBING ---
def solve_hill_climbing(start_board, goal_board, goal_map, heuristic_func, config):
    # CHANGE: Dot notation
    time_limit = config.time_limit
    start_time = time.time()
    
    h_val = heuristic_func(start_board, goal_map)
    current = PuzzleState(start_board, h=h_val)
    
    visited = {tuple(tuple(r) for r in start_board)}
    nodes_expanded = 0
    max_memory = 0
    
    while True:
        current_mem = 1 + len(visited) 
        if current_mem > max_memory: max_memory = current_mem
        
        if time.time() - start_time > time_limit:
            return None, nodes_expanded, max_memory, "> Limit", current.h
        
        nodes_expanded += 1
        if current.board == goal_board:
            return reconstruct_path(current), nodes_expanded, max_memory, time.time() - start_time, 0

        neighbors = current.get_neighbors()
        best_neighbor = None
        
        for neighbor in neighbors:
            neighbor_tuple = tuple(tuple(r) for r in neighbor.board)
            if neighbor_tuple not in visited:
                neighbor.h = heuristic_func(neighbor.board, goal_map)
                if best_neighbor is None or neighbor.h < best_neighbor.h:
                    best_neighbor = neighbor
        
        if best_neighbor is None:
            return None, nodes_expanded, max_memory, "Local Max", current.h
        
        visited.add(tuple(tuple(r) for r in best_neighbor.board))
        current = best_neighbor

def solve_random_restart_hill_climbing(start_board, goal_board, goal_map, heuristic_func, config):
    # CHANGE: Dot notation & Nested Config Access
    time_limit = config.time_limit
    
    # Access nested 'hill_climbing' config object
    params = config.hill_climbing 
    max_restarts = params.max_restarts
    min_scramble = params.min_scramble
    max_scramble = params.max_scramble

    overall_start_time = time.time()
    nodes_expanded = 0
    max_memory = 0
    best_h_found = float('inf')

    for attempt in range(max_restarts):
        if time.time() - overall_start_time > time_limit:
            return None, nodes_expanded, max_memory, "> Limit", best_h_found

        # Restart
        current = PuzzleState(start_board, h=heuristic_func(start_board, goal_map))
        visited = {tuple(tuple(r) for r in current.board)}
        
        # Scramble
        scramble_steps = random.randint(min_scramble, max_scramble)
        for _ in range(scramble_steps):
            neighbors = current.get_neighbors()
            unvisited = [n for n in neighbors if tuple(tuple(r) for r in n.board) not in visited]
            next_node = random.choice(unvisited) if unvisited else random.choice(neighbors)
            
            next_node.h = heuristic_func(next_node.board, goal_map)
            visited.add(tuple(tuple(r) for r in next_node.board))
            current = next_node
            nodes_expanded += 1
            if current.board == goal_board:
                return reconstruct_path(current), nodes_expanded, max_memory, time.time() - overall_start_time, 0

        # Climb
        while True:
            if current.g > max_memory: max_memory = current.g
            if current.h < best_h_found: best_h_found = current.h

            if time.time() - overall_start_time > time_limit:
                return None, nodes_expanded, max_memory, "> Limit", best_h_found

            if current.board == goal_board:
                return reconstruct_path(current), nodes_expanded, max_memory, time.time() - overall_start_time, 0
            
            neighbors = current.get_neighbors()
            nodes_expanded += 1
            best_neighbor = None
            best_neighbor_h = float('inf')

            for n in neighbors:
                n_tuple = tuple(tuple(r) for r in n.board)
                if n_tuple in visited: continue
                n.h = heuristic_func(n.board, goal_map)
                if n.h < best_neighbor_h:
                    best_neighbor = n
                    best_neighbor_h = n.h
            
            if best_neighbor and best_neighbor_h < current.h:
                visited.add(tuple(tuple(r) for r in best_neighbor.board))
                current = best_neighbor
            else:
                break 

    return None, nodes_expanded, max_memory, "Max Restarts", best_h_found

# --- SIMULATED ANNEALING ---
def solve_simulated_annealing(start_board, goal_board, goal_map, heuristic_func, config):
    # CHANGE: Dot notation & Nested Config Access
    time_limit = config.time_limit
    
    # Access nested 'simulated_annealing' config object
    params = config.simulated_annealing
    start_time = time.time()
    
    target_iterations = params.target_iterations
    current_temp = params.start_temp
    min_temp = params.min_temp
    cooling_rate = (min_temp / current_temp) ** (1 / target_iterations)

    h_val = heuristic_func(start_board, goal_map)
    current = PuzzleState(start_board, h=h_val)
    best_node = current
    
    nodes_expanded = 0
    max_memory = 1
    
    while current_temp > min_temp:
        if time.time() - start_time > time_limit:
            return None, nodes_expanded, max_memory, "> Limit", best_node.h
        
        if current.board == goal_board:
            return reconstruct_path(current), nodes_expanded, max_memory, time.time() - start_time, 0
        
        nodes_expanded += 1
        neighbors = current.get_neighbors()
        if not neighbors: break 
            
        next_node = random.choice(neighbors)
        next_node.h = heuristic_func(next_node.board, goal_map)
        
        delta_E = next_node.h - current.h
        
        should_accept = False
        if delta_E < 0:
            should_accept = True
        else:
            probability = math.exp(-delta_E / current_temp)
            if random.random() < probability:
                should_accept = True
        
        if should_accept:
            current = next_node
            if current.h < best_node.h:
                best_node = current
                
        current_temp *= cooling_rate
        if current.g > max_memory: max_memory = current.g

    if best_node.board == goal_board:
        return reconstruct_path(best_node), nodes_expanded, max_memory, time.time() - start_time, 0

    return None, nodes_expanded, max_memory, "Frozen", best_node.h

# --- IDDFS ---
def solve_iddfs(start_board, goal_board, goal_map, config):
    # CHANGE: Dot notation
    time_limit = config.time_limit
    start_time = time.time()
    nodes_expanded = 0
    depth_limit = 0
    max_memory = 0
    last_h = float('inf')

    while True:
        if time.time() - start_time > time_limit:
            return None, nodes_expanded, max_memory, "> Limit", last_h
            
        result, count, run_mem, run_last_h = dls(start_board, goal_board, depth_limit, start_time, goal_map, time_limit)
        
        nodes_expanded += count
        if run_mem > max_memory: max_memory = run_mem
        last_h = run_last_h 
        
        if result is not None:
             return result, nodes_expanded, max_memory, time.time() - start_time, 0
        
        depth_limit += 1

def dls(current_board, goal_board, limit, start_time, goal_map, time_limit):
    path_set = set()
    from .heuristics import h_manhattan # Local import to avoid cycle if any
    return recursive_dls(PuzzleState(current_board), goal_board, limit, path_set, start_time, goal_map, time_limit, h_manhattan)

def recursive_dls(node, goal_board, limit, path_set, start_time, goal_map, time_limit, h_func):
    count = 1
    current_mem = len(path_set) + 1
    max_mem = current_mem
    current_h = h_func(node.board, goal_map)

    if node.board == goal_board:
        return reconstruct_path(node), count, max_mem, 0
    
    if limit <= 0:
        return None, count, max_mem, current_h

    if time.time() - start_time > time_limit:
        return None, count, max_mem, current_h

    board_tuple = tuple(tuple(r) for r in node.board)
    path_set.add(board_tuple)

    for neighbor in node.get_neighbors():
        neighbor_tuple = tuple(tuple(r) for r in neighbor.board)
        if neighbor_tuple not in path_set:
            result, child_count, child_mem, child_h = recursive_dls(neighbor, goal_board, limit-1, path_set, start_time, goal_map, time_limit, h_func)
            
            count += child_count
            current_h = child_h
            if child_mem > max_mem: max_mem = child_mem
                
            if result is not None:
                return result, count, max_mem, 0
                
    path_set.remove(board_tuple)
    return None, count, max_mem, current_h