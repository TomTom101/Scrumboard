import time
import numpy as np

class Card(object):

	def __init__(self, img):
		self.img = img
		self.status = None
		self._key = None
		self._x = 0
		self.minsize = 10
		self.cells = self.__extractCells()

	def __extractCells(self):
		""" Need be filled
		"""
		self.img = self.img.resize(w=150).binarize(thresh=95).morphClose()
		fs = self.img.findBlobs(minsize=self.minsize)

		if fs:
			cells = []
			for char in fs.sortX():
				""" discard if w/h;h/w ratio > 2"""
				# tbd
				char.image = self.img
				char.drawMinRect(width=4, color=(0,255,0))
				charBox = char.boundingBox()
				"""creates a tuple with 2 identical values of the longest side + 2px. e.g. for w*h = 65*70 == (72,72) """
				canvas = tuple([(max(charBox[-2:])+2) for x in range(2)])
				digit = self.img.crop(char).embiggen(canvas).resize(20, 20)
				cells.append(digit.getGrayNumpyCv2())
			return cells

		return None

	@property
	def x(self):
	    return self._x
	@x.setter
	def x(self, value):
	    self._x = value
	
	@property
	def key(self):
	    return self._key
	@key.setter
	def key(self, value):
	    self._key = value
	