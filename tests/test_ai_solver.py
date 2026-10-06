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