from enum import Enum

class GameState(Enum):
    OFF = 0
    WAITING = 1
    ONGOING = 2
    PAUSED = 3
    CANCELLED = 4
    FINISHED = 5