class Cell:
    """Represents one cell on the Minesweeper board."""

    COVERED = 0
    FLAGGED = 1
    UNCOVERED = 2

    def __init__(self):
        """
        Initialize a new cell.

        Every cell begins covered, does not contain a mine, and has
        an adjacent mine count of zero.
        """
        self.state = self.COVERED
        self.is_mine = False
        self.adjacent_mines = 0

    def reset(self):
        """
        Reset the cell to its initial state.
        """
        self.state = self.COVERED
        self.is_mine = False
        self.adjacent_mines = 0

    def getState(self):
        """
        Return the current state of the cell.

        Returns:
            int: COVERED, FLAGGED, or UNCOVERED.
        """
        return self.state

    def setState(self, state):
        """
        Set the current state of the cell.

        Args:
            state (int): The new state of the cell.
        """
        self.state = state

    def hasMine(self):
        """
        Return whether the cell contains a mine.

        Returns:
            bool: True if the cell contains a mine, otherwise False.
        """
        return self.is_mine

    def setMine(self, value=True):
        """
        Set whether the cell contains a mine.

        Args:
            value (bool): True if the cell should contain a mine,
                          otherwise False.
        """
        self.is_mine = value

    def getAdjacentMines(self):
        """
        Return the number of mines surrounding the cell.

        Returns:
            int: Number of adjacent mines from 0 to 8.
        """
        return self.adjacent_mines

    def setAdjacentMines(self, count):
        """
        Set the number of mines surrounding the cell.

        Args:
            count (int): Number of adjacent mines from 0 to 8.
        """
        self.adjacent_mines = count

    def isCovered(self):
        """
        Return whether the cell is covered.

        Returns:
            bool: True if the cell is covered, otherwise False.
        """
        return self.state == self.COVERED

    def isFlagged(self):
        """
        Return whether the cell is flagged.

        Returns:
            bool: True if the cell is flagged, otherwise False.
        """
        return self.state == self.FLAGGED

    def isUncovered(self):
        """
        Return whether the cell is uncovered.

        Returns:
            bool: True if the cell is uncovered, otherwise False.
        """
        return self.state == self.UNCOVERED