import time
import numpy as np

class Card(object):

	def __init__(self, img):
		self.img = img
		self.status = None
		self._key = None
		self.minsize = 10
		self.cells = self.__extractCells()
		np.set_printoptions(threshold='nan')


	def __extractCells(self):
		""" Need be filled
		"""
		self.img = self.img.binarize(thresh=90).morphClose()
		fs = self.img.findBlobs(minsize=self.minsize)

		if fs:
			cells = []
			for b in fs.sortX():
				#r = b.drawMinRect(width=4, color=(255,0,0))
				bb = b.boundingBox()
				"""creates a tuple with 2 identical values of the longest side + 2px. e.g. for w*h = 65*70 == (72,72) """
				canvas = tuple([(max(bb[-2:])+2) for x in range(2)])
				digit = self.img.crop(b).embiggen(canvas).resize(20, 20)
				digit.show()
				time.sleep(1)
				cells.append(digit.getGrayNumpyCv2())
			return cells

		return None

	@property
	def key(self):
	    return self._key
	@key.setter
	def key(self, value):
	    self._key = value
	


	