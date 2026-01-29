def h_manhattan(board, goal_map):
    dist = 0
    n = len(board)
    for r in range(n):
        for c in range(n):
            val = board[r][c]
            if val != 0:
                tr, tc = goal_map[val]
                dist += abs(r - tr) + abs(c - tc)
    return dist

def h_misplaced(board, goal_map):
    count = 0
    n = len(board)
    for r in range(n):
        for c in range(n):
            val = board[r][c]
            if val != 0:
                tr, tc = goal_map[val]
                if (r, c) != (tr, tc):
                    count += 1
    return count