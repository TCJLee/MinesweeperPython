from enum import Enum

class CellState(Enum):
    HIDDEN = 0
    REVEALED = 1
    FLAGGED = 2


class Cell:
    def __init__(self) -> None:
        self.state = CellState.HIDDEN
        self.is_bomb = False
        self.number_of_neighboring_mines = 0