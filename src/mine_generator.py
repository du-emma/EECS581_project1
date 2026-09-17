"""
File: mine_generator.py
Module: MineGenerator
Description: Randomly places the chosen number of mines (10-20) on the 10x10
    board, making sure the player's first-clicked cell never gets a mine.
Author: Arpa
Created: 2026-09-10
Course: EECS 581 - Project 1 (Minesweeper)
"""

import random


class MineGenerator:
    # board is the shared Board, mineCount is how many mines to drop (10-20), safeCell is the first click and should never blow up
    # returns the set of (row, col) mine coords
    def generateMines(self, board, mineCount, safeCell):
        # grab every cell except whatever the player just clicked
        choices = [(r, c) for r in range(10) for c in range(10) if (r, c) != tuple(safeCell)]

        # randomly pick the mine spots out of what's left
        mines = set(random.sample(choices, mineCount))

        # flip is_mine on for each one
        for (row, col) in mines:
            board.getCell(row, col).is_mine = True
        return mines
