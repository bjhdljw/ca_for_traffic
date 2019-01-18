#!/usr/bin/env python
import matplotlib.pyplot as plt
import road
import matplotlib as mpl
import car
import pandas as pd

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

def road_visualization(road):

    colors = ['white', 'blue', 'black']
    cmap = mpl.colors.ListedColormap(colors)

    plt.figure(figsize=(10, 12))
    plt.imshow(road.positionArray, cmap=cmap)
    plt.axis('off')
    plt.show()

if __name__ == '__main__':

    # road = road.Road(80, 3)
    # car = car.Car()
    # car.new_car(road, 0, 1)
    # road_visualization(road)

    basic_figure()

