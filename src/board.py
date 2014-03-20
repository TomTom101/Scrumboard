
import os, time
import numpy as np
import cv2
from SimpleCV import Color, Image
from digits import digits as ocr
from digits import common

import card as c

class Board(object):
	SVMData = 'own_digits_svm.dat'
	def __init__(self, saveTrainingFile=False):
		self.saveTrainingFile = saveTrainingFile
		self._image = None
		self._minsize = 5000;
		self.findColors = [(160, 140, 40), (125,140,60)]
		self.lane_separators = None
		self.model = ocr.SVM()
		if not self.model.load(Board.SVMData):
			raise Exception("SVM data could not be loaded: %s" % Board.SVMData)
		
		self.train_inbox_path = os.path.join(os.path.dirname(__file__), 'train/inbox')

	def __preprocess(self, img):
		#return img.scale(.5)
		return img#.resize(1200)

	@property
	def image(self):
	    return self._image
	@image.setter
	def image(self, image):
		if not image.__class__.__name__ == 'Image':
			image = Image(image)
		self._image = self.__preprocess(image)

	def card(self, key):
	    return self._cards[key]

	
	def findCards(self):
		"""analyzes an image and returns all blobs

		:returns: A SimpleCV FeatureSet
		:rtype: SimpleCV.Features.Features.FeatureSet
		"""
		if not self._image:
			raise Exception("Must set Board.image first!")
		""" maybe better: findBlobsFromHueHistogram() """
		img = self._image.hueDistance(self.findColors[0]).morphClose().binarize(thresh=20) 
		self._cards = {}
		fs = img.findBlobs(minsize=self.minsize)

		if fs:
			fs.draw()
			for b in fs.sortX():
				card_img = self._prepareCardBlob(b)
				card = c.Card(card_img)
				card.key = self.detectKey(card.cells)

				if card.key:
					card.x = b.x
					card.status = self.assignStatus(card)
					self._cards[card.key] = card
					self.doSaveTrainingFile(card)
				b.image = self._image
				b.drawMinRect(color=Color.BLUE, width=3)

		return self._cards

	def _prepareCardBlob(self, blob):
		if abs(blob.angle()) > 45:
			return self._image
		img = self._image.crop(blob, centered=False).rotate(blob.angle(), point=[0,0], fixed=True)
		crop = self._getPostRotationCropRegion(blob)
		if crop is not None:
			img = img.crop(crop)
		return img

	def _getPostRotationCropRegion(self, blob):

		x, y = (0, 0)
		# clock-wise, crop y
		w = blob.minRectWidth()
		h = blob.minRectHeight()
		rect = blob.minRect()
		if blob.angle() > .0:
			# counter clock-wise, crop x
			x += rect[1][0]-rect[0][0]
			w = blob.minRectHeight()
			h = blob.minRectWidth()
		elif blob.angle() < .0:
			y += rect[0][1]-rect[1][1]

	 	#print "angle: %.2f, x, y: %d, %d, w: %d, h: %d" % (blob.angle(), x, y, w, h)

		return (x, y, w-15, h-15)

	def detectKey(self, cells):
		if cells:
			cells = map(ocr.deskew, cells)
			samples = ocr.preprocess_hog(cells)
			key = self.model.predict(samples)
			"""
			@todo we must not accept responses too far away from any match. Every noise will be translated into a number
			"""
			return ''.join(str(int(y)) for y in key)

		return None

	def assignStatus(self, card):
		if self.lane_separators == None:
			self.findLines()

		status = 0
		if self.lane_separators != None:
			for line_x in self.lane_separators:
				if card.x < line_x:
					return status 
				status=status+1

		return None

	def hasCards(self):
		return len(self._cards) > 0

	def doSaveTrainingFile(self, card):
		if self.saveTrainingFile:
			grid = common.mosaic(len(card.key), card.cells)
			filename = '%s/%s.png' % (self.train_inbox_path, card.key)
			cv2.imwrite(filename, grid)

	def findLines(self):
		"""analyzes an image and returns all lines

		:param board_img_file: filename of an image of the entire board
		:returns: A SimpleCV FeatureSet
		:rtype: SimpleCV.Features.Features.FeatureSet
		"""
		img = self._image.binarize(thresh=50).morphClose()
#		lines = self._image.findLines(minlinelength=self._image.height*.5, maxlinegap=self._image.height*.5, maxpixelgap=1, threshold=150)

		lines = img.findBlobs(minsize=self._image.height)
		if lines:
			self.lane_separators = lines.x()
			self.lane_separators.sort()
			return lines
		return None

	def save(self):
		self._image.save('save.jpg')
	
	@property
	def keys(self):
		return [card.key for card in self._cards.values()]
	
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

	def show(self, img=None, t=2):
		if img is None:
			img = self._image
		img.show()
		time.sleep(t)
