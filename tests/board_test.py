import unittest
import os, glob
from src import board
from SimpleCV import Display, Color
import time


class BoardTest(unittest.TestCase):
	showImages = False
	def setUp(self):
		self.board = board.Board()

	def test_constructor(self):
		self.assertTrue('SVM' == self.board.model.__class__.__name__)

	def test_get_correct_number_of_cards(self):
		for file in glob.glob('tests/data/board_ni_*.JPG'):
			self.board.image = os.path.abspath(file)
			fs = self.board.findCards()

			if BoardTest.showImages:
				self.board.showImage()
				time.sleep(2)

			self.assertEqual(self.board.num_cards, 15, '%d blob(s) found in %s' %  (self.board.num_cards, file))

	def test_get_correct_number_of_lines(self):
		for file in glob.glob('tests/data/board_ni_*.JPG'):
			self.board.image = os.path.abspath(file)
			fs = self.board.findLines()
			num_lines = 0

			if fs:
				num_lines = len(fs)
				for b in fs:
					b.draw(width=3, color=Color.GREEN)

			if BoardTest.showImages:
				self.board.showImage()
				time.sleep(2)
			self.assertEqual(self.board.swimlanes, 4, '%d line(s) found in %s' %  (num_lines, file))

	def test_get_card_status(self):
		for file in glob.glob('tests/data/board_ni_*.JPG'):
			self.board.image = os.path.abspath(file)
			fs = self.board.findCards()
			self.assertEqual(1, self.board.card("2358").status)
			self.assertEqual(2, self.board.card("2600").status)

