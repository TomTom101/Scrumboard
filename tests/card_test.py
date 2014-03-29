import unittest
import os
from scrumboard import board
import time
import glob


class CardTest(unittest.TestCase):
    showImages = False
    def setUp(self):
        self.img = os.path.abspath('tests/data/board_clean_1.JPG')

    def test_constructor(self):
        test_board = board.Board()
        self.assertTrue('SVM' == test_board.model.__class__.__name__)


    def test_read_numbers(self):
        for _file in glob.glob('tests/data/board_ni_lines_*.JPG'):
            img = os.path.abspath(_file)
            test_board = board.Board(save_training_file=False)
            test_board.image = img
            test_board.findCards()

            if CardTest.showImages:
                test_board.draw()
                test_board.show()

            self.assertTrue("2358" in test_board.keys, test_board.keys)
            self.assertTrue("2551" in test_board.keys, test_board.keys)
            self.assertTrue("2590" in test_board.keys, test_board.keys)
            self.assertTrue("2361" in test_board.keys, test_board.keys)
            self.assertTrue("2484" in test_board.keys, test_board.keys)
            self.assertTrue("2486" in test_board.keys, test_board.keys)
            self.assertTrue("2481" in test_board.keys, test_board.keys)
            self.assertTrue("2600" in test_board.keys, test_board.keys)
            self.assertTrue("2483" in test_board.keys, test_board.keys)

            self.assertTrue("2611" in test_board.keys, test_board.keys)
            self.assertTrue("2578" in test_board.keys, test_board.keys)
            self.assertTrue("2577" in test_board.keys, test_board.keys)
            self.assertTrue("2455" in test_board.keys, test_board.keys)
            self.assertTrue("2546" in test_board.keys, test_board.keys)
            self.assertTrue("2501" in test_board.keys, test_board.keys)


