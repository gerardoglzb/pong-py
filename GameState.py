from enum import Enum

class GameState(Enum):
    OFF = 0
    WAITING = 1,
    ONGOING = 2,
    CANCELLED = 3,
    FINISHED = 4