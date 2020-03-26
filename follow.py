# coding:utf-8
# !/usr/bin/env python
import sys
import numpy as np
import random

WALL = 3
PROB_SLOW = 0.1


class FollowRule(object):
    """基础跟驰模型"""

    def __init__(self):
        # 每个时间步后更新
        self.count = 1
        self.gap_position_temp2 = sys.maxint
        self.got_exist_first_car = False

    def update_variable(self):
        self.count = 1
        self.gap_position_temp2 = sys.maxint
        self.got_exist_first_car = False

    @staticmethod
    def accelerate_step(road):
        """执行加速步"""
        """从道路最前面的一辆车开始遍历"""
        for i in range(1, road.position_array.shape[0] - 1):
            for j in range(road.position_array.shape[1] - 1, -1, -1):
                v_max_cur_lane = road.get_vmax(i)
                '''加速步骤begin'''
                road.speed_array[i, j] = min(road.speed_array[i, j] + 1, v_max_cur_lane)
                '''加速步骤end'''

    @staticmethod
    def compute_gap(road):
        gap = np.zeros(road.position_array.shape)
        for i in range(1, road.lanes + 1):
            gap_position_temp = sys.maxint
            for j in range(road.position_array.shape[1] - 1, -1, -1):
                if road.position_array[i, j] == 1 or road.position_array[i, j] == 2 or road.position_array[i, j] == WALL:
                    gap[i, j] = gap_position_temp - j - 1
                    gap_position_temp = j
        return gap

    @staticmethod
    def slow_down_step(i, j, gap, road, self):
        """减速步begin"""
        if road.position_array[i, j] == 1 or road.position_array[i, j] == 2 or road.position_array[i, j] == WALL:
            if road.position_array[i, j] == 2:
                pass
            if road.position_array[i, j] == WALL:
                pass
            # 第一、二辆车待用NaSch模型减速
            elif self.count == 1 or self.count == 2:
                temp_speed = min(road.speed_array[i, j], gap[i, j])
                road.speed_array[i, j] = max(temp_speed, 0)
            # 如果前方不是车辆，而是障碍物的话，不需要考虑前车速度，使用NaSch模型减速步
            elif self.gap_position_temp2 < road.position_array.shape[1] \
                    and (road.position_array[i, self.gap_position_temp2] == 2
                         or road.position_array[i, self.gap_position_temp2] == WALL):
                temp_speed = min(road.speed_array[i, j], gap[i, j])
                road.speed_array[i, j] = max(temp_speed, 0)
            # 如果前方是车辆的话，为了更快行进，会考虑前车速度，使用VE减速步
            else:
                d = max(0, gap[i, self.gap_position_temp2] - 1)
                v_max_before = road.limit_speed if (
                    road.is_limit and road.limit_begin <= self.gap_position_temp2 <= road.limit_end) else road.get_vmax(i)
                vq = min(v_max_before - 1, d)
                vq = min(vq, road.speed_array[i, self.gap_position_temp2])
                road.speed_array[i, j] = min(road.speed_array[i, j], gap[i, j] + vq)
            self.count += 1
            self.gap_position_temp2 = j
        '''减速步end'''

    @staticmethod
    def random_slow_down(road):
        for i in range(1, road.lanes + 1):
            for j in range(road.position_array.shape[1] - 1, -1, -1):
                if road.position_array[i, j] == 1 and random.uniform(0, 1) <= PROB_SLOW:
                    road.speed_array[i, j] = max(road.speed_array[i, j] - 1, 0)

    @staticmethod
    def update_position(road):
        for i in range(1, road.lanes + 1):
            for j in range(road.position_array.shape[1] - 1, -1, -1):
                if road.position_array[i, j] == 1:
                    position_next = int(j + road.speed_array[i, j])
                    if position_next != j:
                        # '''流量&总行程时间&总行程车速统计begin'''
                        # '''限速区末端为计数点'''
                        # if j <= road.limit_end <= position_next:
                        #     road.count_flow += 1
                        #     road.travel_time += road.speed_counter[i, j]
                        #     road.travel_speed += (road.limit_end - road.limit_begin) / road.speed_counter[i, j]
                        # '''流量&总行程时间&总行程车速统计end'''
                        if position_next < road.position_array.shape[1]:
                            road.position_array[i, position_next] = 1
                            road.speed_array[i, position_next] = road.speed_array[i, j]
                            road.speed_counter[i, position_next] = road.speed_counter[i, j]
                            road.des_array[i, position_next] = road.des_array[i, j]
                        road.position_array[i, j] = 0
                        road.speed_array[i, j] = 0
                        road.speed_counter[i, j] = 0
                        road.des_array[i, j] = 0


class ExistFollowRule(FollowRule):

    @staticmethod
    def slow_down_step(i, j, gap, road, self):
        """快速路出口前，快速路上欲驶离快速车辆的减速规则"""
        # 计数器，第1辆车和第2辆车减速步特殊处理：第1辆车不需要减速
        '''减速步begin'''
        if road.position_array[i, j] == 1 or road.position_array[i, j] == 2 or road.position_array[i, j] == WALL:
            if not self.got_exist_first_car and j == road.existPosition and road.des_array[i, j] == 2:
                suppose_next_position = int(road.speed_array[i, j] + j)
                if road.is_red and suppose_next_position > road.existPosition:
                    temp_speed = min(road.speed_array[i, j], road.existPosition - j)
                    road.speed_array[i, j] = max(temp_speed, 0)
                self.got_exist_first_car = True
            if not self.got_exist_first_car and j == road.existPosition - 1 and road.des_array[i, j] == 2:
                suppose_next_position = int(road.speed_array[i, j] + j)
                if road.is_red and suppose_next_position > road.existPosition:
                    temp_speed = min(road.speed_array[i, j], road.existPosition - j)
                    road.speed_array[i, j] = max(temp_speed, 0)
                self.got_exist_first_car = True
            if not self.got_exist_first_car and j == road.existPosition - 2 and road.des_array[i, j] == 2:
                suppose_next_position = int(road.speed_array[i, j] + j)
                if road.is_red and suppose_next_position > road.existPosition:
                    temp_speed = min(road.speed_array[i, j], road.existPosition - j)
                    road.speed_array[i, j] = max(temp_speed, 0)
                self.got_exist_first_car = True
            if road.position_array[i, j] == 2:
                pass
            if road.position_array[i, j] == WALL:
                pass
            elif self.count == 1 or self.count == 2:
                temp_speed = min(road.speed_array[i, j], gap[i, j])
                road.speed_array[i, j] = max(temp_speed, 0)
            # 如果前方不是车辆，而是障碍物的话，不需要考虑前车速度，使用NaSch模型减速步
            elif self.gap_position_temp2 < road.position_array.shape[1] \
                    and (road.position_array[i, self.gap_position_temp2] == 2
                         or road.position_array[i, self.gap_position_temp2] == WALL):
                temp_speed = min(road.speed_array[i, j], gap[i, j])
                road.speed_array[i, j] = max(temp_speed, 0)
            # 如果前方是车辆的话，为了更快行进，会考虑前车速度，使用VE减速步
            else:
                d = max(0, gap[i, self.gap_position_temp2] - 1)
                v_max_before = road.limit_speed if (
                        road.is_limit and road.limit_begin <= self.gap_position_temp2 <= road.limit_end) else road.vmax
                vq = min(v_max_before - 1, d)
                vq = min(vq, road.speed_array[i, self.gap_position_temp2])
                road.speed_array[i, j] = min(road.speed_array[i, j], gap[i, j] + vq)
            self.count += 1
            self.gap_position_temp2 = j
        '''减速步end'''