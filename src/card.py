class Card(object):

	def __init__(self, blob):
		self.blob = blob
		self.key = self.__extractKey()
		self.status = None

	def __extractKey(self):
		return None


	