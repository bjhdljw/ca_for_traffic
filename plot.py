#!/usr/bin/env python
import matplotlib.pyplot as plt
import road
import matplotlib as mpl
import car

if __name__ == '__main__':
    colors = ['white', 'blue', 'black']
    cmap = mpl.colors.ListedColormap(colors)
    road = road.Road(80, 3)
    car = car.Car()
    car.new_car(road, 0, 1)

    plt.figure(figsize=(10, 12))
    plt.imshow(road.positionArray, cmap = cmap)
    plt.axis('off')
    plt.show()

