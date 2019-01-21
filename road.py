#coding:utf-8
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
    def progress(self):
        positionArray = self.positionArray
        speedArray = self.speedArray
        for i in range(1, positionArray.shape[0] - 2):
            for j in range(positionArray.shape[1] - 1, -1, -1):
                #Nasch位置更新步
                if(positionArray[i, j] == 1):
                    position_next = int(j + speedArray[i, j])
                    if (position_next != j):
                        if(position_next < positionArray.shape[1]):
                            positionArray[i, position_next] = 1
                            speedArray[i, position_next] = speedArray[i, j]
                        positionArray[i, j] = 0
                        speedArray[i, j] = 0

        return positionArray

