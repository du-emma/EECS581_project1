from src.board import BoardManager
from src.number_calculator import calculateNumbers


def test_single_mine():
    board = BoardManager()

    # Place one mine in the middle of the board.
    board.getCell(5, 5).setMine()

    calculateNumbers(board)

    # All eight surrounding cells should have a value of 1.
    assert board.getCell(4, 4).getAdjacentMines() == 1
    assert board.getCell(4, 5).getAdjacentMines() == 1
    assert board.getCell(4, 6).getAdjacentMines() == 1

    assert board.getCell(5, 4).getAdjacentMines() == 1
    assert board.getCell(5, 6).getAdjacentMines() == 1

    assert board.getCell(6, 4).getAdjacentMines() == 1
    assert board.getCell(6, 5).getAdjacentMines() == 1
    assert board.getCell(6, 6).getAdjacentMines() == 1

    # A cell far away from the mine should have zero.
    assert board.getCell(0, 0).getAdjacentMines() == 0


def test_two_mines():
    board = BoardManager()

    board.getCell(4, 4).setMine()
    board.getCell(4, 6).setMine()

    calculateNumbers(board)

    # Cell between the two mines should see both.
    assert board.getCell(4, 5).getAdjacentMines() == 2

    # Cell directly below the middle should also see both.
    assert board.getCell(5, 5).getAdjacentMines() == 2


def test_corner_mine():
    board = BoardManager()

    # Put a mine in the top-left corner.
    board.getCell(0, 0).setMine()

    calculateNumbers(board)

    # Only three cells can border a corner.
    assert board.getCell(0, 1).getAdjacentMines() == 1
    assert board.getCell(1, 0).getAdjacentMines() == 1
    assert board.getCell(1, 1).getAdjacentMines() == 1

    assert board.getCell(2, 2).getAdjacentMines() == 0