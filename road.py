#coding:utf-8
#!/usr/bin/env python
import numpy as np
import sys
import random

HAVECAR = 1
WALL = 2
EMPTY = 0
PROBSLOW = 0.1


class Road(object):
    def __init__(self, length, lanes, vmax, prob_in):
        self.length = length
        self.lanes = lanes
        self.positionArray = np.zeros((lanes + 2, length))
        self.speedArray = np.zeros((lanes + 2, length))
        self.positionArray[0, :] = WALL
        self.positionArray[lanes + 1, :] = WALL
        self.speedArray[0, :] = WALL
        self.speedArray[lanes + 1, :] = WALL
        self.vmax = vmax
        self.prob_in = prob_in
    def progress(self, limit_speed = 0, limit_begin = 0, limit_end = 0, is_limit = False):
        positionArray = self.positionArray
        speedArray = self.speedArray
        #中间量：只有减速步的时候用
        gap = np.zeros(positionArray.shape)
        gap_position_temp = sys.maxint
        for i in range(1, positionArray.shape[0] - 1):
            for j in range(positionArray.shape[1] - 1, -1, -1):
                #计数器，第1辆车和第2辆车减速步特殊处理
                count = 1
                '''加速步骤begin'''
                if positionArray[i, j] == 1 and not is_limit:
                    speedArray[i, j] = min(speedArray[i, j] + 1, self.vmax)
                elif is_limit and limit_begin < j < limit_end:
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
                        is_limit and limit_begin < gap_position_temp < limit_end) else self.vmax
                        vq = min(vmax_before - 1, d)
                        speedArray[i, j] = min(speedArray[i, j], gap[i, j] + vq)
                '''减速步end'''
                '''随机慢化步begin'''
                if (positionArray[i, j] == 1 and random.uniform(0, 1) <= PROBSLOW):
                    speedArray[i, j] = max(speedArray[i, j] - 1, 0)
                '''随机慢化步end'''
                '''Nasch位置更新步begin'''
                if(positionArray[i, j] == 1):
                    position_next = int(j + speedArray[i, j])
                    if (position_next != j):
                        if(position_next < positionArray.shape[1]):
                            positionArray[i, position_next] = 1
                            speedArray[i, position_next] = speedArray[i, j]
                        positionArray[i, j] = 0
                        speedArray[i, j] = 0
                '''Nasch位置更新步end'''
                count += 1

        return positionArray

