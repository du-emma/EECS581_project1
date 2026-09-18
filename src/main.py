"""Entry point for the Minesweeper project.

This file creates the game model and starts the app. The UI is intentionally
not imported here because the current UI module is still under development and
currently runs code on import, which makes it a poor entry point.
"""

try:
    from .board import BoardManager
    from .game import Game
except ImportError:  # pragma: no cover
    from board import BoardManager
    from game import Game


BOARD_SIZE = 10
MINE_COUNT = 10


def main():
    """Initialize the game and return the game object."""
    board = BoardManager()
    game = Game(board, MINE_COUNT)

    print("Minesweeper initialized.")
    print(f"Board size: {board.ROWS}x{board.COLS}")
    print(f"Mine count: {game.mine_count}")
    print("The UI layer can be wired in here once it is finished.")

    return game


if __name__ == "__main__":
    main()
