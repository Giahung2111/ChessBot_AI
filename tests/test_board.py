import unittest
from game.board import Board

class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_initial_board_setup(self):
        self.assertEqual(self.board.get_piece_at((0, 0)), 'R')  # Rook
        self.assertEqual(self.board.get_piece_at((0, 1)), 'N')  # Knight
        self.assertEqual(self.board.get_piece_at((0, 2)), 'B')  # Bishop
        self.assertEqual(self.board.get_piece_at((0, 3)), 'Q')  # Queen
        self.assertEqual(self.board.get_piece_at((0, 4)), 'K')  # King
        self.assertEqual(self.board.get_piece_at((0, 5)), 'B')  # Bishop
        self.assertEqual(self.board.get_piece_at((0, 6)), 'N')  # Knight
        self.assertEqual(self.board.get_piece_at((0, 7)), 'R')  # Rook
        self.assertEqual(self.board.get_piece_at((1, 0)), 'P')  # Pawn

    def test_valid_move(self):
        self.board.move_piece((1, 0), (2, 0))  # Move Pawn
        self.assertEqual(self.board.get_piece_at((2, 0)), 'P')
        self.assertEqual(self.board.get_piece_at((1, 0)), None)

    def test_invalid_move(self):
        with self.assertRaises(ValueError):
            self.board.move_piece((0, 0), (0, 5))  # Invalid move for Rook

    def test_checkmate(self):
        self.board.setup_checkmate_scenario()  # Hypothetical method to set up a checkmate
        self.assertTrue(self.board.is_checkmate())

if __name__ == '__main__':
    unittest.main()