from src.cell import Cell


def test_cell_initial_state():
    cell = Cell()

    assert cell.getState() == Cell.COVERED
    assert cell.hasMine() is False
    assert cell.getAdjacentMines() == 0
    assert cell.isCovered() is True
    assert cell.isFlagged() is False
    assert cell.isUncovered() is False


def test_cell_state_changes():
    cell = Cell()

    cell.setState(Cell.FLAGGED)
    assert cell.isFlagged() is True

    cell.setState(Cell.UNCOVERED)
    assert cell.isUncovered() is True


def test_cell_mine():
    cell = Cell()

    cell.setMine()
    assert cell.hasMine() is True

    cell.setMine(False)
    assert cell.hasMine() is False


def test_adjacent_mines():
    cell = Cell()

    cell.setAdjacentMines(5)

    assert cell.getAdjacentMines() == 5


def test_reset():
    cell = Cell()

    cell.setMine()
    cell.setState(Cell.FLAGGED)
    cell.setAdjacentMines(4)

    cell.reset()

    assert cell.getState() == Cell.COVERED
    assert cell.hasMine() is False
    assert cell.getAdjacentMines() == 0