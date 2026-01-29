# puzzle_experiment/puzzle_setup.py
from pydantic import BaseModel, field_validator, ValidationInfo
from typing import List

class PuzzleSetup(BaseModel):
    start_state: List[List[int]]
    goal_state: List[List[int]]

    # --- VALIDATOR: Ensures board is valid (Square & Correct Numbers) ---
    @field_validator('start_state', 'goal_state')
    @classmethod
    def validate_board(cls, board: List[List[int]], info: ValidationInfo) -> List[List[int]]:
        field_name = info.field_name
        
        # 1. Check if empty
        if not board:
            raise ValueError(f"{field_name} cannot be empty")

        # 2. Check dimensions (must be square NxN)
        n = len(board)
        for i, row in enumerate(board):
            if len(row) != n:
                raise ValueError(f"{field_name}: Row {i} has length {len(row)}, expected {n}. Board must be square.")

        # 3. Check values (Must contain 0 to N^2-1 exactly)
        flat_board = [cell for row in board for cell in row]
        expected_set = set(range(n * n))
        actual_set = set(flat_board)

        if actual_set != expected_set:
            missing = expected_set - actual_set
            extra = actual_set - expected_set
            raise ValueError(f"{field_name}: Invalid values. Missing: {missing}, Unexpected: {extra}")

        return board

# --- INSTANCE: User edits this part ---
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