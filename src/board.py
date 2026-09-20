"""
File: board.py
Description:Manages the 10x10 Minesweeper board. The board is stored as a 2D array of Cell objects.
Inputs:Row and column positions when accessing or modifying cells.
Outputs: Cell objects or the entire board.
External Sources: ChatGPT was used to assist with integration of the Cell class with the BoardManager.
Author: Emma Roy
Course: EECS 581 - Project 1 (Minesweeper)
"""

from .cell import Cell


class BoardManager:
    """Manages the 10x10 Minesweeper board."""

    ROWS = 10
    COLS = 10

    # cell state constants are kept here as aliases so other modules
    # can access them through BoardManager if needed.
    COVERED = Cell.COVERED
    FLAGGED = Cell.FLAGGED
    UNCOVERED = Cell.UNCOVERED

    def __init__(self):
        """Create and initialize the board."""
        self.reset()

    def reset(self):
        """Reset the board by creating a new 10x10 grid of Cell objects."""
        self.grid = [
            [Cell() for _ in range(self.COLS)]
            for _ in range(self.ROWS)
        ]

    def getCell(self, row, col):
        """
        Return the Cell object at the specified board position.

        Args:
            row (int): Row index from 0 to 9.
            col (int): Column index from 0 to 9.

        Returns:
            Cell: Cell object at the specified position.
        """
        return self.grid[row][col]

    def setCell(self, row, col, state):
        """
        Set the visible state of a cell.

        Args:
            row (int): Row index from 0 to 9.
            col (int): Column index from 0 to 9.
            state (int): COVERED, FLAGGED, or UNCOVERED.
        """
        self.grid[row][col].setState(state)

    def getBoard(self):
        """Return the entire 10x10 grid of Cell objects."""
        return self.grid