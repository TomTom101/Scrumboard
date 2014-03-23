#!/usr/bin/python

import cProfile
from src import board
 #['2551', '2590', '2546', '2611', '2486', '2484', '2358', '2483', '2455', '258', '2518', '2501', '2600', '2481', '2361']
#        ['2590', '2546', '2611', '55', '2484', '2483', '2455', '2481', '2486', '258', '2600', '236', '251', '250', '358']

myboard = board.Board(saveTrainingFile=False)
myboard.image = '/Users/thobra/scrumboard/tests/data/board_ni_2.JPG'
myboard.findLines()

def run():
	global myboard
	myboard.image = '/Users/thobra/scrumboard/tests/data/board_ni_2.JPG'
	myboard.findCards()
	if myboard.hasCards():
		print myboard.keys
		#myboard.showImage()
		#myboard.save()
		#time.sleep(5)

cProfile.run("run()")

"""
cam = Camera()
i = cam.getImage()
disp = Display(resolution=(i.width*2, i.height*2))
myboard = myboard.myBoard()

while not disp.isDone():
	myboard.image = cam.getImage()
	myboard.findCards()
	if myboard.hasCards():
		print myboard.keys
	myboard.showImage()
	#time.sleep(1)


disp.quit()
exit()
"""