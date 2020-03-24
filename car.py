#coding:utf-8
#!/usr/bin/env python
import random

SIDE_SIDE = 0.8
MAIN_MAIN = 0.8


class Car(object):

    def __init__(self, length = 1):
        # TODO 目前只支持车辆长度为1元胞
        self.length = length

    @staticmethod
    def new_car(car, road, speed, lane):
        if road.positionArray[lane, 0] == 0:
            road.speedArray[lane, 0: car.length] = speed
            road.positionArray[lane, 0: car.length] = 1
            road.speedCounter[lane, 0: car.length] = 1
            if lane == 6 or lane == 7:
                if random.uniform(0, 1) <= SIDE_SIDE:
                    road.desArray[lane, car.length] = 3
                else:
                    road.desArray[lane, car.length] = 4
            elif 5 > lane > 0:
                if random.uniform(0, 1) <= MAIN_MAIN:
                    road.desArray[lane, car.length] = 1
                else:
                    road.desArray[lane, car.length] = 2
