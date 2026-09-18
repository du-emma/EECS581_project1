"""
Module: NumberCalculator
Description:
    Calculates the number of adjacent mines for every non-mine cell on
    the board. The calculated values 0 to 8, is stored in each Cell object
    for quick access during gameplay
Inputs:
    A BoardManager object containing the 10x10 Minesweeper board after
    mines have been generated
Outputs:
    None
External Sources:
    ChatGPT was used to refine syntax and and logic when testing
Author:
    Serom Kim
Created:
    9/16/26
"""

def calculateNumbers(board):
    """
    Calculate and store the number of adjacent mines for each non-mine cell.

    Each cell can have up to eight neighboring cells. For every non-mine
    cell, this function examines those neighboring positions and counts
    how many contain mines.

    Args:
        board: BoardManager object containing the 10x10 grid of Cell objects.

    Returns:
        None. Adjacent mine counts are written directly to the Cell objects.
    """

    # Visit every position on the board.
    for row in range(board.ROWS):
        for col in range(board.COLS):
            current_cell = board.getCell(row, col)
            # Mines do not need an adjacent mine count.
            if current_cell.hasMine():
                continue
            mine_count = 0
            # Check the eight possible neighboring positions.
            for row_offset in range(-1, 2):
                for col_offset in range(-1, 2):
                    # An offset of (0, 0) is the current cell itself.
                    if row_offset == 0 and col_offset == 0:
                        continue
                    neighbor_row = row + row_offset
                    neighbor_col = col + col_offset
                    # Only check neighbors that are inside the board.
                    if (
                        0 <= neighbor_row < board.ROWS
                        and 0 <= neighbor_col < board.COLS
                    ):
                        neighbor = board.getCell(
                            neighbor_row,
                            neighbor_col
                        )
                        # Increase the count when the neighboring cell
                        # contains a mine.
                        if neighbor.hasMine():
                            mine_count += 1
            # Store the completed count in the current Cell object.
            current_cell.setAdjacentMines(mine_count)