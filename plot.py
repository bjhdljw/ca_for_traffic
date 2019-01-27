#coding:utf-8
#!/usr/bin/env python
import matplotlib.pyplot as plt
import road
import matplotlib as mpl
import car as car
import pandas as pd
import random
from scipy import optimize
import numpy as np

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
    plt.scatter(flow, speed, linewidths=1)
    # plt.scatter(density, flow, linewidths=1)
    # plt.scatter(density, speed, linewidths=1)
    '''拟合test'''
    A1, B1, C1 = optimize.curve_fit(f_2, xdata, ydata)[0]
    x1 = np.arange(0, 200, 1)
    y1 = A1*x1*x1 + B1*x1 + C1
    plt.plot(x1, y1)
    '''拟合test'''
    plt.show()


def space_time():
    df = pd.read_csv('space_time.csv', encoding='utf-8').fillna(0)
    plt.scatter()
    print df


def road_visualization_dynamic(road, time_interval, pause_time):

    colors = ['white', 'blue', 'red', 'black']
    cmap = mpl.colors.ListedColormap(colors)

    temp_flow = 0
    temp_speed = 0
    temp_travel_time = 0

    plt.ion()
    fig = plt.figure()
    '''可视化界面布局begin'''
    ax1 = fig.add_subplot(311)
    ax2 = fig.add_subplot(334)
    ax3 = fig.add_subplot(335)
    ax4 = fig.add_subplot(336)
    ax2.axis('off')
    ax3.axis('off')
    ax4.axis('off')
    '''可视化界面布局end'''
    for t in range(simulation_times):
        for i in range(1, road.lanes + 1):
            carr = car.Car()
            if random.uniform(0, 1) < road.prob_in:
                # TODO 初始速度的随机分布
                car.Car.new_car(carr, road, 0, i)
        '''每一时间步一展示数据begin'''
        str_t = 'timestamp= %d' % t
        str_limit_begin = 'limit begin= %d' % (road.limit_begin + 1)
        str_limit_end = 'limit end= %d' % (road.limit_end + 1)
        str_travel_time = 'travel time=%.2f s' % (road.travel_time/road.count_flow if road.count_flow != 0 else 0)
        travel_speed = (road.travel_speed/road.count_flow if road.count_flow != 0 else 0)
        str_travel_speed = 'travel speed=%.2f cells/s' % travel_speed
        str_flow = 'traffic flow= %d' % road.count_flow
        str_density = 'traffic density= %.2f' % (road.count_flow/travel_speed if travel_speed != 0 else 0)
        str_switch_counter = 'switch_times= % d' % road.switch_counter
        ax2.text(0, 0, str_t)
        ax2.text(0, 0.2, str_flow)
        ax2.text(0, 0.4, str_limit_begin)
        ax2.text(0, 0.6, str_limit_end)
        ax2.text(0, 0.8, str_travel_time)
        ax2.text(0, 1, str_travel_speed)
        ax2.text(0, 1.2, str_density)
        ax2.text(0, 1.4, str_switch_counter)
        '''每一时间步一展示数据end'''
        '''每t时间步展示数据begin'''
        if t % time_interval == 0:
            interval_flow = road.count_flow - temp_flow
            temp_flow = road.count_flow
            interval_speed = road.travel_speed - temp_speed
            temp_speed = road.travel_speed
            interval_travel_time = road.travel_time - temp_travel_time
            temp_travel_time = road.travel_time
        '''每t时间步展示数据end'''
        str_interval_flow = 'interval flow= %d' % interval_flow
        interval_travel_speed = interval_speed / interval_flow if interval_flow != 0 else 0
        str_interval_traval_speed = 'interval travel speed= %.2f' % interval_travel_speed
        str_interval_density = 'interval density= %.2f' % (interval_flow/interval_travel_speed if interval_travel_speed != 0 else 0)
        str_interval_travel_time = 'interval travel time= %.2f' % (interval_travel_time/interval_flow if interval_flow != 0 else 0)
        ax2.text(0, -0.2, str_interval_flow)
        ax2.text(0, -0.4, str_interval_traval_speed)
        ax2.text(0, -0.6, str_interval_density)
        ax2.text(0, -0.8, str_interval_travel_time)
        ax1.imshow(road.positionArray, cmap=cmap)
        ax1.axis('off')
        plt.pause(pause_time)
        ax2.clear()
        ax2.axis('off')
        road.progress(road.limit_speed)
    plt.ioff()

if __name__ == '__main__':

    colors = ['white', 'blue', 'black']
    cmap = mpl.colors.ListedColormap(colors)

    simulation_times = 1000
    lanes = 3
    road_length = 80
    new_car_speed = 0
    new_car_position = 1
    vmax = 5
    limit_speed = 1
    pro_in = 0.6
    islimit = False
    limit_begin = 50
    limit_end = 60
    lane_for_st_figure = 3
    time_interval = 10
    switch_lane_prob = 1
    pause_time = 1
    congestion_point_lane = 3
    congestion_point_point = 50

    road = road.Road(road_length, lanes, vmax, pro_in, True, limit_begin, limit_end, lane_for_st_figure, switch_lane_prob, limit_speed, congestion_point_lane, congestion_point_point)
    road_visualization_dynamic(road, time_interval, pause_time)

    '''test'''
    '''test'''


