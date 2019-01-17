#!/usr/bin/env python
import numpy as np

HAVECAR = 1
WALL = 2
EMPTY = 0

class Road(object):
    def __init__(self, length, lanes):
        self.length = length
        self.lanes = lanes
        self.positionArray = np.zeros((lanes + 2, length))
        self.speedArray = np.zeros((lanes + 2, length))
        self.positionArray[0, :] = WALL
        self.positionArray[lanes + 1, :] = WALL
        self.speedArray[0, :] = WALL
        self.speedArray[lanes + 1, :] = WALL
    # def progress(self):

