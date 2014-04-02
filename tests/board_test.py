import unittest
import os, glob
from scrumboard import board
from SimpleCV import Display, Color
import time


class BoardTest(unittest.TestCase):
	showImages = False
	def setUp(self):
		self.board = board.Board()

	def test_constructor(self):
		self.assertTrue('SVM' == self.board.model.__class__.__name__)

	def test_get_correct_number_of_cards(self):
		for file in glob.glob('tests/data/board_ni_lines_*.JPG'):
			self.board.image = os.path.abspath(file)
			fs = self.board.findCards()
			#self.board.draw(save=True)

			if BoardTest.showImages:
				self.board.show(sec=5)

			self.assertEqual(self.board.num_cards, 15, '%d blob(s) found in %s' %  (self.board.num_cards, file))

	def test_get_correct_number_of_lines(self):
		for file in glob.glob('tests/data/board_ni_lines_*.JPG'):
			self.board.image = os.path.abspath(file)
			fs = self.board.findLines()
			#fs.draw(color=Color.RED, width=10)
			num_lines = 0

			if fs:
				num_lines = len(fs)
				#fs.draw(width=2, autocolor=True)
				for b in fs:
					b.drawMinRect(width=5, color=Color.GREEN)
					b.image = self.board._imageprocessed

			if BoardTest.showImages:
				self.board.draw()
				self.board.show(self.board._imageprocessed_lines, 6)

			self.assertEqual(self.board.swimlanes, 5, '%d line(s) found in %s' %  (num_lines, file))

	def tst_get_card_status(self):
		for file in glob.glob('tests/data/board_ni_*.JPG'):
			self.board.image = os.path.abspath(file)
			fs = self.board.findCards()
			self.assertEqual(1, self.board.card("2358").status)
			self.assertEqual(2, self.board.card("2600").status)

