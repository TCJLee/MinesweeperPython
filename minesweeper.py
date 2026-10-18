from board import Board
from cell import CellState
import tkinter as tk
from tkinter import messagebox

class Minesweeper:

    def __init__(self, root: tk.Tk, size: int, bomb_count: int) -> None:
        self.root = root
        self.board = Board(size, bomb_count)
        self._num_of_revealed = 0
        self._num_of_flagged = 0

        # UI creation
        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10)
        self.bomb_counter = tk.Label(self.root, text=f"0/{bomb_count}")
        self.bomb_counter.pack()
        self.buttons: list[list[tk.Button]] = []
        self._create_widgets()

    def _create_widgets(self) -> None:
        for x in range(self.board.size):
            row = []
            for y in range(self.board.size):
                btn = tk.Button(self.frame, width=2, height=1, bg="light gray",
                    command=lambda x=x, y=y: self._reveal_cell(x, y))
                btn.bind("<Button-3>", lambda e, x=x, y=y: self._toggle_flag(x, y))
                btn.grid(row=x, column=y)
                row.append(btn)
            self.buttons.append(row)

    def _reveal_cell(self, x: int, y: int) -> None:
        cell = self.board.cells[x][y]
        if cell.is_bomb:
            self.buttons[x][y].config(bg = "red", text = "\U0001f4a3", fg="black") # bomb emoji
            messagebox.showinfo("Result", "You lost!")
            self.root.quit()
        else:
            self._reveal_recursive(x, y)
            self._check_win()

    def _check_win(self) -> None:
        if self._num_of_revealed == (self.board.size ** 2) - self.board.bomb_count:
            messagebox.showinfo("Result", "You won!")
            self.root.quit()

    def _toggle_flag(self, x: int, y: int) -> None:
        cell = self.board.cells[x][y]
        if cell.state == CellState.HIDDEN:
            cell.state = CellState.FLAGGED
            self.buttons[x][y].config(text="\U0001f6a9", fg="red") # flag emoji
            self._num_of_flagged += 1
        elif cell.state == CellState.FLAGGED:
            cell.state = CellState.HIDDEN
            self.buttons[x][y].config(text="")
            self._num_of_flagged -= 1
        self.bomb_counter.config(text=f"{self._num_of_flagged}/{self.board.bomb_count}")

    def _reveal_recursive(self, x: int, y: int) -> None:
        cell = self.board.cells[x][y]
        if cell.state == CellState.REVEALED or cell.is_bomb:
            return

        cell.state = CellState.REVEALED
        self._num_of_revealed += 1

        self.buttons[x][y].config(bg="white", state=tk.DISABLED,
            text=str(cell.number_of_neighboring_mines) if cell.number_of_neighboring_mines else "")
        if cell.number_of_neighboring_mines == 0:
            for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                if 0 <= x + dx < self.board.size and 0 <= y + dy < self.board.size:
                    self._reveal_recursive(x + dx, y + dy)