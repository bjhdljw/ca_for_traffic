#!/usr/bin/env python

class Car(object):

    def __init__(self, length = 1):
        self.lenghth = length

    def new_car(self, road, speed, lane):
        road.positionArray[lane, 0 : self.lenghth] = 1
        road.speedArray[lane, 0] = speed