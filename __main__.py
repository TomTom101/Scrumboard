#!/usr/bin/python

import cProfile
from src import board

Myboard = board.Board(save_training_file=False)
Myboard.image = '/Users/thobra/scrumboard/tests/data/board_ni_2.JPG'
Myboard.findLines()

def run():
    global Myboard
    Myboard.image = '/Users/thobra/scrumboard/tests/data/board_ni_2.JPG'
    Myboard.findCards()
    if Myboard.hasCards():
        print Myboard.keys

cProfile.run("run()")
