import time

class Card(object):

	def __init__(self, img_card):
		self.img_card = img_card
		self.status = None
		self.minsize = self.img_card.area() * .006
		self.key = self.__extractKey()

	def __extractKey(self):
		""" Need be filled
		"""
		self.img_card= self.img_card.binarize(thresh=90).morphClose().morphClose()

		fs = self.img_card.findBlobs(minsize=self.minsize)
		if fs:
			fs.draw()
			fs.image = self.img_card	
			for b in fs:
				r = b.drawMinRect(width=4, color=(255,0,0))
				bb = b.boundingBox()
				canvas = tuple([max(bb[-2:]) for x in range(2)])
				digit = self.img_card.crop(b).embiggen(canvas)
				time.sleep(1)

			#self.img_card.show()
			return str(len(fs)) * 4
		return None


	