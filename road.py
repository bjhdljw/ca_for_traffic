#coding:utf-8
#!/usr/bin/env python
import numpy as np
import sys
import random
import csv

HAVECAR = 1
WALL = 3
EMPTY = 0
PROBSLOW = 0.1


class Road(object):
    def __init__(self, length, lanes, vmax, prob_in, islimit, limit_begin, limit_end, lane_for_st_figure, switch_lane_prob, limit_speed, congestion_point_lane, congestion_point_point, time_can_wait, switch_left_prob, congestion_length):
        self.length = length
        self.lanes = lanes
        self.positionArray = np.zeros((lanes + 2, length))
        self.speedArray = np.zeros((lanes + 2, length))
        self.speedCounter = np.zeros((lanes + 2, length))
        self.timeWaited = np.zeros((lanes + 2, length))
        self.positionArray[0, :] = WALL
        self.positionArray[lanes + 1, :] = WALL
        self.speedArray[0, :] = WALL
        self.speedArray[lanes + 1, :] = WALL
        self.speedCounter[0, :] = WALL
        self.speedCounter[lanes + 1, :] = WALL
        self.timeWaited[0, :] = WALL
        self.timeWaited[lanes + 1, :] = WALL
        self.vmax = vmax
        self.prob_in = prob_in
        self.is_limit = islimit
        self.limit_begin = limit_begin
        self.limit_end = limit_end
        self.lane_for_st_figure = lane_for_st_figure
        self.count_flow = 0
        self.travel_time = 0
        self.travel_speed = 0
        self.switch_lane_prob = switch_lane_prob
        self.switch_counter = 0
        self.limit_speed = limit_speed
        self.congestion_point_lane = congestion_point_lane
        self.congestion_point_point = congestion_point_point
        self.congestion_length = congestion_length
        self.positionArray[congestion_point_lane, congestion_point_point : congestion_point_point + congestion_length] = 2
        self.time_can_wait = time_can_wait
        self.switch_left_prob = switch_left_prob
    def progress(self, speed):
        limit_speed = speed
        positionArray = self.positionArray
        speedArray = self.speedArray
        speedCounter = self.speedCounter
        timeWaited = self.timeWaited
        #中间量：只有减速步的时候用
        gap = np.zeros(positionArray.shape)
        left_change_condition = np.zeros(positionArray.shape)
        right_change_condition = np.zeros(positionArray.shape)
        left_change_real = np.zeros(positionArray.shape)
        right_change_real = np.zeros(positionArray.shape)
        for i in range(1, positionArray.shape[0] - 1):
            gap_position_temp = sys.maxint
            for j in range(positionArray.shape[1] - 1, -1, -1):
                '''确定当前的vmax：vmax or limit_speed'''
                vmax = self.vmax
                if positionArray[i, j] == 1:
                    vmax = limit_speed if (positionArray[i, j] == 1 and self.is_limit and self.limit_begin <= j <= self.limit_end) else self.vmax
                '''确定当前的vmax：vmax or limit_speed'''
                '''加速步骤begin'''
                speedArray[i, j] = min(speedArray[i, j] + 1, vmax)
                '''加速步骤end'''
                '''计算前车距离begin'''
                if positionArray[i, j] == 1 or positionArray[i, j] == 2:
                    if gap_position_temp - j - 1 < 0:
                        raise RuntimeError('gap error')
                    gap[i, j] = gap_position_temp - j - 1
                    gap_position_temp = j
                '''计算前车距离end'''
                '''行程开始时间累计begin'''
                if self.limit_begin <= j <= self.limit_end and speedCounter[i, j] != 0:
                    speedCounter[i, j] += 1
                '''行程开始时间累计end'''
            '''为时空图做准备begin'''
            prepare_space_time(positionArray, self.lane_for_st_figure)
            '''为时空图做准备begin'''
        '''逐车道换道begin'''
        for i in range(1, self.lanes + 1):
            switch_lane(positionArray, i, self.lanes, self.vmax, right_change_condition, left_change_condition,
                        speedArray, gap, left_change_real, right_change_real, self.switch_lane_prob, speedCounter, self, timeWaited)
        '''逐车道换道end'''
        '''换道后更新前车距离begin'''
        gap = np.zeros(positionArray.shape)
        for i in range(1, positionArray.shape[0] - 1):
            gap_position_temp = sys.maxint
            for j in range(positionArray.shape[1] - 1, -1, -1):
                if positionArray[i, j] == 1 or positionArray[i, j] == 2:
                    if gap_position_temp - j - 1 < 0:
                        raise RuntimeError('gap error')
                    gap[i, j] = gap_position_temp - j - 1
                    gap_position_temp = j
        '''换道后更新前车距离end'''
        '''减速步、随机慢化步begin'''
        for i in range(1, positionArray.shape[0] - 1):
            # 计数器，第1辆车和第2辆车减速步特殊处理
            count = 1
            gap_position_temp2 = sys.maxint
            for j in range(positionArray.shape[1] - 1, -1, -1):
                '''确定当前的vmax：vmax or limit_speed'''
                vmax = limit_speed if (positionArray[i, j] == 1 and self.is_limit and self.limit_begin <= j <= self.limit_end) else self.vmax
                '''确定当前的vmax：vmax or limit_speed'''
                '''减速步begin'''
                if positionArray[i, j] == 1 or positionArray[i, j] == 2:
                    if positionArray[i, j] == 2:
                        pass
                    elif gap_position_temp2 < positionArray.shape[1] and positionArray[i, gap_position_temp2] == 2:
                        temp_speed = min(speedArray[i, j], gap[i, j])
                        speedArray[i, j] = max(temp_speed, 0)
                    elif count == 1:
                        pass
                    elif count == 2:
                        temp_speed = min(speedArray[i, j], gap[i, j])
                        speedArray[i, j] = max(temp_speed, 0)
                    else:
                        d = max(0, gap[i, gap_position_temp2] - 1)
                        vmax_before = limit_speed if (self.is_limit and self.limit_begin <= gap_position_temp2 <= self.limit_end) else self.vmax
                        vq = min(vmax_before - 1, d)
                        vq = min(vq, speedArray[i, gap_position_temp2])
                        speedArray[i, j] = min(speedArray[i, j], gap[i, j] + vq)
                        if speedArray[i, j] > d + gap[i, j]:
                            raise RuntimeError('ve error')
                    count += 1
                    gap_position_temp2 = j
                    if speedArray[i, j] < 0:
                        raise RuntimeError('v error')
                '''减速步end'''
                '''随机慢化步begin'''
                if (positionArray[i, j] == 1 and random.uniform(0, 1) <= PROBSLOW):
                    speedArray[i, j] = max(speedArray[i, j] - 1, 0)
                '''随机慢化步end'''
        '''减速步、随机慢化步end'''
        for i in range(1, positionArray.shape[0] - 1):
            for j in range(positionArray.shape[1] - 1, -1, -1):
                '''Nasch位置更新步begin'''
                if (positionArray[i, j] == 1):
                    position_next = int(j + speedArray[i, j])
                    if position_next != j:
                        if position_next < positionArray.shape[1] and position_next != 1:
                            for c in range(j + 1, position_next + 1):
                                if positionArray[i, c] == 1:
                                    print 'i= %d' % i
                                    print 'j= %d' % j
                                    print 'c= %d' % c
                                    print 'i speed= %d' % speedArray[i, j]
                                    print 'position_next= %d' % position_next
                                    raise RuntimeError('car conflict')
                                if positionArray[i, c] == 2:
                                    print 'i= %d' % i
                                    print 'j= %d' % j
                                    print 'c= %d' % c
                                    print 'i speed= %d' % speedArray[i, j]
                                    print 'position_next= %d' % position_next
                                    print 'gap= %d' % gap[i, j]
                                    raise RuntimeError('congestion conflict')
                        '''流量&总行程时间&总行程车速统计begin'''
                        if j <= self.limit_end <= position_next:
                            self.count_flow += 1
                            self.travel_time += speedCounter[i, j]
                            self.travel_speed += (self.limit_end - self.limit_begin) / speedCounter[i, j]
                        '''流量&总行程时间&总行程车速统计end'''
                        if (position_next < positionArray.shape[1]):
                            positionArray[i, position_next] = 1
                            speedArray[i, position_next] = speedArray[i, j]
                            speedCounter[i, position_next] = speedCounter[i, j]
                            timeWaited[i, position_next] = 0
                        positionArray[i, j] = 0
                        speedArray[i, j] = 0
                        speedCounter[i, j] = 0
                        timeWaited[i, j] = 0
                    elif position_next == j and j != 0:
                        timeWaited[i, j] += 1
                '''Nasch位置更新步end'''
        return positionArray


def prepare_space_time(positionArray, lane):
    out = open('space_time.csv', mode='a')
    csv_writer = csv.writer(out, dialect='excel')
    csv_writer.writerow(positionArray[lane, :])


def switch_lane(positionArray, i, lanes, vmax, right_change_condition, left_change_condition, speedArray, gap, left_change_real, right_change_real, switch_lane_prob, speedCounter, road, timeWaited):
    for j in range(positionArray.shape[1] - 1, -1, -1):
        change_force = False
        if positionArray[i, j] == 1 and i == road.congestion_point_lane and j < road.congestion_point_point and j + road.vmax > road.congestion_point_point:
            change_force = True
        if (timeWaited[i, j] != 0 and timeWaited[i, j] % (road.time_can_wait * 2) == 0) or change_force:
            '''计算换道条件begin'''
            if positionArray[i, j] == 1:
                if i == 1:
                    change = True
                    if positionArray[i + 1, j] == 1 or positionArray[i + 1, j] == 2:
                        change = False
                    right_change_condition[i, j] = change
                elif i == lanes:
                    change = True
                    if positionArray[i - 1, j] == 1 or positionArray[i - 1, j] == 2:
                        change = False
                    left_change_condition[i, j] = change
                elif 1 < i < lanes:
                    change_left = True
                    change_right = True
                    if positionArray[i - 1, j] == 1 or positionArray[i - 1, j] == 2:
                        change_left = False
                    if positionArray[i + 1, j] == 1 or positionArray[i + 1, j] == 2:
                        change_right = False
                    left_change_condition[i, j] = change_left
                    right_change_condition[i, j] = change_right
            '''计算换道条件end'''
            '''计算是否满足换道动机（即是否换道）begin'''
            if positionArray[i, j] == 1:
                if i == 1:
                    if (gap[i, j] == 0 and right_change_condition[i, j] == 1 and random.uniform(0, 1) < switch_lane_prob) or (change_force and right_change_condition[i, j] == 1):
                        right_change_real[i, j] = 1
                elif 1 < i < lanes:
                    if (gap[i, j] == 0 and right_change_condition[i, j] == 1 and random.uniform(0, 1) < switch_lane_prob) or (change_force and right_change_condition[i, j] == 1):
                        right_change_real[i, j] = 1
                    if (gap[i, j] == 0 and left_change_condition[i, j] == 1 and random.uniform(0, 1) < switch_lane_prob) or (change_force and left_change_condition[i, j] == 1):
                        left_change_real[i, j] = 1
                elif i == lanes:
                    if (gap[i, j] == 0 and left_change_condition[i, j] == 1 and random.uniform(0, 1) < switch_lane_prob) or (change_force and left_change_condition[i, j] == 1):
                        left_change_real[i, j] = 1
            '''计算是否满足换道动机（即是否换道）end'''
            '''进行换道begin'''
            if positionArray[i, j] == 1 and (left_change_real[i, j] == 1 or right_change_real[i, j] == 1):
                if i == 1:
                    if positionArray[i + 1, j] == 1:
                        print 'lane= %d' % i
                        print 'j= %d' % j
                        raise RuntimeError('switch error')
                    positionArray[i + 1, j] = 1
                    speedArray[i + 1, j] = speedArray[i, j]
                    speedCounter[i + 1, j] = speedCounter[i, j]
                    timeWaited[i + 1, j] = 0
                elif 1 < i < lanes and left_change_real[i, j] == 1 and random.uniform(0, 1) < road.switch_left_prob:
                    if left_change_real[i, j] == 1 and right_change_real[i, j] != 1:
                        if positionArray[i - 1, j] == 1:
                            print 'lane= %d' % i
                            print 'j= %d' % j
                            raise RuntimeError('switch error')
                        positionArray[i - 1, j] = 1
                        speedArray[i - 1, j] = speedArray[i, j]
                        speedCounter[i - 1, j] = speedCounter[i, j]
                        timeWaited[i - 1, j] = 0
                    if left_change_real[i, j] != 1 and right_change_real[i, j] == 1:
                        if positionArray[i + 1, j] == 1:
                            print 'lane= %d' % i
                            print 'j= %d' % j
                            raise RuntimeError('switch error')
                        positionArray[i + 1, j] = 1
                        speedArray[i + 1, j] = speedArray[i, j]
                        speedCounter[i + 1, j] = speedCounter[i, j]
                        timeWaited[i + 1, j] = 0
                    if left_change_real[i, j] == 1 and right_change_real[i, j] == 1 and random.uniform(0, 1) < road.switch_left_prob:
                        if positionArray[i - 1, j] == 1:
                            print 'lane= %d' % i
                            print 'j= %d' % j
                            raise RuntimeError('switch error')
                        positionArray[i - 1, j] = 1
                        speedArray[i - 1, j] = speedArray[i, j]
                        speedCounter[i - 1, j] = speedCounter[i, j]
                        timeWaited[i - 1, j] = 0
                    elif right_change_real[i, j] == 1 and left_change_real[i, j] == 1:
                        if positionArray[i + 1, j] == 1:
                            print 'lane= %d' % i
                            print 'j= %d' % j
                            raise RuntimeError('switch error')
                        positionArray[i + 1, j] = 1
                        speedArray[i + 1, j] = speedArray[i, j]
                        speedCounter[i + 1, j] = speedCounter[i, j]
                        timeWaited[i + 1, j] = 0
                elif i == lanes:
                    if positionArray[i - 1, j] == 1:
                        print 'lane= %d' % i
                        print 'j= %d' % j
                        raise RuntimeError('switch error')
                    positionArray[i - 1, j] = 1
                    speedArray[i - 1, j] = speedArray[i, j]
                    speedCounter[i - 1, j] = speedCounter[i, j]
                    timeWaited[i - 1, j] = 0
                positionArray[i, j] = 0
                speedArray[i, j] = 0
                speedCounter[i, j] = 0
                road.switch_counter += 1
                timeWaited[i, j] = 0
            elif positionArray[i, j] == 1 and j != 0 and (left_change_real[i, j] != 1 and right_change_real[i, j] != 1):
                timeWaited[i, j] += 1
            '''进行换道end'''
        else:
            '''计算换道条件begin'''
            if positionArray[i, j] == 1:
                if i == 1:
                    change = True
                    for r in range(j - vmax - 1, j + 1):
                        if positionArray[i + 1, r] == 1 or positionArray[i + 1, r] == 2:
                            change = False
                            break
                    right_change_condition[i, j] = change
                elif i == lanes:
                    change = True
                    for l in range(j - vmax - 1, j + 1):
                        if positionArray[i - 1, l] == 1 or positionArray[i - 1, l] == 2:
                            change = False
                            break
                    left_change_condition[i, j] = change
                elif 1 < i < lanes:
                    change_left = True
                    change_right = True
                    for l in range(j - vmax - 1, j + 1):
                        if positionArray[i - 1, l] == 1 or positionArray[i - 1, l] == 2:
                            change_left = False
                            break
                    for r in range(j - vmax - 1, j + 1):
                        if positionArray[i + 1, r] == 1 or positionArray[i + 1, r] == 2:
                            change_right = False
                            break
                    left_change_condition[i, j] = change_left
                    right_change_condition[i, j] = change_right
            '''计算换道条件end'''
            '''计算是否满足换道动机（即是否换道）begin'''
            if positionArray[i, j] == 1:
                if i == 1:
                    if min(speedArray[i, j] + 1, vmax) > gap[i, j] and right_change_condition[
                        i, j] == 1 and random.uniform(
                            0, 1) < switch_lane_prob:
                        right_change_real[i, j] = 1
                elif 1 < i < lanes:
                    if min(speedArray[i, j] + 1, vmax) > gap[i, j] and right_change_condition[
                        i, j] == 1 and random.uniform(
                            0, 1) < switch_lane_prob:
                        right_change_real[i, j] = 1
                    if min(speedArray[i, j] + 1, vmax) > gap[i, j] and left_change_condition[
                        i, j] == 1 and random.uniform(
                            0, 1) < switch_lane_prob:
                        left_change_real[i, j] = 1
                elif i == lanes:
                    if min(speedArray[i, j] + 1, vmax) > gap[i, j] and left_change_condition[
                        i, j] == 1 and random.uniform(
                            0, 1) < switch_lane_prob:
                        left_change_real[i, j] = 1
            '''计算是否满足换道动机（即是否换道）end'''
            '''进行换道begin'''
            if positionArray[i, j] == 1 and (left_change_real[i, j] == 1 or right_change_real[i, j] == 1):
                if i == 1:
                    if positionArray[i + 1, j] == 1:
                        print 'lane= %d' % i
                        print 'j= %d' % j
                        raise RuntimeError('switch error')
                    positionArray[i + 1, j] = 1
                    speedArray[i + 1, j] = speedArray[i, j]
                    speedCounter[i + 1, j] = speedCounter[i, j]
                    timeWaited[i + 1, j] = 0
                elif 1 < i < lanes:
                    if left_change_real[i, j] == 1 and right_change_real[i, j] != 1:
                        if positionArray[i - 1, j] == 1:
                            print 'lane= %d' % i
                            print 'j= %d' % j
                            raise RuntimeError('switch error')
                        positionArray[i - 1, j] = 1
                        speedArray[i - 1, j] = speedArray[i, j]
                        speedCounter[i - 1, j] = speedCounter[i, j]
                        timeWaited[i - 1, j] = 0
                    if right_change_real[i, j] == 1 and left_change_real[i, j] != 1:
                        if positionArray[i + 1, j] == 1:
                            print 'lane= %d' % i
                            print 'j= %d' % j
                            raise RuntimeError('switch error')
                        positionArray[i + 1, j] = 1
                        speedArray[i + 1, j] = speedArray[i, j]
                        speedCounter[i + 1, j] = speedCounter[i, j]
                        timeWaited[i + 1, j] = 0
                    if right_change_real[i, j] == 1 and left_change_real[i, j] == 1 and random.uniform(0, 1) < road.switch_left_prob:
                        if positionArray[i - 1, j] == 1:
                            print 'lane= %d' % i
                            print 'j= %d' % j
                            raise RuntimeError('switch error')
                        positionArray[i - 1, j] = 1
                        speedArray[i - 1, j] = speedArray[i, j]
                        speedCounter[i - 1, j] = speedCounter[i, j]
                        timeWaited[i - 1, j] = 0
                    elif right_change_real[i, j] == 1 and left_change_real[i, j] == 1:
                        if positionArray[i + 1, j] == 1:
                            print 'lane= %d' % i
                            print 'j= %d' % j
                            raise RuntimeError('switch error')
                        positionArray[i + 1, j] = 1
                        speedArray[i + 1, j] = speedArray[i, j]
                        speedCounter[i + 1, j] = speedCounter[i, j]
                        timeWaited[i + 1, j] = 0
                elif i == lanes:
                    if positionArray[i - 1, j] == 1:
                        print 'lane= %d' % i
                        print 'j= %d' % j
                        raise RuntimeError('switch error')
                    positionArray[i - 1, j] = 1
                    speedArray[i - 1, j] = speedArray[i, j]
                    speedCounter[i - 1, j] = speedCounter[i, j]
                    timeWaited[i - 1, j] = 0
                positionArray[i, j] = 0
                speedArray[i, j] = 0
                speedCounter[i, j] = 0
                road.switch_counter += 1
                timeWaited[i, j] = 0
            elif positionArray[i, j] == 1 and j != 0 and (left_change_real[i, j] != 1 and right_change_real[i, j] != 1):
                timeWaited[i, j] += 1
            '''进行换道end'''


