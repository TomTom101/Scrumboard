#!/usr/bin/python
from SimpleCV import *
from src import board


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