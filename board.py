from cell import Cell, CellState
from random import randint

class Board:
    def __init__(self, size: int, bomb_count: int) -> None:
        self.size = size
        self.bomb_count = bomb_count
        self.cells = [[Cell() for y in range(size)] for x in range(size)]

        # Place the bombs
        bombs_left_to_place = bomb_count
        while bombs_left_to_place > 0:
            bomb_x = randint(0, self.size - 1)
            bomb_y = randint(0, self.size - 1)
            if self.cells[bomb_x][bomb_y].is_bomb:
                continue
            self.cells[bomb_x][bomb_y].is_bomb = True
            bombs_left_to_place -= 1

        # Update the number of neighbors
        for x, row in enumerate(self.cells):
            for y, cell in enumerate(row):
                number_of_neighboring_mines = 0
                number_of_neighboring_mines += (x > 0 and y > 0) and self.cells[x - 1][y - 1].is_bomb
                number_of_neighboring_mines += (x > 0) and self.cells[x - 1][y].is_bomb
                number_of_neighboring_mines += (x > 0 and y < self.size - 1) and self.cells[x - 1][y + 1].is_bomb
                number_of_neighboring_mines += (y > 0) and self.cells[x][y - 1].is_bomb
                number_of_neighboring_mines += (y < self.size - 1) and self.cells[x][y + 1].is_bomb
                number_of_neighboring_mines += (x < self.size - 1 and y > 0) and self.cells[x + 1][y - 1].is_bomb
                number_of_neighboring_mines += (x < self.size - 1) and self.cells[x + 1][y].is_bomb
                number_of_neighboring_mines += ((x < self.size - 1 and y < self.size - 1) and
                    self.cells[x + 1][y + 1].is_bomb)
                cell.number_of_neighboring_mines = number_of_neighboring_mines