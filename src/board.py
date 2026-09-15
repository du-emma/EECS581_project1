class BoardManager:
    ROWS = 10
    COLS = 10

    COVERED = 0
    FLAGGED = 1
    UNCOVERED = 2
    MINE = 3

    def __init__(self):
        self.reset()

    def reset(self):
        """Reset the board so every cell is covered."""
        self.grid = [
            [self.COVERED for _ in range(self.COLS)]
            for _ in range(self.ROWS)
        ]

    def getCell(self, row, col):
        """Return the state of a cell."""
        return self.grid[row][col]

    def setCell(self, row, col, state):
        """Set the state of a cell."""
        self.grid[row][col] = state

    def getBoard(self):
        """Return the entire board."""
        return self.grid
