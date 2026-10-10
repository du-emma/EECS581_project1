"""
File: ai_solver.py
Module: AI Solver

Description:
    Implements the AI solver for the Minesweeper game.
    The medium difficulty uses basic Minesweeper deduction rules
    to flag likely mines and uncover safe cells. The hard difficulty
    adds the 1-2-1 pattern rule. If no logical move can be found,
    the AI chooses a random covered cell.

Inputs:
    Current Game and BoardManager state.

Outputs:
    AI actions that flag or uncover cells.

External Sources:
    ChatGPT was used to assist with the structure and logic
    of the Medium and Hard AI implementations.

Authors:
    Atique Ahanaf Danial - Medium AI
    Ever Armenta - Hard AI

Created:
    2026-10-05
Modified:
    2026-10-08

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

    def _covered_neighbor_set(self, row, col):
        """Return the covered neighboring coordinates around a cell."""
        covered = set()

        for neighbor_row, neighbor_col in self._neighbors(row, col):
            neighbor = self.board.getCell(neighbor_row, neighbor_col)
            if neighbor.isCovered():
                covered.add((neighbor_row, neighbor_col))

        return covered

    def _has_flagged_neighbor(self, row, col):
        """Return True if a cell has at least one flagged neighbor."""
        for neighbor_row, neighbor_col in self._neighbors(row, col):
            if self.board.getCell(neighbor_row, neighbor_col).isFlagged():
                return True

        return False

    def _apply_121(self):
        """Find and apply one horizontal or vertical 1-2-1 pattern."""

        # Check horizontal 1-2-1 patterns.
        for row in range(self.board.ROWS):
            for col in range(self.board.COLS - 2):
                first = self.board.getCell(row, col)
                middle = self.board.getCell(row, col + 1)
                last = self.board.getCell(row, col + 2)

                if not (
                    first.isUncovered()
                    and middle.isUncovered()
                    and last.isUncovered()
                    and first.getAdjacentMines() == 1
                    and middle.getAdjacentMines() == 2
                    and last.getAdjacentMines() == 1
                ):
                    continue

                # Existing flags change what the visible 1-2-1 means, so let
                # the Medium rules handle those situations instead.
                if (
                    self._has_flagged_neighbor(row, col)
                    or self._has_flagged_neighbor(row, col + 1)
                    or self._has_flagged_neighbor(row, col + 2)
                ):
                    continue

                # The three hidden cells can be directly above or below the
                # revealed 1-2-1 cells.
                for hidden_row in (row - 1, row + 1):
                    if not (0 <= hidden_row < self.board.ROWS):
                        continue

                    left = (hidden_row, col)
                    center = (hidden_row, col + 1)
                    right = (hidden_row, col + 2)

                    # Make sure these are the only covered neighbors involved
                    # in the pattern before applying the deduction.
                    if self._covered_neighbor_set(row, col) != {left, center}:
                        continue
                    if self._covered_neighbor_set(row, col + 1) != {
                        left, center, right
                    }:
                        continue
                    if self._covered_neighbor_set(row, col + 2) != {center, right}:
                        continue

                    self.game.toggleFlag(*left)
                    self.game.toggleFlag(*right)
                    self.game.uncover(*center)
                    return True

        # Check vertical 1-2-1 patterns.
        for row in range(self.board.ROWS - 2):
            for col in range(self.board.COLS):
                first = self.board.getCell(row, col)
                middle = self.board.getCell(row + 1, col)
                last = self.board.getCell(row + 2, col)

                if not (
                    first.isUncovered()
                    and middle.isUncovered()
                    and last.isUncovered()
                    and first.getAdjacentMines() == 1
                    and middle.getAdjacentMines() == 2
                    and last.getAdjacentMines() == 1
                ):
                    continue

                if (
                    self._has_flagged_neighbor(row, col)
                    or self._has_flagged_neighbor(row + 1, col)
                    or self._has_flagged_neighbor(row + 2, col)
                ):
                    continue

                # The three hidden cells can be directly left or right of the
                # revealed 1-2-1 cells.
                for hidden_col in (col - 1, col + 1):
                    if not (0 <= hidden_col < self.board.COLS):
                        continue

                    top = (row, hidden_col)
                    center = (row + 1, hidden_col)
                    bottom = (row + 2, hidden_col)

                    if self._covered_neighbor_set(row, col) != {top, center}:
                        continue
                    if self._covered_neighbor_set(row + 1, col) != {
                        top, center, bottom
                    }:
                        continue
                    if self._covered_neighbor_set(row + 2, col) != {center, bottom}:
                        continue

                    self.game.toggleFlag(*top)
                    self.game.toggleFlag(*bottom)
                    self.game.uncover(*center)
                    return True

        return False

    def hard_move(self):
        """Make one move using Medium rules plus the 1-2-1 pattern."""

        if self.game.getStatus() != GameStatus.IN_PROGRESS:
            return self.game.getStatus()

        # Hard mode first looks for its extra 1-2-1 deduction.
        if self._apply_121():
            return self.game.getStatus()

        # If no 1-2-1 pattern applies, use the existing Medium rules,
        # including their random fallback.
        return self.medium_move()

