# coding:utf-8
# !/usr/bin/env python


class Counter(object):

    @staticmethod
    def increase_time_counter(road):
        """更新快速路出口至入口下游区间内车辆的行程时间"""
        for i in range(1, 8):
            for j in range(road.entrancePosition + 1, road.existPosition, -1):
                if road.position_array[i, j] == 1:
                    road.speed_counter[i, j] += 1

