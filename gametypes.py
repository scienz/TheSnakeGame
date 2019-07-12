from enum import Enum

class CellType(Enum):
    EMPTY = 1
    FOOD = 2
    SNAKEPART = 3

class DirectionType(Enum):
    LEFT = 1
    RIGHT = 2
    TOP = 3
    BOTTOM = 4

class GameMode(Enum):
    AUTO = 1
    MANUAL = 2