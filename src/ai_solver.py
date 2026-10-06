"""
File: ai_solver.py
Module: AI Solver

Description:
    Implements the AI solver for the Minesweeper game.
    The medium difficulty uses basic Minesweeper deduction rules
    to flag likely mines and uncover safe cells. If no logical
    move can be found, the AI chooses a random covered cell.

Inputs:
    Current Game and BoardManager state.

Outputs:
    AI actions that flag or uncover cells.

External Sources:
    ChatGPT was used to assist with the structure and logic
    of the Medium AI implementation.

Author:
    Atique Ahanaf Danial

Created:
    2026-10-05

Course:
    EECS 581 - Project 2 (Minesweeper)
"""

import random

from .game import GameStatus


class AISolver:
    """Handles AI moves for the Minesweeper game."""

    def __init__(self, game):
        """Initialize the AI with the current game."""
        self.game = game
        self.board = game.board

    def _neighbors(self, row, col):
        """Return all valid neighboring coordinates."""
        neighbors = []

        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):

                if dr == 0 and dc == 0:
                    continue

                new_row = row + dr
                new_col = col + dc

                if (0 <= new_row < self.board.ROWS and
                        0 <= new_col < self.board.COLS):
                    neighbors.append((new_row, new_col))

        return neighbors

    def medium_move(self):
        """
        Make one move using the Medium AI rules.

        Rule 1:
        If the number of hidden neighbors equals the number of
        mines still needed around a revealed cell, flag all of
        those hidden neighbors.

        Rule 2:
        If the number of flagged neighbors equals the revealed
        cell's number, uncover the remaining hidden neighbors.

        If neither rule can be used, uncover a random hidden cell.
        """

        # Do not make another move if the game is already over.
        if self.game.getStatus() != GameStatus.IN_PROGRESS:
            return self.game.getStatus()

        # Do not make another move if the game is already over.
        if self.game.getStatus() != GameStatus.IN_PROGRESS:
            return self.game.getStatus()

        # Examine every uncovered numbered cell on the board.
        for row in range(self.board.ROWS):
            for col in range(self.board.COLS):
                cell = self.board.getCell(row, col)

                if not cell.isUncovered():
                    continue

                number = cell.getAdjacentMines()

                # A zero cell does not provide a useful deduction here.
                if number == 0:
                    continue

                hidden_neighbors = []
                flagged_neighbors = []

                for neighbor_row, neighbor_col in self._neighbors(row, col):
                    neighbor = self.board.getCell(
                        neighbor_row, neighbor_col
                    )

                    if neighbor.isFlagged():
                        flagged_neighbors.append(
                            (neighbor_row, neighbor_col)
                        )
                    elif neighbor.isCovered():
                        hidden_neighbors.append(
                            (neighbor_row, neighbor_col)
                        )

                if not hidden_neighbors:
                    continue

                # Rule 1:
                # All remaining hidden neighbors must be mines.
                remaining_mines = number - len(flagged_neighbors)

                if (remaining_mines > 0 and
                        remaining_mines == len(hidden_neighbors)):

                    for hidden_row, hidden_col in hidden_neighbors:
                        self.game.toggleFlag(hidden_row, hidden_col)

                    return self.game.getStatus()

                # Rule 2:
                # All mines around this cell are already flagged,
                # so the remaining hidden neighbors are safe.
                if len(flagged_neighbors) == number:

                    for hidden_row, hidden_col in hidden_neighbors:
                        self.game.uncover(hidden_row, hidden_col)

                        if self.game.getStatus() != GameStatus.IN_PROGRESS:
                            return self.game.getStatus()

                    return self.game.getStatus()

        # No logical move was found, so use the required random fallback.
        hidden_cells = []

        for row in range(self.board.ROWS):
            for col in range(self.board.COLS):
                cell = self.board.getCell(row, col)

                if cell.isCovered():
                    hidden_cells.append((row, col))

        if hidden_cells:
            row, col = random.choice(hidden_cells)
            self.game.uncover(row, col)

        return self.game.getStatus()