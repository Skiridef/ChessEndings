import unittest
from pathlib import Path
from Main import read_board, validate_board, iddfs

BASE_DIR = Path(__file__).parent

class TestChessEngine(unittest.TestCase):
    def _load_board(self, filename):
        filepath = BASE_DIR / filename
        return read_board(str(filepath))

    def test_invalid_board_validation(self):
        """
        Checks invalid board validation
        """
        board = self._load_board("invalid_board.txt")
        self.assertFalse(validate_board(board))

    def test_no_forced_mate(self):
        """
        Checks no forced mate
        """
        board = self._load_board("no_mate.txt")
        self.assertTrue(validate_board(board))
        result = iddfs(board, max_depth = 3, is_white_start =True)
        self.assertIsNone(result)

    def test_mate_in_1(self):
        """
        Mate in 1 (Rook a1 -> a8)
        """
        board = self._load_board("mate_in_1.txt")
        self.assertTrue(validate_board(board))
        result = iddfs(board, max_depth = 3, is_white_start =True)
        self.assertIsNone(result)

        depth, move = result
        self.assertEqual(depth, 1)

    def test_mate_in_2(self):
        """
        Ladder mate in 2
        """
        board = self._load_board("mate_in_2.txt")
        self.assertTrue(validate_board(board))
        result = iddfs(board, max_depth = 4, is_white_start =True)
        self.assertIsNone(result)
        depth, move = result
        self.assertEqual(depth, 2)

    def test_mate_in_3(self):
        """
        Ladder mate in 3
        """
        board = self._load_board("mate_in_3.txt")
        self.assertTrue(validate_board(board))
        result = iddfs(board, max_depth = 4, is_white_start =True)
        self.assertIsNone(result)
        depth, move = result
        self.assertEqual(depth, 3)

if __name__ == '__main__':
    unittest.main()
