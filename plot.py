#coding:utf-8
#!/usr/bin/env python
import matplotlib.pyplot as plt
import road
import matplotlib as mpl
import car as car
import pandas as pd
import random
import csv
import time
import os
from multiprocessing import Process


def f_1(x, A, B):
    return A*x + B


def f_2(x, A, B, C):
    return A*x*x + B*x + C


def f_3(x, A, B, C, D):
    return A*x*x*x + B*x*x + C*x + D


def basic_figure():
    df = pd.read_csv('HD32_test.csv', encoding='utf-8').fillna(0)
    flow = df.loc[:, ['VEH_TOTAL']]
    speed = df.loc[:, ['AVG_SPEED']]
    flow.rename(columns={'VEH_TOTAL':'SUM'}, inplace=True)
    speed.rename(columns={'AVG_SPEED':'SUM'}, inplace=True)
    density = flow / speed
    xdata = flow['SUM']
    ydata = speed['SUM']
    xlist = xdata.values.tolist()
    ylist = ydata.values.tolist()
    xset = set(xlist)
    d = dict()
    # for s in xset:
    #     sum = 0
    #     count = 0
    #     for i in range(0, len(xlist)):
    #         if xlist[i] == s:
    #             sum += ylist[i]
    #             count += 1
    #     d[s] = sum/count
    # plt.plot(d.keys(), d.values(), '.')

    print speed
    plt.scatter(flow, speed, s=2)
    # plt.scatter(density, flow, linewidths=1)
    # plt.scatter(density, speed, linewidths=1)
    # '''拟合test'''
    # A1, B1, C1 = optimize.curve_fit(f_2, xdata, ydata)[0]
    # x1 = np.arange(0, 200, 1)
    # y1 = A1*x1*x1 + B1*x1 + C1
    # plt.plot(x1, y1)
    # '''拟合test'''
    plt.show()


def if_red(t, road):
    """计算当前是否为红灯"""
    temp = int(t % 20)
    if temp < road.red_time:
        # road.position_array[road.block_lane - 1, road.existPosition + 1] = 2
        road.position_array[road.block_lane, road.entrancePosition + 1] = 2
        road.is_red = True
        return True
    else:
        # road.position_array[road.block_lane - 1, road.existPosition + 1] = 3
        road.position_array[road.block_lane, road.entrancePosition + 1] = 3
        road.is_red = False
        return False


def check_something(road):
    pass
    # for i in range(1, road.lanes + 1):
    #     for j in range(1, road.length):
    #         if road.des_array[i, j] == 1:
    #             print("check false")


def road_visualization(road, time_interval, pause_time, cur_data):
    colors = ['white', 'blue', 'red', 'black']
    cmap = mpl.colors.ListedColormap(colors)
    temp_flow = 0
    temp_entrance_flow = 0
    temp_speed = 0
    flow_list = list()
    flow_list.append("流量：")
    entrance_flow_list = list()
    entrance_flow_list.append("入口匝道流量：")
    speed_list = list()
    speed_list.append("速度：")
    density_list = list()
    density_list.append("密度：")
    t_list = list()
    t_list.append("时间步：")
    """Turn interactive mode on."""
    plt.ion()
    for t in range(road.simulation_times):
        time_begin = time.time();
        """入口随机入车 begin"""
        for i in range(1, road.lanes + 1):
            if i == 5:
                continue
            carr = car.Car()
            if random.uniform(0, 1) < road.prob_in:
                # TODO 初始速度的随机分布
                car.Car.new_car(carr, road, 0, i)
        """入口随机入车 end"""
        if t % time_interval == 0:
            '''每t时间步展示数据'''
            interval_flow = road.count_flow - temp_flow
            temp_flow = road.count_flow

            interval_entrance_flow = road.count_entrance_flow - temp_entrance_flow
            temp_entrance_flow = road.count_entrance_flow

            interval_speed = road.travel_speed - temp_speed
            temp_speed = road.travel_speed
            interval_travel_speed = round(interval_speed / interval_flow, 2) if interval_flow != 0 else 0
            if interval_flow == 0 and interval_speed == 0:
                pass
            else:
                t_list.append(t / time_interval)
                speed_list.append(interval_travel_speed)
                entrance_flow_list.append(interval_entrance_flow)
                flow_list.append(interval_flow)
                density_list.append((round(interval_flow / interval_travel_speed, 2) if interval_travel_speed != 0 else 0))
            '''写入CSV'''
            out = open('data/data' + cur_data + '.csv', 'w')
            csv_write = csv.writer(out, dialect='excel')
            csv_write.writerow(t_list)
            csv_write.writerow(flow_list)
            csv_write.writerow(speed_list)
            csv_write.writerow(entrance_flow_list)
            csv_write.writerow(density_list)
            '''写入CSV'''
        plt.imshow(road.position_array, cmap=cmap)
        plt.axis('off')
        plt.pause(pause_time)
        if_red(t, road)
        road.sim()
        check_something(road)
        time_end = time.time()
        print "当前仿真" + cur_data + "的数据，当前时间步：" + str(t) + "，耗时：" + str(time_end - time_begin)
    plt.ioff()


if __name__ == '__main__':

    time_interval = 30
    pause_time = 0.01

    for i in range(15):
        if i % 2 == 0 and i >= 6:
            time_begin = time.time()
            road_instance = road.InterweaveRoad()
            road_instance.red_time = i
            cur_data = 'red-light-time' + str(i)
            p = Process(target=road_visualization(road_instance, time_interval, pause_time, cur_data), args=(cur_data,))
            p.start()
            p.join()
            time_end = time.time()
            print "仿真red-light-time=" + str(i) + "数据共耗时：" + str(round((time_end - time_begin) / 60)) + "min"

    # time_begin = time.time()
    # road = road.InterweaveRoad()
    # road_visualization(road, time_interval, pause_time, " no_control")
    # time_end = time.time()
    # print "仿真一组数据共需要：" + str(round((time_end - time_begin) / 60)) + "min"


