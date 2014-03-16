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
			fs = self.board.findCards()
			num_blobs = 0

			if fs:
				num_blobs = len(fs)

			if BoardTest.showImages:
				self.board.showImage()
				time.sleep(2)

			self.assertEqual(num_blobs, 5, '%d blob(s) found in %s' %  (num_blobs, img))

	def test_get_correct_number_of_lines(self):
		for i in range(1,3):
			img = os.path.abspath('tests/data/board_numbers_%d.JPG' % i)
			self.board.image = img
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

	def test_get_card_status(self):
		for i in range(1,3):
			img = os.path.abspath('tests/data/board_numbers_%d.JPG' % i)
			self.board.image = img
			fs = self.board.findCards()
			self.assertEqual(0, self.board.card("2345").status)
			self.assertEqual(1, self.board.card("6890").status)

