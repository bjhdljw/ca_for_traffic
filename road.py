#coding:utf-8
#!/usr/bin/env python
import numpy as np
import sys
import random
import csv

HAVECAR = 1
WALL = 2
EMPTY = 0
PROBSLOW = 0.1


class Road(object):
    def __init__(self, length, lanes, vmax, prob_in, islimit, limit_begin, limit_end, lane_for_st_figure):
        self.length = length
        self.lanes = lanes
        self.positionArray = np.zeros((lanes + 2, length))
        self.speedArray = np.zeros((lanes + 2, length))
        self.speedCounter = np.zeros((lanes + 2, length))
        self.positionArray[0, :] = WALL
        self.positionArray[lanes + 1, :] = WALL
        self.speedArray[0, :] = WALL
        self.speedArray[lanes + 1, :] = WALL
        self.speedCounter[0, :] = WALL
        self.speedCounter[lanes + 1, :] = WALL
        self.vmax = vmax
        self.prob_in = prob_in
        self.is_limit = islimit
        self.limit_begin = limit_begin
        self.limit_end = limit_end
        self.lane_for_st_figure = lane_for_st_figure
        self.count_flow = 0
        self.travel_time = 0
        self.travel_speed = 0
    def progress(self, speed):
        if not self.is_limit:
            limit_speed = self.vmax
        else:
            limit_speed = speed
        positionArray = self.positionArray
        speedArray = self.speedArray
        speedCounter = self.speedCounter
        #中间量：只有减速步的时候用
        gap = np.zeros(positionArray.shape)
        gap_position_temp = sys.maxint
        for i in range(1, positionArray.shape[0] - 1):
            # 计数器，第1辆车和第2辆车减速步特殊处理
            count = 1
            for j in range(positionArray.shape[1] - 1, -1, -1):
                '''加速步骤begin'''
                if positionArray[i, j] == 1 and not self.is_limit:
                    speedArray[i, j] = min(speedArray[i, j] + 1, self.vmax)
                elif positionArray[i, j] == 1 and self.is_limit and self.limit_begin <= j <= self.limit_end:
                    speedArray[i, j] = min(speedArray[i, j] + 1, limit_speed)
                '''加速步骤end'''
                '''计算前车距离begin'''
                if(positionArray[i, j] == 1):
                    gap[i, j] = gap_position_temp - j
                    gap_position_temp = j
                '''计算前车距离end'''
                '''减速步begin'''
                if (positionArray[i, j] == 1):
                    if count == 1:
                        pass
                    elif count == 2:
                        speedArray[i, j] = min(speedArray[i, j], gap[i, j] - 1)
                    else:
                        d = max(0, gap[i, gap_position_temp] - 1)
                        vmax_before = limit_speed if (
                        self.is_limit and self.limit_begin <= gap_position_temp <= self.limit_end) else self.vmax
                        vq = min(vmax_before - 1, d)
                        speedArray[i, j] = min(speedArray[i, j], gap[i, j] + vq)
                    count += 1
                '''减速步end'''
                '''随机慢化步begin'''
                if (positionArray[i, j] == 1 and random.uniform(0, 1) <= PROBSLOW):
                    speedArray[i, j] = max(speedArray[i, j] - 1, 0)
                '''随机慢化步end'''
                '''行程开始时间累计begin'''
                if self.limit_begin <= j <= self.limit_end and speedCounter[i, j] != 0:
                    speedCounter[i, j] += 1
                '''行程开始时间累计end'''
                '''Nasch位置更新步begin'''
                if(positionArray[i, j] == 1):
                    position_next = int(j + speedArray[i, j])
                    if (position_next != j):
                        '''流量&总行程时间&总行程车速统计begin'''
                        if j <= self.limit_end <= position_next:
                            self.count_flow += 1
                            self.travel_time += speedCounter[i, j]
                            self.travel_speed += (self.limit_end - self.limit_begin) / speedCounter[i, j]
                        '''流量&总行程时间&总行程车速统计end'''
                        if(position_next < positionArray.shape[1]):
                            positionArray[i, position_next] = 1
                            speedArray[i, position_next] = speedArray[i, j]
                            speedCounter[i, position_next] = speedCounter[i, j]
                        positionArray[i, j] = 0
                        speedArray[i, j] = 0
                        speedCounter[i, j] = 0
                '''Nasch位置更新步end'''
            '''为时空图做准备begin'''
            prepare_space_time(positionArray, self.lane_for_st_figure)
            '''为时空图做准备begin'''
        return positionArray


def prepare_space_time(positionArray, lane):
    out = open('space_time.csv', mode='a')
    csv_writer = csv.writer(out, dialect='excel')
    csv_writer.writerow(positionArray[lane, :])

