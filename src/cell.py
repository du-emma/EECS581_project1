"""
Module: Cell
Description:
    Defines the Cell class used to represent an individual cell 
    on the board. Each cell stores its visible state, whether it
    contains a mine, and the number of adjacent mines
Inputs:
    Cell state, mine status, and adjacent mine count when modified
Outputs:
    Cell objects containing the data needed by the BoardManager,
    MineGenerator, NumberCalculator, and Game Logic
External Sources:
    ChatGPT was used to refine syntax and logic
Author:
    Serom Kim
Created:
    9/14/26
"""

class Cell:
    # Represents one cell on the Minesweeper board
    # Possible visible states of a cell
    COVERED = 0
    FLAGGED = 1
    UNCOVERED = 2
    def __init__(self):
        #Initialize a new cell

        # All cells begin covered, contain no mine, and have an adjacent
        # mine count of zero.
        self.state = self.COVERED
        self.is_mine = False
        self.adjacent_mines = 0

    def reset(self):
        #Reset the cell to its original state
        self.state = self.COVERED
        self.is_mine = False
        self.adjacent_mines = 0

    def getState(self):
        #Return the current visible state of the cell
        return self.state
    
    def setState(self, state):
        #Set the visible state of the cell
        self.state = state

    def hasMine(self):
        #Return whether the cell contains a mine
        return self.is_mine
    
    def setMine(self, value=True):
       #Set whether the cell contains a mine
        self.is_mine = value

    def getAdjacentMines(self):
        #Return the number of mines surrounding the cell
        return self.adjacent_mines
    
    def setAdjacentMines(self, count):
        #Set the number of mines surrounding the cell
        self.adjacent_mines = count

    def isCovered(self):
        #Return whether the cell is covered
        return self.state == self.COVERED
    
    def isFlagged(self):
        # Return whether the cell is flagged
        return self.state == self.FLAGGED
    
    def isUncovered(self):
        #Return whether the cell is uncovered.
        return self.state == self.UNCOVERED