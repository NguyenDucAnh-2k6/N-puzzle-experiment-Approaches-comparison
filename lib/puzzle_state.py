class PuzzleState:
    def __init__(self, board, parent=None, move="", g=0, h=0):
        self.board = board
        self.parent = parent
        self.move = move
        self.g = g
        self.h = h
        self.f = g + h
        
        self.n = len(board)
        # Find blank (0)
        self.blank_pos = None
        for r in range(self.n):
            for c in range(self.n):
                if self.board[r][c] == 0:
                    self.blank_pos = (r, c)
                    break

    def __lt__(self, other):
        if self.f == other.f:
            return self.h < other.h
        return self.f < other.f
    
    def __eq__(self, other):
        return self.board == other.board
    
    def __hash__(self):
        return hash(str(self.board))

    def get_neighbors(self):
        neighbors = []
        r, c = self.blank_pos
        moves = [(-1, 0, "Up"), (1, 0, "Down"), (0, -1, "Left"), (0, 1, "Right")]
        
        for dr, dc, move_name in moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.n and 0 <= nc < self.n:
                new_board = [row[:] for row in self.board]
                new_board[r][c], new_board[nr][nc] = new_board[nr][nc], new_board[r][c]
                neighbors.append(PuzzleState(new_board, self, move_name, self.g + 1))
        return neighbors