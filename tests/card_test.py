import unittest
import os
from src import board
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
        all_keys = []
        for i in range(1,5):
            img = os.path.abspath('tests/data/board_numbers_%d.JPG' % i)
            test_board = board.Board()
            test_board.image = img
            test_board.findCards()
            all_keys.extend(test_board.keys)

            if CardTest.showImages:
                test_board.show()
                time.sleep(1)
            #for key in test_board.keys:
                #self.assertEqual(4, len(key), "Key '%s' has wrong size: %d" % (key, len(key)))
        self.assertTrue("2345" in all_keys, all_keys)
        self.assertTrue("6890" in all_keys, all_keys)
        self.assertTrue("2176" in all_keys, all_keys)
        self.assertTrue("8431" in all_keys, all_keys)
        self.assertTrue("5678" in all_keys, all_keys)
        self.assertTrue("1234" in all_keys, all_keys)

    def test_read_first_line_only(self):
        for _file in glob.glob('tests/data/board_ni_*.JPG'):
            img = os.path.abspath(_file)
            test_board = board.Board(save_training_file=True)
            test_board.image = img
            test_board.findCards()

            if CardTest.showImages:
                test_board.show()
                time.sleep(1)
                
            self.assertTrue("2358" in test_board.keys, test_board.keys)
            self.assertTrue("2501" in test_board.keys, test_board.keys)
            self.assertTrue("2551" in test_board.keys, test_board.keys)
            self.assertTrue("2590" in test_board.keys, test_board.keys)
            self.assertTrue("2361" in test_board.keys, test_board.keys)
            self.assertTrue("2484" in test_board.keys, test_board.keys)
            self.assertTrue("2546" in test_board.keys, test_board.keys)
            self.assertTrue("2455" in test_board.keys, test_board.keys)
            self.assertTrue("2486" in test_board.keys, test_board.keys)
            self.assertTrue("2481" in test_board.keys, test_board.keys)
            self.assertTrue("2600" in test_board.keys, test_board.keys)
            self.assertTrue("2483" in test_board.keys, test_board.keys)

            #self.assertTrue("2611" in test_board.keys, test_board.keys)
            #self.assertTrue("2578" in test_board.keys, test_board.keys)
            #self.assertTrue("2577" in test_board.keys, test_board.keys)

    def tst_read_wide_numbers(self):
        all_keys = []
        for i in range(1,2):
            img = os.path.abspath('tests/data/board_numbers_wide_%d.JPG' % i)
            test_board = board.Board()
            test_board.image = img
            test_board.minsize = 5000
            test_board.findCards()
            all_keys.extend(test_board.keys)

            if CardTest.showImages:
                test_board.show()
                time.sleep(1)

        self.assertTrue("2345" in all_keys, all_keys)
        self.assertTrue("6890" in all_keys, all_keys)

