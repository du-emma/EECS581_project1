from src.board import BoardManager
from src.game import Game
from src.ai_solver import AISolver


def test_ai_solver_initialization():
    board = BoardManager()
    game = Game(board, 10)

    ai = AISolver(game)

    assert ai.game is game
    assert ai.board is board


def test_medium_ai_flags_mine():
    board = BoardManager()
    game = Game(board, 1)
    ai = AISolver(game)

    # Set up a simple known board state.
    game._mines_placed = True

    # Make A1 a revealed "1".
    center = board.getCell(0, 0)
    center.setState(center.UNCOVERED)
    center.setAdjacentMines(1)


    # B1 is the only hidden neighbor, so the AI should flag it.
    board.getCell(0, 1).setState(board.getCell(0, 1).COVERED)

    # Reveal A2 and B2 so they are not possible hidden mines.
    board.getCell(1, 0).setState(board.getCell(1, 0).UNCOVERED)
    board.getCell(1, 1).setState(board.getCell(1, 1).UNCOVERED)

    ai.medium_move()

    assert board.getCell(0, 1).isFlagged()


def test_medium_ai_uncovers_safe_cell():
    board = BoardManager()
    game = Game(board, 1)
    ai = AISolver(game)

    # Mines are already placed for this test.
    game._mines_placed = True

    # A1 is an uncovered cell showing the number 1.
    center = board.getCell(0, 0)
    center.setState(center.UNCOVERED)
    center.setAdjacentMines(1)

    # B1 is already flagged as the one mine.
    mine_cell = board.getCell(0, 1)
    mine_cell.setState(mine_cell.FLAGGED)

    # A2 is covered and should be safe.
    safe_cell = board.getCell(1, 0)
    safe_cell.setState(safe_cell.COVERED)

    # B2 is uncovered so A2 is the only remaining hidden neighbor.
    board.getCell(1, 1).setState(
        board.getCell(1, 1).UNCOVERED
    )

    ai.medium_move()

    assert safe_cell.isUncovered()


def test_medium_ai_random_fallback():
    board = BoardManager()
    game = Game(board, 10)
    ai = AISolver(game)

    # Mines are already considered placed so uncovering a cell
    # does not generate a new random board.
    game._mines_placed = True

    # There are no uncovered numbered cells, so neither
    # Rule 1 nor Rule 2 can be used.
    covered_before = 0

    for row in range(board.ROWS):
        for col in range(board.COLS):
            if board.getCell(row, col).isCovered():
                covered_before += 1

    ai.medium_move()

    covered_after = 0

    for row in range(board.ROWS):
        for col in range(board.COLS):
            if board.getCell(row, col).isCovered():
                covered_after += 1

    # The random fallback should uncover at least one cell.
    assert covered_after < covered_before


def test_hard_ai_horizontal_121():
    board = BoardManager()
    game = Game(board, 2)
    ai = AISolver(game)

    game._mines_placed = True

    # Create a revealed horizontal 1-2-1 pattern along the top row.
    for col, number in enumerate((1, 2, 1)):
        cell = board.getCell(0, col)
        cell.setState(cell.UNCOVERED)
        cell.setAdjacentMines(number)

    # Reveal the extra neighbors beside the pattern so the only hidden
    # neighbors are the three cells directly below 1-2-1.
    board.getCell(0, 3).setState(board.getCell(0, 3).UNCOVERED)
    board.getCell(1, 3).setState(board.getCell(1, 3).UNCOVERED)

    # The two outer hidden cells are mines and the middle one is safe.
    board.getCell(1, 0).setMine(True)
    board.getCell(1, 2).setMine(True)
    board.getCell(1, 1).setAdjacentMines(2)

    ai.hard_move()

    assert board.getCell(1, 0).isFlagged()
    assert board.getCell(1, 1).isUncovered()
    assert board.getCell(1, 2).isFlagged()


def test_hard_ai_vertical_121():
    board = BoardManager()
    game = Game(board, 2)
    ai = AISolver(game)

    game._mines_placed = True

    # Create a revealed vertical 1-2-1 pattern along the left edge.
    for row, number in enumerate((1, 2, 1)):
        cell = board.getCell(row, 0)
        cell.setState(cell.UNCOVERED)
        cell.setAdjacentMines(number)

    # Reveal the extra cells below the pattern so the only hidden
    # neighbors are the three cells directly to the right of 1-2-1.
    board.getCell(3, 0).setState(board.getCell(3, 0).UNCOVERED)
    board.getCell(3, 1).setState(board.getCell(3, 1).UNCOVERED)

    board.getCell(0, 1).setMine(True)
    board.getCell(2, 1).setMine(True)
    board.getCell(1, 1).setAdjacentMines(2)

    ai.hard_move()

    assert board.getCell(0, 1).isFlagged()
    assert board.getCell(1, 1).isUncovered()
    assert board.getCell(2, 1).isFlagged()


def test_hard_ai_uses_medium_rules_when_no_121():
    board = BoardManager()
    game = Game(board, 1)
    ai = AISolver(game)

    game._mines_placed = True

    # A1 is a revealed 1 with only B1 still hidden, so the Medium
    # flagging rule should be used when no 1-2-1 pattern exists.
    center = board.getCell(0, 0)
    center.setState(center.UNCOVERED)
    center.setAdjacentMines(1)

    board.getCell(1, 0).setState(board.getCell(1, 0).UNCOVERED)
    board.getCell(1, 1).setState(board.getCell(1, 1).UNCOVERED)

    ai.hard_move()

    assert board.getCell(0, 1).isFlagged()

