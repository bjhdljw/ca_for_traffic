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


def road_visualization_dynamic(road):

    colors = ['white', 'blue', 'black']
    cmap = mpl.colors.ListedColormap(colors)

    plt.ion()
    for _ in range(simulation_times):
        for i in range(1, road.lanes + 1):
            carr = car.Car()
            if random.uniform(0, 1) < road.prob_in:
                # TODO 初始速度的随机分布
                car.Car.new_car(carr, road, 0, i)
        plt.imshow(road.positionArray, cmap=cmap)
        plt.axis('off')
        plt.pause(0.2)
        road.progress()
    plt.ioff()

if __name__ == '__main__':

    colors = ['white', 'blue', 'black']
    cmap = mpl.colors.ListedColormap(colors)

    simulation_times = 1000
    lanes = 3
    road_length = 50
    new_car_speed = 0
    new_car_position = 1
    vmax = 5
    pro_in = 0.2

    road = road.Road(road_length, lanes, vmax, pro_in)
    road_visualization_dynamic(road)


