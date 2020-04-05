# coding:utf-8
# !/usr/bin/env python
import random

SIDE_SIDE = 0.5
MAIN_MAIN = 0.7


class Car(object):

    def __init__(self, length = 1):
        # TODO 目前只支持车辆长度为1元胞
        self.length = length

    @staticmethod
    def new_car(car, road, speed, lane):
        if road.position_array[lane, 0] == 0:
            if lane == 6 or lane == 7:
                road.speed_array[lane, 0: car.length] = speed
                road.position_array[lane, 0: car.length] = 1
                road.speed_counter[lane, 0: car.length] = 0
                if random.uniform(0, 1) <= SIDE_SIDE:
                    road.des_array[lane, 0: car.length] = 3
                else:
                    road.des_array[lane, 0: car.length] = 4
            elif 5 > lane > 0:
                pass
                road.speed_array[lane, 0: car.length] = speed
                road.position_array[lane, 0: car.length] = 1
                road.speed_counter[lane, 0: car.length] = 0
                if random.uniform(0, 1) < MAIN_MAIN:
                    road.des_array[lane, 0: car.length] = 1
                else:
                    road.des_array[lane, 0: car.length] = 2
