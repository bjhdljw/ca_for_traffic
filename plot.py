#coding:utf-8
#!/usr/bin/env python
import matplotlib.pyplot as plt
import road
import matplotlib as mpl
import car as car
import pandas as pd
import random
import csv

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

    '''list to storage'''
    flow_store = list()
    speed_store = list()
    '''list to storage'''

    '''list for basic_figure'''
    flow_list = list()
    speed_list = list()
    density_list = list()
    '''list for basic_figure'''

    plt.ion()
    '''可视化界面布局begin'''
    time_space_count = 0
    '''可视化界面布局end'''
    for t in range(road.simulation_times):
        """入口随机入车 begin"""
        for i in range(1, road.lanes + 1):
            carr = car.Car()
            if random.uniform(0, 1) < road.prob_in:
                # TODO 初始速度的随机分布
                car.Car.new_car(carr, road, 0, i)
        """入口随机入车 end"""
        '''每一时间步一展示数据begin'''
        '''每一时间步一展示数据end'''
        '''每t时间步展示数据begin'''
        if t % time_interval == 0:
            # 计算当前时间周期内各项数据
            # 流量
            interval_flow = road.count_flow - temp_flow
            temp_flow = road.count_flow
            # 速度
            interval_speed = road.travel_speed - temp_speed
            temp_speed = road.travel_speed
            interval_travel_time = road.travel_time - temp_travel_time
            temp_travel_time = road.travel_time
            interval_travel_speed = interval_speed / interval_flow if interval_flow != 0 else 0
            # 时空图
            # time_space_y = list()
            # time_space_x = list()
            if interval_flow == 0 and interval_speed == 0:
                pass
            else:
                # time_space_temp = road.positionArray[road.lane_for_st_figure, road.limit_begin : road.limit_end]
                # .tolist()
                # for i in range(0, len(time_space_temp)):
                #     if time_space_temp[i] == 0:
                #         time_space_y.append(time_space_temp[i] + time_space_count)
                #         time_space_x.append(i)
                speed_list.append(interval_speed)
                flow_list.append(interval_flow)
                # TODO 密度直接这么算出来可以吗？
                density_list.append((interval_flow / interval_travel_speed if interval_travel_speed != 0 else 0))
                # time_space_count += 1
            '''写入CSV'''
            out = open('speed-flow-storage.csv', 'w')
            csv_write = csv.writer(out, dialect='excel')
            csv_write.writerow(speed_list)
            csv_write.writerow(flow_list)
            '''写入CSV'''
        '''每t时间步展示数据end'''
        str_interval_flow = 'interval flow= %d' % interval_flow
        interval_travel_speed = interval_speed / interval_flow if interval_flow != 0 else 0
        str_interval_traval_speed = 'interval travel speed= %.2f' % interval_travel_speed
        str_interval_density = 'interval density= %.2f' % (interval_flow/interval_travel_speed if interval_travel_speed != 0 else 0)
        str_interval_travel_time = 'interval travel time= %.2f' % (interval_travel_time/interval_flow if interval_flow != 0 else 0)
        plt.imshow(road.positionArray, cmap=cmap)
        plt.axis('off')
        plt.pause(pause_time)
        road.progress(road.limit_speed)
    plt.ioff()

if __name__ == '__main__':

    colors = ['white', 'blue', 'black']
    cmap = mpl.colors.ListedColormap(colors)

    time_interval = 10
    pause_time = 1

    road = road.Road()
    road_visualization_dynamic(road, time_interval, pause_time)


