import time
import numpy as np

class Card(object):

	def __init__(self, img_card):
		self.img_card = img_card
		self.status = None
		self._key = None
		self.minsize = self.img_card.area() * .006
		self.cells = self.__extractCells()
		np.set_printoptions(threshold='nan')


	def __extractCells(self):
		""" Need be filled
		"""
		self.img_card = self.img_card.binarize(thresh=90).morphClose().morphClose()

		fs = self.img_card.findBlobs(minsize=self.minsize)
		if fs:
			cells = []
			for b in fs.sortX():
				r = b.drawMinRect(width=4, color=(255,0,0))
				bb = b.boundingBox()
				canvas = tuple([max(bb[-2:]) for x in range(2)])
				digit = self.img_card.crop(b).embiggen(canvas).resize(20, 20)
				digit.show()
				cells.append(digit.getGrayNumpyCv2())
			return cells

		return None

	@property
	def key(self):
	    return self._key
	@key.setter
	def key(self, value):
	    self._key = value
	


	