#!/usr/bin/python
from SimpleCV import *
from src import board

# def show(img, t=2):
# 	if img is not None:
# 		img.show()
# 		time.sleep(t)

# i = Image('/Users/thobra/Dropbox/board_1.JPG').scale(.2)

# i = i.hueDistance((160, 140, 40)).morphClose().binarize(thresh=25)
# fs = i.findBlobs(minsize=200).sortArea()
# for b in fs[1:]:
# 	#b = fs[-3]
# 	b.drawRect(width=5, color=Color.RED)
# 	show(i)
# 	im=i.crop(b, centered=False)
# 	show(im)
# 	rect = b.minRect()
# 	im=im.rotate(b.angle(), point=[0,0], fixed=True)
# 	show(im)
# 	# if rect[3][1] > rect[1][1] > nur x crop, y = 0, +angle?
# 	# rechtsdrehung is -angle!
# 	"""
# 	((97.16923147645254, 199.04614215666575),
# 	(227.7107773100413, 191.79383415890922),
# 	(92.27692410597435, 110.98460822390328),
# 	(222.8184699395631, 103.73230022614675))
# 	angle: -3.18, x, y: 130, 88
# 	((253.93755973118397, 95.97698700172268),
# 	(256.64334831562815, 10.294014379584635),
# 	(123.21529426249684, 91.84889943877474),
# 	(125.92108284694102, 6.165926816636702))
# 	angle: 1.81, x, y: 2, 4
# 	"""
# 	x, y, w, h = (2, 2, -2, -2)
# 	if b.angle() < -1.:
# 		# clock-wise, crop y
# 		y += rect[0][1]-rect[1][1]
# 		w += b.minRectWidth()
# 		h += b.minRectHeight()
# 	elif b.angle() > 1.:
# 		# counter clock-wise, crop x
# 		w += b.minRectHeight()
# 		h += b.minRectWidth()
# 		x += rect[1][0]-rect[0][0]
	
# 	im=im.crop(x, y, w, h)
# 	show(im)
# 	print "angle: %.2f, x, y: %d, %d, w: %d, h: %d" % (b.angle(), x, y, w, h)

# exit()

board = board.Board(saveTrainingFile=False)
board.image = '/Users/thobra/Dropbox/board_2.JPG'
board.findCards()
if board.hasCards():
	print board.keys
	#board.showImage()
	board.save()
	#time.sleep(5)

"""
cam = Camera()
i = cam.getImage()
disp = Display(resolution=(i.width*2, i.height*2))
board = board.Board()

while not disp.isDone():
	board.image = cam.getImage()
	board.findCards()
	if board.hasCards():
		print board.keys
	board.showImage()
	#time.sleep(1)


disp.quit()
exit()