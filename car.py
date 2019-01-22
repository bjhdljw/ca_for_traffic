#!/usr/bin/env python


class Car(object):

    def __init__(self, length = 1):
        self.lenghth = length

    @staticmethod
    def new_car(car, road, speed, lane):
        if road.positionArray[lane, 0] == 0:
            road.speedArray[lane, 0] = speed
            road.positionArray[lane, 0: car.lenghth] = 1