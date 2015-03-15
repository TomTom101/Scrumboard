#!/usr/bin/python

import cProfile
from scrumboard import board


def changedStatus(key, status):
    pass

Myboard = board.Board(save_training_file=False)
Myboard.image = '/Users/thobra/Dev/scrumboard/tests/data/board_ni_2.JPG'
Myboard.findLines()

def run():
    global Myboard
    Myboard.image = '/Users/thobra/Dev/scrumboard/tests/data/board_ni_2.JPG'
    Myboard.findCards()
    if Myboard.hasCards():
        print Myboard.list_cards
        Myboard.card("2600").status = 4
run()
#cProfile.run("run()")
