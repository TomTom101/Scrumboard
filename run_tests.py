#!/usr/bin/python

import unittest

from tests import board_test
from SimpleCV import *


loader = unittest.TestLoader()

suite = loader.loadTestsFromModule(board_test)

#suite.addTests(loader.loadTestsFromModule(datafile_test))



runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)
