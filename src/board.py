
from SimpleCV import Image
from src import card

class Board(object):
	def __init__(self, board_img_file):
		img = Image(board_img_file).resize(800,600)
		self.img = self.__preprocess(img)

		self._num_cards = 5
		self._minsize = 5000;
		self.findColors = [(160, 125, 40)]
		self.cards = []
		self.lane_separators = []

	def __preprocess(self, img):
		return img.resize(800,600)

	def findCards(self):
		"""analyzes an image and returns all blobs

		:returns: A SimpleCV FeatureSet
		:rtype: SimpleCV.Features.Features.FeatureSet
		"""
		fs = self.img.hueDistance(self.findColors[0]).binarize(thresh=50).findBlobs(minsize=self.minsize)
		for b in fs:
			self.cards.append(card.Card(b))
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
