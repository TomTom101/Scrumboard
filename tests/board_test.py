import unittest
import os
#from mock import Mock
from src import board
from SimpleCV import Display, Color
import time


class BoardTest(unittest.TestCase):
	showImages = False
	def setUp(self):
		self.num_cards = 5
		self.img = os.path.abspath('tests/data/board_clean_1.JPG')

	def test_constructor(self):
		test_board = board.Board()
		self.assertTrue('SVM' == test_board.model.__class__.__name__)

	def test_get_correct_number_of_cards(self):
		for i in range(1,5):
			img = os.path.abspath('tests/data/board_clean_%d.JPG' % i)
			test_board = board.Board()
			test_board.image = img
			test_board.minsize = 5000
			fs = test_board.findCards()
			num_blobs = 0

			if fs:
				num_blobs = len(fs)

			if BoardTest.showImages:
				test_board.showImage()
				time.sleep(2)

			self.assertEqual(num_blobs, 5, '%d blob(s) found in %s' %  (num_blobs, img))

	def test_get_correct_number_of_lines(self):
		for i in range(1,5):
			img = os.path.abspath('tests/data/board_clean_%d.JPG' % i)
			test_board = board.Board()
			test_board.image = img
			test_board.minsize = 5000
			fs = test_board.findLines()
			num_lines = 0

			if fs:
				num_lines = len(fs)
				for b in fs:
					b.draw(width=3, color=Color.GREEN)

			if BoardTest.showImages:
				test_board.showImage()
				time.sleep(2)
			self.assertEqual(test_board.swimlanes, 3, '%d line(s) found in %s' %  (num_lines, img))

	def test_read_numbers(self):
		all_keys = []
		for i in range(1,5):
			img = os.path.abspath('tests/data/board_numbers_%d.JPG' % i)
			test_board = board.Board()
			test_board.image = img
			test_board.minsize = 5000
			test_board.findCards()
			all_keys.extend(test_board.keys)

			if BoardTest.showImages:
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

	def test_wait(self):
		time.sleep(0.1)