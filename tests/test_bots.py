import unittest
from bots.easy_bot import EasyBot
from bots.medium_bot import MediumBot
from bots.hard_bot import HardBot
from game.board import Board

class TestBots(unittest.TestCase):

    def setUp(self):
        self.board = Board()
        self.easy_bot = EasyBot()
        self.medium_bot = MediumBot()
        self.hard_bot = HardBot()

    def test_easy_bot_move(self):
        initial_position = self.board.get_position()
        move = self.easy_bot.make_move(self.board)
        self.assertNotEqual(initial_position, self.board.get_position(), "EasyBot should make a move.")

    def test_medium_bot_move(self):
        initial_position = self.board.get_position()
        move = self.medium_bot.make_move(self.board)
        self.assertNotEqual(initial_position, self.board.get_position(), "MediumBot should make a move.")

    def test_hard_bot_move(self):
        initial_position = self.board.get_position()
        move = self.hard_bot.make_move(self.board)
        self.assertNotEqual(initial_position, self.board.get_position(), "HardBot should make a move.")

    def test_bot_evaluation(self):
        evaluation_easy = self.easy_bot.evaluate(self.board)
        evaluation_medium = self.medium_bot.evaluate(self.board)
        evaluation_hard = self.hard_bot.evaluate(self.board)

        self.assertIsInstance(evaluation_easy, int, "EasyBot evaluation should return an integer.")
        self.assertIsInstance(evaluation_medium, int, "MediumBot evaluation should return an integer.")
        self.assertIsInstance(evaluation_hard, int, "HardBot evaluation should return an integer.")

if __name__ == '__main__':
    unittest.main()