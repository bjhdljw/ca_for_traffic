# coding:utf-8
# !/usr/bin/env python
import random

WALL = 3


class SwitchRule(object):
    
    @staticmethod
    def switch_condition(i, j, road, right_change_condition, left_change_condition):
        if road.position_array[i, j] == 1:
            if int(road.switch_helper_array[i, j]) == 1 or int(road.switch_helper_array[i, j]) == 6:
                change = True
                temp_v_max = road.get_vmax(i + 1)
                if road.position_array[i + 1, j] == 2 or road.position_array[i + 1, j] == WALL:
                    change = False
                for r in range(j - int(temp_v_max) - 1, j + 1):
                    if road.position_array[i + 1, r] == 1:
                        change = False
                        break
                right_change_condition[i, j] = change
            elif road.switch_helper_array[i, j] == 4 or road.switch_helper_array[i, j] == 7:
                change = True
                temp_v_max = road.get_vmax(i - 1)
                if road.position_array[i - 1, j] == 2 or road.position_array[i - 1, j] == WALL:
                    change = False
                for l in range(j - temp_v_max - 1, j + 1):
                    if road.position_array[i - 1, l] == 1:
                        change = False
                        break
                left_change_condition[i, j] = change
            elif road.switch_helper_array[i, j] == 2 or road.switch_helper_array[i, j] == 3:
                change_left = True
                change_right = True
                temp_v_max_l = road.get_vmax(i - 1)
                temp_v_max_r = road.get_vmax(i + 1)
                if road.position_array[i - 1, j] == 2 or road.position_array[i - 1, j] == WALL:
                    change_left = False
                if road.position_array[i + 1, j] == 2 or road.position_array[i + 1, j] == WALL:
                    change_right = False
                for l in range(j - int(temp_v_max_l) - 1, j + 1):
                    if road.position_array[i - 1, l] == 1 or road.position_array[i - 1, l] == 2:
                        change_left = False
                        break
                for r in range(j - int(temp_v_max_r) - 1, j + 1):
                    if road.position_array[i + 1, r] == 1 or road.position_array[i + 1, r] == 2:
                        change_right = False
                        break
                left_change_condition[i, j] = change_left
                right_change_condition[i, j] = change_right

    @staticmethod
    def switch_purpose(i, j, road, gap, right_change_condition, right_change_real, left_change_condition,
                       left_change_real):
        if road.position_array[i, j] == 1:
            if int(road.switch_helper_array[i, j]) == 1 or int(road.switch_helper_array[i, j]) == 6:
                if min(road.speed_array[i, j] + 1, road.get_vmax(i)) > gap[i, j] and right_change_condition[i, j] == 1 \
                        and random.uniform(0, 1) < road.switch_lane_prob:
                    right_change_real[i, j] = 1
            elif int(road.switch_helper_array[i, j]) == 2 or int(road.switch_helper_array[i, j]) == 3:
                if min(road.speed_array[i, j] + 1, road.get_vmax(i)) > gap[i, j] and right_change_condition[i, j] == 1 \
                        and random.uniform(0, 1) < road.switch_lane_prob:
                    right_change_real[i, j] = 1
                if min(road.speed_array[i, j] + 1, road.get_vmax(i)) > gap[i, j] and left_change_condition[i, j] == 1 \
                        and random.uniform(0, 1) < road.switch_lane_prob:
                    left_change_real[i, j] = 1
            elif int(road.switch_helper_array[i, j]) == 4 or int(road.switch_helper_array[i, j]) == 7:
                if min(road.speed_array[i, j] + 1, road.get_vmax(i)) > gap[i, j] and left_change_condition[i, j] == 1 \
                        and random.uniform(0, 1) < road.switch_lane_prob:
                    left_change_real[i, j] = 1

    @staticmethod
    def switch(i, j, road, left_change_real, right_change_real):
        if road.position_array[i, j] == 1 and (left_change_real[i, j] == 1 or right_change_real[i, j] == 1):
            if int(road.switch_helper_array[i, j]) == 1 or int(road.switch_helper_array[i, j]) == 6:
                road.position_array[i + 1, j] = 1
                road.speed_array[i + 1, j] = road.speed_array[i, j]
                road.speed_counter[i + 1, j] = road.speed_counter[i, j]
                road.des_array[i + 1, j] = road.des_array[i, j]
            elif int(road.switch_helper_array[i, j]) == 2 or int(road.switch_helper_array[i, j]) == 3:
                if left_change_real[i, j] == 1 and right_change_real[i, j] != 1:
                    road.position_array[i - 1, j] = 1
                    road.speed_array[i - 1, j] = road.speed_array[i, j]
                    road.speed_counter[i - 1, j] = road.speed_counter[i, j]
                    road.des_array[i - 1, j] = road.des_array[i, j]
                if right_change_real[i, j] == 1 and left_change_real[i, j] != 1:
                    road.position_array[i + 1, j] = 1
                    road.speed_array[i + 1, j] = road.speed_array[i, j]
                    road.speed_counter[i + 1, j] = road.speed_counter[i, j]
                    road.des_array[i + 1, j] = road.des_array[i, j]
                if right_change_real[i, j] == 1 and left_change_real[i, j] == 1 and random.uniform(0, 1) < road.switch_left_prob:
                    road.position_array[i - 1, j] = 1
                    road.speed_array[i - 1, j] = road.speed_array[i, j]
                    road.speed_counter[i - 1, j] = road.speed_counter[i, j]
                    road.des_array[i - 1, j] = road.des_array[i, j]
                elif right_change_real[i, j] == 1 and left_change_real[i, j] == 1:
                    road.position_array[i + 1, j] = 1
                    road.speed_array[i + 1, j] = road.speed_array[i, j]
                    road.speed_counter[i + 1, j] = road.speed_counter[i, j]
                    road.des_array[i + 1, j] = road.des_array[i, j]
            elif int(road.switch_helper_array[i, j]) == 4 or int(road.switch_helper_array[i, j]) == 7:
                road.position_array[i - 1, j] = 1
                road.speed_array[i - 1, j] = road.speed_array[i, j]
                road.speed_counter[i - 1, j] = road.speed_counter[i, j]
                road.des_array[i - 1, j] = road.des_array[i, j]
            road.position_array[i, j] = 0
            road.speed_array[i, j] = 0
            road.speed_counter[i, j] = 0
            road.des_array[i, j] = 0
            road.switch_counter += 1


class NearExistSwitchRule(SwitchRule):
    """
    临近快速路出口，但是无法驶离快速路的路段，只需要des_array[i, j] == 2的车辆在快速路1、2、3车道的换道情况，其他情况和基础换
    道条件相同；
    """

    @staticmethod
    def switch_condition(i, j, road, right_change_condition, left_change_condition):
        """des_array[i, j] == 2的车辆换道条件单独处理，其余车辆换道条件和基础换道条件相同"""
        if road.position_array[i, j] == 1:
            if road.des_array[i, j] == 2:
                if i == road.block_lane - 1 \
                        and road.position_array[i + 1, j] == 0 \
                        and not road.is_red:
                    right_change_condition[i, j] = True
                if int(road.switch_helper_array[i, j]) == 1 \
                        or int(road.switch_helper_array[i, j]) == 2 \
                        or int(road.switch_helper_array[i, j]) == 3:
                    change = True
                    if road.position_array[i + 1, j] == 1 or road.position_array[i + 1, j] == 2 or road.position_array[i + 1, j] == 3:
                        change = False
                    right_change_condition[i, j] = change
            else:
                SwitchRule.switch_condition(i, j, road, right_change_condition, left_change_condition)

    @staticmethod
    def switch_purpose(i, j, road, gap, right_change_condition, right_change_real, left_change_condition,
                       left_change_real):
        """des_array[i, j] == 2的车辆换道动机单独处理，其余车辆换道条件和基础换道条件相同"""
        if road.position_array[i, j] == 1:
            if road.des_array[i, j] == 2:
                if i == road.block_lane - 1 and road.position_array[i + 1, j] == 0 and right_change_condition[i, j] == 1:
                    right_change_real[i, j] = 1
                if (int(road.switch_helper_array[i, j]) == 1 or int(road.switch_helper_array[i, j]) == 2 or int(road.switch_helper_array[i, j]) == 3) \
                        and right_change_condition[i, j]:
                    right_change_real[i, j] = 1
            else:
                SwitchRule.switch_purpose(i, j, road, gap, right_change_condition, right_change_real,
                                          left_change_condition, left_change_real)

    @staticmethod
    def switch(i, j, road, left_change_real, right_change_real):
        if i == road.block_lane - 1 \
                and road.position_array[i, j] == 1 \
                and road.des_array[i, j] == 2 \
                and road.position_array[i + 1, j] == 0 \
                and right_change_real[i, j] == 1:
            road.position_array[i + 1, j] = 1
            road.speed_array[i + 1, j] = road.speed_array[i, j]
            road.speed_counter[i + 1, j] = road.speed_counter[i, j]
            road.des_array[i + 1, j] = road.des_array[i, j]
            road.position_array[i, j] = 0
            road.speed_array[i, j] = 0
            road.speed_counter[i, j] = 0
            road.des_array[i, j] = 0
            road.switch_counter += 1
        else:
            SwitchRule.switch(i, j, road, left_change_real, right_change_real)


class InterweaveSwitchRule(SwitchRule):

    @staticmethod
    def switch_condition(i, j, road, right_change_condition, left_change_condition):
        """des_array[i, j] == 2的车辆换道条件单独处理，其余车辆换道条件和基础换道条件相同"""
        if road.position_array[i, j] == 1:
            if road.des_array[i, j] == 4:
                if i == road.block_lane \
                        and road.position_array[i - 1, j] == 0 \
                        and road.position_array[i - 2, j] == 0 \
                        and not road.is_red:
                    left_change_condition[i, j] = True
                if int(road.switch_helper_array[i, j]) == 6 \
                        or int(road.switch_helper_array[i, j]) == 7:
                    change = True
                    if road.position_array[i - 1, j] == 1 or road.position_array[i - 1, j] == 2 or road.position_array[
                                i - 1, j] == 3:
                        change = False
                    left_change_condition[i, j] = change
            else:
                SwitchRule.switch_condition(i, j, road, right_change_condition, left_change_condition)

    @staticmethod
    def switch_purpose(i, j, road, gap, right_change_condition, right_change_real, left_change_condition,
                       left_change_real):
        """des_array[i, j] == 2的车辆换道动机单独处理，其余车辆换道条件和基础换道条件相同"""
        if road.position_array[i, j] == 1:
            if road.des_array[i, j] == 4:
                if i == road.block_lane and road.position_array[i - 1, j] == 0 and left_change_condition[i, j] == 1:
                    left_change_real[i, j] = 1
                if (int(road.switch_helper_array[i, j]) == 6 or int(road.switch_helper_array[i, j]) == 7) \
                        and left_change_condition[i, j]:
                    left_change_real[i, j] = 1
            else:
                SwitchRule.switch_purpose(i, j, road, gap, right_change_condition, right_change_real,
                                          left_change_condition, left_change_real)

    @staticmethod
    def switch(i, j, road, left_change_real, right_change_real):
        if road.position_array[i, j] == 1 \
                and road.des_array[i, j] == 4 \
                and left_change_real[i, j] == 1:
            road.position_array[i - 1, j] = 1
            road.speed_array[i - 1, j] = road.speed_array[i, j]
            road.speed_counter[i - 1, j] = road.speed_counter[i, j]
            road.des_array[i - 1, j] = road.des_array[i, j]
            road.position_array[i, j] = 0
            road.speed_array[i, j] = 0
            road.speed_counter[i, j] = 0
            road.des_array[i, j] = 0
            road.switch_counter += 1
        elif i == road.block_lane \
                and road.position_array[i, j] == 1 \
                and road.des_array[i, j] == 4 \
                and road.position_array[i - 1, j] == 0 \
                and left_change_real[i, j] == 1:
            road.position_array[i - 2, j] = 1
            road.speed_array[i - 2, j] = road.speed_array[i, j]
            road.speed_counter[i - 2, j] = road.speed_counter[i, j]
            road.des_array[i - 2, j] = road.des_array[i, j]
            road.position_array[i, j] = 0
            road.speed_array[i, j] = 0
            road.speed_counter[i, j] = 0
            road.des_array[i, j] = 0
            road.switch_counter += 1
        else:
            SwitchRule.switch(i, j, road, left_change_real, right_change_real)

