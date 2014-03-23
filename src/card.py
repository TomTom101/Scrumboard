import time
from SimpleCV import Color

class Card(object):

    def __init__(self, img):
        """ after binarization, increase canvas each side by 1px and fill
         with black.
        This way all areas that touch
        the card will also be filled, like lines the card is hung over.
        The floodFill point can be any on the edge.
        """
        self._image = img.binarize(thresh=95).morphClose().dilate().embiggen((img.width+2, img.height+2), color=Color.WHITE).floodFill((0, 0), color=Color.BLACK)
        self._status = None
        self._key = None
        self._x = 0
        # Filter out noise. The size of course depends on the card dimension. This might be too much when cards are really small.
        self.minsize = 50
        self.cells = self._extract_cells()

    def _extract_cells(self):
        fs = self._image.findBlobs(minsize=self.minsize)

        if fs:
            chars = fs.sortY()

            # Find Y position of the char that is the first from top to bottom
            #  and allow characters that start 50% below
            upmost_char_y = chars[0].mMinRectangle[0][1] * 1.5
            chars = chars.filter(chars.y() <= upmost_char_y)
            cells = []
            for char in chars.sortX():
                # discard if w/h;h/w ratio > 2
                # tbdone
                char.image = self._image
                char.drawMinRect(width=4, color=(0, 255, 0))
                char_box = char.boundingBox()
                # Creates a tuple with 2 identical values of the longest side + 2px. e.g. for w*h = 65*70 == (72,72)
                canvas = tuple([(max(char_box[-2:])+2) for x in range(2)])
                digit = self._image.crop(char).embiggen(canvas).resize(20, 20)
                #digit.show()
                #time.sleep(.5)
                cells.append(digit.getGrayNumpyCv2())
            return cells

        return None

    def show(self, img=None, t=2):
        if img is None:
            img = self._image
        img.show()
        time.sleep(t)

    @property
    def status(self):
        return self._status
    @status.setter
    def status(self, value):
        if(self._status is not None and value != self._status):
            print "Value changed of WWW-%s!" % self._key
        self._status = value

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

