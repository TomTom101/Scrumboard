
from SimpleCV import Color, Image
import card as c
from digits import digits as ocr
import numpy as np
import cv2
import time

class Board(object):
	SVMData = 'digits_svm.dat'
	def __init__(self, board_img_file):

		self._num_cards = 5
		self._minsize = 5000;
		self.findColors = [(160, 125, 40), (125,140,60)]
		self.cards = []
		self.lane_separators = []
		self.model = ocr.SVM(C=2.67, gamma=5.383)
		self.model.load(Board.SVMData)
		img = Image(board_img_file)
		self.img = self.__preprocess(img)

	def __preprocess(self, img):
		return img.resize(800,600)


	def findCards(self):
		"""analyzes an image and returns all blobs

		:returns: A SimpleCV FeatureSet
		:rtype: SimpleCV.Features.Features.FeatureSet
		"""
		img = self.img.hueDistance(self.findColors[0]).morphClose().binarize(thresh=25) 
		fs = img.findBlobs(minsize=self.minsize)
		for b in fs:
			card = c.Card(self.img.crop(b))
			if card.cells:
				card.cells = map(ocr.deskew, card.cells)
				samples = ocr.preprocess_hog(card.cells)
				key = self.model.predict(samples)
				card.key = ''.join(str(int(y)) for y in key)
			self.cards.append(card)
			b.image = self.img
			b.drawMinRect(color=Color.RED, width=3)

		return self.cards


	def findLines(self):
		"""analyzes an image and returns all lines

		:param board_img_file: filename of an image of the entire board
		:returns: A SimpleCV FeatureSet
		:rtype: SimpleCV.Features.Features.FeatureSet
		"""
		self.img = self.img.binarize(thresh=50).morphClose()
#		lines = self.img.findLines(minlinelength=self.img.height*.5, maxlinegap=self.img.height*.5, maxpixelgap=1, threshold=150)

		lines = self.img.findBlobs(minsize=self.img.height)
		self.lane_separators = lines.x()
		return lines

	def save(self):
		self.img.save('save.jpg')
	
	@property
	def keys(self):
	    return [card.key for card in self.cards]
	
	@property
	def swimlanes(self):
		return len(self.lane_separators)+1

	@property
	def minsize(self):
	    return self._minsize
	@minsize.setter
	def minsize(self, value):
	    self._minsize = value
	
	@property
	def num_cards(self):
		return self._num_cards

	def setDisplay(self, display):
		self.display = display

	def showImage(self):
		self.img.show()
