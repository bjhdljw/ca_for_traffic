#coding:utf-8
#!/usr/bin/env python
import matplotlib.pyplot as plt
import road
import matplotlib as mpl
import car as car
import pandas as pd
import random


def basic_figure():
    df = pd.read_csv('HD32_test.csv', encoding='utf-8').fillna(0)
    flow = df.loc[:, ['VEH_TOTAL']]
    speed = df.loc[:, ['AVG_SPEED']]
    flow.rename(columns={'VEH_TOTAL':'SUM'}, inplace=True)
    speed.rename(columns={'AVG_SPEED':'SUM'}, inplace=True)
    density = flow / speed
    plt.scatter(flow, speed, linewidths=1)
    # plt.scatter(density, flow, linewidths=1)
    # plt.scatter(density, speed, linewidths=1)
    plt.show()


def space_time():
    df = pd.read_csv('space_time.csv', encoding='utf-8').fillna(0)
    plt.scatter()
    print df


def road_visualization_dynamic(road):

    colors = ['white', 'blue', 'black']
    cmap = mpl.colors.ListedColormap(colors)

    plt.ion()
    for t in range(simulation_times):
        for i in range(1, road.lanes + 1):
            carr = car.Car()
            if random.uniform(0, 1) < road.prob_in:
                # TODO 初始速度的随机分布
                car.Car.new_car(carr, road, 0, i)
        '''可视化界面布局begin'''
        fig = plt.figure()
        ax1 = fig.add_subplot(311)
        ax2 = fig.add_subplot(334)
        ax3 = fig.add_subplot(335)
        ax4 = fig.add_subplot(336)
        ax2.axis('off')
        ax3.axis('off')
        ax4.axis('off')
        '''可视化界面布局end'''
        '''每一时间步一展示数据begin'''
        str_t = 'timestamp= %d' % t
        str_limit_begin = 'limit begin= %d' % (road.limit_begin + 1)
        str_limit_end = 'limit end= %d' % (road.limit_end + 1)
        str_travel_time = 'travel time=%.2f s' % (road.travel_time/road.count_flow if road.count_flow != 0 else 0)
        travel_speed = (road.travel_speed/road.count_flow if road.count_flow != 0 else 0)
        str_travel_speed = 'travel speed=%.2f cells/s' % travel_speed
        str_flow = 'traffic flow= %d' % road.count_flow
        str_density = 'traffic density= %.2f' % (road.count_flow/travel_speed if travel_speed != 0 else 0)
        ax2.text(0, 0, str_t)
        ax2.text(0, 0.2, str_flow)
        ax2.text(0, 0.4, str_limit_begin)
        ax2.text(0, 0.6, str_limit_end)
        ax2.text(0, 0.8, str_travel_time)
        ax2.text(0, 1, str_travel_speed)
        ax2.text(0, 1.2, str_density)
        '''每一时间步一展示数据end'''
        ax1.imshow(road.positionArray, cmap=cmap)
        ax1.axis('off')
        plt.pause(0.2)
        road.progress(road.vmax)
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
    pro_in = 0.2
    islimit = False
    limit_begin = 10
    limit_end = 20
    lane_for_st_figure = 3

    road = road.Road(road_length, lanes, vmax, pro_in, True, 0, road_length - 1, lane_for_st_figure)
    road_visualization_dynamic(road)

    # '''test'''
    # space_time()
    # '''test'''


