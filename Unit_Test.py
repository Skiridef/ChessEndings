import unittest
from pathlib import Path
from Main import read_board, validate_board, iddfs, format_move, get_result_message

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
        self.assertIsNotNone(result)

        depth, move = result
        self.assertEqual(depth, 1)

    def test_mate_in_2(self):
        """
        Ladder mate in 2
        """
        board = self._load_board("mate_in_2.txt")
        self.assertTrue(validate_board(board))
        result = iddfs(board, max_depth = 4, is_white_start =True)
        self.assertIsNotNone(result)
        depth, move = result
        self.assertEqual(depth, 3)

    def test_mate_in_3(self):
        """
        Ladder mate in 3
        """
        board = self._load_board("mate_in_3.txt")
        self.assertTrue(validate_board(board))
        result = iddfs(board, max_depth = 6, is_white_start =True)
        self.assertIsNotNone(result)
        depth, move = result
        self.assertEqual(depth, 5)

    def test_format_move(self):
        """Checks that matrix coordinates are correctly translated to chess notation
        """
        self.assertEqual(format_move(((7, 0), (0, 0))), "from a1 to a8")
        self.assertEqual(format_move(((4,6), (4,1))), "from g4 to b4")

    def test_output_messages(self):
        """
        Checks the exact string outputs for winning and drawing scenarios
        """
        board_win = self._load_board("mate_in_1.txt")
        result_win = iddfs(board_win, max_depth = 3, is_white_start =True)
        win_msg = get_result_message(board_win, result_win, max_depth = 3)
        self.assertEqual(win_msg, "Win found in 1 moves (depth: 1). Play: R from a1 to a8")

        board_draw = self._load_board("no_mate.txt")
        result_draw = iddfs(board_draw, max_depth = 3, is_white_start =True)
        draw_msg = get_result_message(board_draw, result_draw, max_depth = 3)
        self.assertEqual(draw_msg, "No forced win found within 3 plies")

if __name__ == '__main__':
    unittest.main()
