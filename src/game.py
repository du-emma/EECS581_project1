"""
File: game.py
Module: Game
Description: Implements the overall gameplay rules of minesweeper, evaluates win/loss
Author: Jana & Ellie
Created: 2026-09-10
Course: EECS 581 - Project 1 (Minesweeper)
"""

from enum import Enum

from board import Cell
from mine_generator import MineGenerator
from number_calculator import calculateNumbers

BOARD_SIZE = 10


class GameStatus(str, Enum):
    IN_PROGRESS = "IN_PROGRESS"
    WON = "WON"
    LOST = "LOST"


class Game:
    def __init__(self, board, mine_count):
        '''initializes the board and number of mines to place'''
        self.board = board
        self.mine_count = mine_count
        self._mine_generator = MineGenerator()
        self._status = GameStatus.IN_PROGRESS
        self._mines_placed = False
        self._revealed_count = 0
        self._flags_placed = 0
        self._total_safe_cells = BOARD_SIZE * BOARD_SIZE - mine_count

    # Public methods

    def uncover(self, row, col):
        '''reveals the cell at (row, col)'''
        if self._status != GameStatus.IN_PROGRESS:
            return self._status

        if not self._in_bounds(row, col):
            return self._status

        cell = self.board.getCell(row, col)

        if cell.isFlagged():
            return self._status

        if cell.isUncovered():
            return self._status

        if not self._mines_placed:
            self._mine_generator.generateMines(self.board, self.mine_count, (row, col))
            calculateNumbers(self.board) # could be NumberCalculator().calculateNumbers(self.board)
            self._mines_placed = True

        if cell.hasMine():
            self._lose()
            return self._status

        self._flood_fill_reveal(row, col)
        self._check_win()
        return self._status

    def toggleFlag(self, row, col):
        '''toggles the flagged state of the cell at (row, col)'''
        if self._status != GameStatus.IN_PROGRESS:
            return self._status

        if not self._in_bounds(row, col):
            return self._status

        cell = self.board.getCell(row, col)

        if cell.isUncovered():
            return self._status

        if cell.isFlagged():
            cell.setState(Cell.COVERED)
            self._flags_placed -= 1
        else:
            cell.setState(Cell.FLAGGED)
            self._flags_placed += 1

        return self._status

    def getStatus(self):
        '''returns the status: IN_PROGRESS, WON, LOST'''
        return self._status

    def remainingFlags(self):
        '''returns the number of remaining flags'''
        return self.mine_count - self._flags_placed

    # Internal helpers

    def _in_bounds(self, row, col):
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE

    def _neighbors(self, row, col):
        '''returns the up-to-8 in-bounds neighboring coordinates of (row, col)'''
        coords = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if self._in_bounds(nr, nc):
                    coords.append((nr, nc))
        return coords

    def _flood_fill_reveal(self, row, col):
        '''interative flood-fill starting at (row, col)'''
        stack = [(row, col)]
        visited = set()

        while stack:
            r, c = stack.pop()
            if (r, c) in visited:
                continue
            visited.add((r, c))

            cell = self.board.getCell(r, c)

            if cell.isUncovered() or cell.isFlagged():
                continue

            cell.setState(Cell.UNCOVERED)
            self._revealed_count += 1

            if cell.getAdjacentMines() == 0 and not cell.hasMine():
                for nr, nc in self._neighbors(r, c):
                    if (nr, nc) not in visited:
                        stack.append((nr, nc))

    def _lose(self):
        '''mark the game as lost and reveal every mine on the board'''
        self._status = GameStatus.LOST
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                cell = self.board.getCell(r, c)
                if cell.hasMine():
                    cell.setState(Cell.UNCOVERED)

    def _check_win(self):
        '''a win occurs the moment every non-mine cell has been uncovered'''
        if self._revealed_count >= self._total_safe_cells:
            self._status = GameStatus.WON