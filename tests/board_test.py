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
		self.board = board.Board()

	def test_constructor(self):
		self.assertTrue('SVM' == self.board.model.__class__.__name__)

	def test_get_correct_number_of_cards(self):
		for i in range(1,5):
			img = os.path.abspath('tests/data/board_clean_%d.JPG' % i)
			self.board.image = img
			self.board.minsize = 5000
			fs = self.board.findCards()
			num_blobs = 0

			if fs:
				num_blobs = len(fs)

			if BoardTest.showImages:
				self.board.showImage()
				time.sleep(2)

			self.assertEqual(num_blobs, 5, '%d blob(s) found in %s' %  (num_blobs, img))

	def test_get_correct_number_of_lines(self):
		for i in range(1,5):
			img = os.path.abspath('tests/data/board_clean_%d.JPG' % i)
			self.board.image = img
			self.board.minsize = 5000
			fs = self.board.findLines()
			num_lines = 0

			if fs:
				num_lines = len(fs)
				for b in fs:
					b.draw(width=3, color=Color.GREEN)

			if BoardTest.showImages:
				self.board.showImage()
				time.sleep(2)
			self.assertEqual(self.board.swimlanes, 3, '%d line(s) found in %s' %  (num_lines, img))

	def test_read_numbers(self):
		all_keys = []
		for i in range(1,5):
			img = os.path.abspath('tests/data/board_numbers_%d.JPG' % i)
			self.board.image = img
			self.board.minsize = 5000
			self.board.findCards()
			all_keys.extend(self.board.keys)

			if BoardTest.showImages:
				self.board.showImage()
				time.sleep(1)
			#for key in self.board.keys:
				#self.assertEqual(4, len(key), "Key '%s' has wrong size: %d" % (key, len(key)))
		self.assertTrue("2345" in all_keys, all_keys)
		self.assertTrue("6890" in all_keys, all_keys)
		self.assertTrue("2176" in all_keys, all_keys)
		self.assertTrue("8431" in all_keys, all_keys)
		self.assertTrue("5678" in all_keys, all_keys)
		self.assertTrue("1234" in all_keys, all_keys)
