# puzzle_experiment/config.py
from pydantic import BaseModel, Field

class SimulatedAnnealingConfig(BaseModel):
    target_iterations: int = Field(200000, description="How many iterations to run")
    start_temp: float = 100.0
    min_temp: float = 0.5

class HillClimbingConfig(BaseModel):
    max_restarts: int = 1000
    min_scramble: int = 5
    max_scramble: int = 20

class PuzzleConfig(BaseModel):
    # Top level config
    time_limit: int = Field(1000, gt=0, description="Max runtime in seconds")
    beam_width: int = Field(100, gt=0, description="Nodes to keep in memory")
    
    # Nested configs
    simulated_annealing: SimulatedAnnealingConfig = SimulatedAnnealingConfig()
    hill_climbing: HillClimbingConfig = HillClimbingConfig()

# Create the instance
# Users can edit values right here
config = PuzzleConfig(
    time_limit=1000, # User changed this
    beam_width=100,
    simulated_annealing=SimulatedAnnealingConfig(
        target_iterations=500000 # User increased this
    )
)