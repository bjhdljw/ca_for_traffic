#coding:utf-8
#!/usr/bin/env python


class Car(object):

    def __init__(self, length = 1):
        # TODO 目前只支持车辆长度为1元胞
        self.lenghth = length

    @staticmethod
    def new_car(car, road, speed, lane):
        if road.positionArray[lane, 0] == 0:
            road.speedArray[lane, 0: car.lenghth] = speed
            road.positionArray[lane, 0: car.lenghth] = 1
            road.speedCounter[lane, 0: car.lenghth] = 1