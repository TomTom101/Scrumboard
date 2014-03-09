#!/usr/bin/python

import signal
import sys, time
from SimpleCV import *

img = Image("data/board_simple.jpg")


y = Color.hsv((202, 152, 50))
y_dist = img.hueDistance((200, 160, 55)).dilate().binarize(thresh=25)

lines_ = img.binarize()
lines = lines_.findLines()
lines.show()
time.sleep(8)
cards = y_dist.findBlobs(minsize=2000)
cards.draw(width=2)
#cards.show(width=3)

for card in cards:
	print card
	card.drawMinRect(width=3)

y_dist.image = img
img.addDrawingLayer(y_dist.dl())
#img = img - y_dist 
img.show()
time.sleep(8)