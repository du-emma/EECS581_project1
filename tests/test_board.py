# to run this file, run the following command in terminal:
# python -m unittest tests.test_board

import unittest

from src.board import BoardManager
from src.cell import Cell


class TestBoardManager(unittest.TestCase):

    def setUp(self):
        self.board = BoardManager()

    def test_board_has_correct_dimensions(self):
        grid = self.board.getBoard()

        self.assertEqual(len(grid), BoardManager.ROWS)
        self.assertEqual(len(grid), 10)

        for row in grid:
            self.assertEqual(len(row), BoardManager.COLS)
            self.assertEqual(len(row), 10)

    def test_new_board_cells_start_covered_and_empty(self):
        for row in range(BoardManager.ROWS):
            for col in range(BoardManager.COLS):
                cell = self.board.getCell(row, col)

                self.assertTrue(cell.isCovered())
                self.assertFalse(cell.hasMine())
                self.assertEqual(cell.getAdjacentMines(), 0)

    def test_get_cell_returns_cell_at_requested_position(self):
        cell = self.board.getCell(3, 7)

        self.assertIsInstance(cell, Cell)
        self.assertIs(cell, self.board.getBoard()[3][7])

    def test_set_cell_changes_state(self):
        self.board.setCell(2, 4, Cell.FLAGGED)

        self.assertTrue(self.board.getCell(2, 4).isFlagged())

        self.board.setCell(2, 4, Cell.UNCOVERED)

        self.assertTrue(self.board.getCell(2, 4).isUncovered())

    def test_reset_creates_clean_board(self):
        cell = self.board.getCell(0, 0)
        cell.setState(Cell.FLAGGED)
        cell.setMine(True)
        cell.setAdjacentMines(3)

        self.board.reset()

        reset_cell = self.board.getCell(0, 0)
        self.assertTrue(reset_cell.isCovered())
        self.assertFalse(reset_cell.hasMine())
        self.assertEqual(reset_cell.getAdjacentMines(), 0)

    def test_each_board_location_has_its_own_cell_object(self):
        top_left = self.board.getCell(0, 0)
        next_cell = self.board.getCell(0, 1)

        self.assertIsNot(top_left, next_cell)

        top_left.setState(Cell.FLAGGED)

        self.assertTrue(top_left.isFlagged())
        self.assertTrue(next_cell.isCovered())


if __name__ == "__main__":
    unittest.main()