import scrumboard
import os, time
from SimpleCV import Color, Image
from scrumboard.digits import digits as ocr
from scrumboard.digits import common
import scrumboard.card as c
import cv2

class Board(object):
    """ Board handles everything concerning the overall organization of
    the entire board.
    """
    # Location of HOG data file
    SVMData = 'own_digits_svm.dat'
    # By what factor should the board be scaled down
    ScaleBoard = .2
    # What colors to look for
    FindColors = [(160, 140, 40), (125, 140, 60)]
    def __init__(self, save_training_file=False):
        self.save_training_file = save_training_file
        self._image = None
        self._imageprocessed = None
        # MIST - behelf:
        self._imageprocessed2 = None
        self._minsize = 0
        self._blobs = None
        self._num_cards = 0
        self._cards = {}
        self.lane_separators = None

        self.model = ocr.SVM()
        if not self.model.load(Board.SVMData):
            raise Exception("SVM data could not be loaded: %s" % Board.SVMData)

        self.train_inbox_path = os.path.join(os.path.dirname(__file__), 'train/inbox')
        scrumboard.load_config()

    def _preprocess(self, img):
        return img.scale(Board.ScaleBoard)



    def findLines(self): #pylint: disable=C0103
        """analyzes an image and returns all lines

        :param board_img_file: filename of an image of the entire board
        :returns: A SimpleCV FeatureSet
        :rtype: SimpleCV.Features.Features.FeatureSet
        """
        self._imageprocessed_lines = self._imageprocessed.binarize(thresh=40).morphClose() \
            .crop(  x=0, y=self._imageprocessed.height*.25, \
                    w=self._imageprocessed.width, \
                    h=self._imageprocessed.height*.75)

        # lines = img.findLines(
        #     minlinelength=self._imageprocessed_lines.height*.5,
        #     maxlinegap=self._imageprocessed_lines.height*.5,
        #     maxpixelgap=1,
        #     threshold=200)

        lines = self._imageprocessed_lines.findBlobs(minsize=self._imageprocessed_lines.height)
        if lines:
            #lines.image = img
#            lines.draw()
            self.lane_separators = lines.x()
            self.lane_separators.sort()
            return lines
        return None

    def findCards(self): #pylint: disable=C0103
        """analyzes an image and returns all blobs

        :returns: A SimpleCV FeatureSet
        :rtype: SimpleCV.Features.Features.FeatureSet
        """
        if not self._image:
            raise Exception("Must set Board.image first!")

        thresh = float(scrumboard.config.get('settings', 'binarize_threshold'))
        self._imageprocessed_cards = self._imageprocessed \
                .hueDistance(Board.FindColors[0]) \
                .binarize(thresh=thresh) \
                .morphOpen()

        self._blobs = self._imageprocessed_cards.findBlobs(minsize=self.minsize)

        if self._blobs:
            for b in self._blobs.sortX():
                card_img = self._prepareCardBlob(b)
                card = c.Card(card_img)
                card.key = self.detectKey(card.cells)

                if card.key:
                    card.x = b.x
                    card.status = self._assign_status(card)
                    self._cards[card.key] = card
                    self.dosave_training_file(card)

        return self._cards


    def _prepareCardBlob(self, blob):
        if abs(blob.angle()) > 45:
            return self._image
        size_up_factor = 1/Board.ScaleBoard
        crop_region = map(lambda x: ((size_up_factor*x[0], size_up_factor*x[1])), blob.points)
        #crop_region = blob
        img = self._image.crop(crop_region, \
            centered=False).rotate(blob.angle(), \
            point=[0, 0], \
            fixed=True)
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

    def save(self):
        self._imageprocessed.save('save.jpg')

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
        return len(self._blobs)

    def draw(self, img=None, save=False):
        if self._blobs is not None:
            if img is None:
                img = self._imageprocessed
            for b in self._blobs:
                b.image = img
                b.drawMinRect(color=Color.RED, width=5)
                if save:
                    c_jpg = os.path.join(scrumboard.config \
                        .get('config', 'static_file_path'), 'cards.jpg')
                    img.save(c_jpg)

    def show(self, img=None, sec=1):
        if img is None:
            img = self._imageprocessed
        img.show()
        time.sleep(sec)
