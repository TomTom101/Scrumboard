import unittest
import os
#from mock import Mock
from src import board
from SimpleCV import Display, Color
import time


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
			test_board.minsize = 5000
			test_board.findCards()
			all_keys.extend(test_board.keys)

			if CardTest.showImages:
				test_board.showImage()
				time.sleep(1)
			#for key in test_board.keys:
				#self.assertEqual(4, len(key), "Key '%s' has wrong size: %d" % (key, len(key)))
		self.assertTrue("2345" in all_keys, all_keys)
		self.assertTrue("6890" in all_keys, all_keys)
		self.assertTrue("2176" in all_keys, all_keys)
		self.assertTrue("8431" in all_keys, all_keys)
		self.assertTrue("5678" in all_keys, all_keys)
		self.assertTrue("1234" in all_keys, all_keys)

