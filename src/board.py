
import os, time
from SimpleCV import Image
from src.digits import digits as ocr
from src.digits import common
import src.card as c
import cv2

class Board(object):
    """ Board handles everything concerning the overall organization of
    the entire board.
    """
    # Location of HOG data file
    SVMData = 'own_digits_svm.dat'
    # By what factor should the board be scaled down
    ScaleBoard = .1
    def __init__(self, save_training_file=False):
        self.save_training_file = save_training_file
        self._image = None
        self._imageprocessed = None
        self._minsize = 0
        self._num_cards = 0
        self._cards = {}
        self.find_colors = [(160, 140, 40), (125, 140, 60)]
        self.lane_separators = None

        self.model = ocr.SVM()
        if not self.model.load(Board.SVMData):
            raise Exception("SVM data could not be loaded: %s" % Board.SVMData)

        self.train_inbox_path = os.path.join(os.path.dirname(__file__), 'train/inbox')

    def _preprocess(self, img):
        return img.scale(Board.ScaleBoard)

    @property
    def image(self):
        return self._image
    @image.setter
    def image(self, image):
        if not image.__class__.__name__ == 'Image':
            image = Image(image)
        self._imageprocessed = self._preprocess(image)
        area = float(self._imageprocessed.width*self._imageprocessed.height)
        self._minsize = area/500
        self._image = image

    def card(self, key):
        return self._cards[key]


    def findCards(self): #pylint: disable=C0103
        """analyzes an image and returns all blobs

        :returns: A SimpleCV FeatureSet
        :rtype: SimpleCV.Features.Features.FeatureSet
        """
        if not self._image:
            raise Exception("Must set Board.image first!")
        img = self._imageprocessed.hueDistance(self.find_colors[0]).morphClose().binarize(thresh=15)

        fs = img.findBlobs(minsize=self.minsize)

        if fs:
            self._num_cards = len(fs)
            for b in fs.sortX():
                b.image = self._image
                card_img = self._prepareCardBlob(b)
                card = c.Card(card_img)
                card.key = self.detectKey(card.cells)

                if card.key:
                    card.x = b.x
                    card.status = self._assign_status(card)
                    self._cards[card.key] = card
                    self.dosave_training_file(card)
                #b.image = img#.self._image
                #b.drawMinRect(color=Color.BLUE, width=3)
            #self.show(img)
        return self._cards

    def _prepareCardBlob(self, blob):
        if abs(blob.angle()) > 45:
            return self._image
        size_up_factor = 1/Board.ScaleBoard
        crop_region = map(lambda x: ((size_up_factor*x[0], size_up_factor*x[1])), blob.points)
        #crop_region = blob
        img = self._image.crop(crop_region, centered=False).rotate(blob.angle(), point=[0, 0], fixed=True)
        #self.show(img)
        crop = self._getPostRotationCropRegion(blob)

        if crop is not None:
            img = img.crop(crop)
        #self.show(img)
        return img

    def _getPostRotationCropRegion(self, blob):
        x, y = (0, 0)
        # clock-wise, crop y
        w = blob.minRectWidth()
        h = blob.minRectHeight()
        size_up_factor = 1/Board.ScaleBoard
        rect = blob.minRect()
        rect = map(lambda x: ((size_up_factor*x[0], size_up_factor*x[1])), rect)
        if blob.angle() > .0:
            # counter clock-wise, crop x
            x += rect[1][0]-rect[0][0]
            w = blob.minRectHeight()
            h = blob.minRectWidth()
        elif blob.angle() < .0:
            y += rect[0][1]-rect[1][1]

        #print "angle: %.2f, x, y: %d, %d, w: %d, h: %d" % (blob.angle(), x, y, w, h)

        return (x, y, w*size_up_factor-15, h*size_up_factor-15)

    def detectKey(self, cells): #pylint: disable=C0103
        if cells:
            cells = map(ocr.deskew, cells)
            samples = ocr.preprocess_hog(cells)
            key = self.model.predict(samples)

            # @todo we must not accept responses too far away from any match.
            # Every noise will be translated into a number.

            return ''.join(str(int(y)) for y in key)

        return None

    def _assign_status(self, card):
        if self.lane_separators == None:
            self.findLines()

        status = 0
        if self.lane_separators != None:
            for line_x in self.lane_separators:
                if card.x < line_x:
                    return status
                status = status+1

        return None

    def hasCards(self): #pylint: disable=C0103
        return len(self._cards) > 0

    def dosave_training_file(self, card):
        if self.save_training_file:
            grid = common.mosaic(len(card.key), card.cells)
            filename = '%s/%s.png' % (self.train_inbox_path, card.key)
            cv2.imwrite(filename, grid)

    def findLines(self): #pylint: disable=C0103
        """analyzes an image and returns all lines

        :param board_img_file: filename of an image of the entire board
        :returns: A SimpleCV FeatureSet
        :rtype: SimpleCV.Features.Features.FeatureSet
        """
        img = self._image.binarize(thresh=50).morphClose()
#       lines = self._image.findLines(minlinelength=self._image.height*.5, maxlinegap=self._image.height*.5, maxpixelgap=1, threshold=150)

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
    def list_cards(self):
        return [{"key": card.key, "status": card.status} for (key, card) in self._cards.items()]

    @property
    def num_cards(self):
        return self._num_cards

    def show(self, img=None, time=1):
        if img is None:
            img = self._image
        img.show()
        time.sleep(time)
