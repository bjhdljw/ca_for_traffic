# coding:utf-8
# !/usr/bin/env python
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import csv


def general_flow_figure():
    csv_file = open('data/flow.csv')
    lines = csv.reader(csv_file)
    t = list()
    flow_no = list()
    flow_6_en = list()
    flow_4_en = list()
    i = 0
    for row in lines:
        if i == 0:
            t.append(row)
        elif i == 1:
            flow_no.append(row)
        elif i == 4:
            flow_6_en.append(row)
        elif i == 3:
            flow_4_en.append(row)
        i += 1
    t = t[0]
    flow_no = flow_no[0]
    flow_6_en = flow_6_en[0]
    flow_4_en = flow_4_en[0]
    del(t[0])
    del(flow_no[0])
    del(flow_6_en[0])
    del(flow_4_en[0])
    t = map(int, t)
    flow_no = map(int, flow_no)
    flow_6_en = map(float, flow_6_en)
    flow_4_en = map(float, flow_4_en)
    plt.ylabel('flow(veh/30s)')
    plt.xlabel('time(30s)')
    plt.plot(t, flow_no, label='no control')
    plt.plot(t, flow_4_en, label='entrance only 4s')
    plt.plot(t, flow_6_en, label='entrance only 6s')
    plt.legend()
    plt.savefig('pic/flow-time.png')
    plt.show()


def general_speed_figure():
    csv_file = open('data/speed.csv')
    lines = csv.reader(csv_file)
    t = list()
    speed_no = list()
    speed_6_en = list()
    speed_4_only = list()
    i = 0
    for row in lines:
        if i == 0:
            t.append(row)
        elif i == 1:
            speed_no.append(row)
        elif i == 4:
            speed_6_en.append(row)
        elif i == 3:
            speed_4_only.append(row)
        i += 1
    t = t[0]
    speed_no = speed_no[0]
    speed_6_en = speed_6_en[0]
    speed_4_only = speed_4_only[0]
    del(t[0])
    del(speed_no[0])
    del(speed_6_en[0])
    del(speed_4_only[0])
    t = map(int, t)
    speed_no = map(float, speed_no)
    speed_6_en = map(float, speed_6_en)
    speed_4_only = map(float, speed_4_only)
    plt.ylabel('speed(km/h)')
    plt.xlabel('time(30s)')
    plt.plot(t, speed_no, label='no control')
    plt.plot(t, speed_4_only, label='entrance only 4s')
    plt.plot(t, speed_6_en, label='entrance only 6s')
    plt.legend()
    plt.savefig('pic/speed-time.png')
    plt.show()


def general_density_figure():
    csv_file = open('data/density.csv')
    lines = csv.reader(csv_file)
    t = list()
    density_no = list()
    density_6_only = list()
    density_4_only = list()
    i = 0
    for row in lines:
        if i == 0:
            t.append(row)
        elif i == 1:
            density_no.append(row)
        elif i == 4:
            density_6_only.append(row)
        elif i == 3:
            density_4_only.append(row)
        i += 1
    t = t[0]
    density_no = density_no[0]
    density_6_only = density_6_only[0]
    density_4_only = density_4_only[0]
    del(t[0])
    del(density_no[0])
    del(density_6_only[0])
    del(density_4_only[0])
    t = map(int, t)
    density_no = map(float, density_no)
    density_6_only = map(float, density_6_only)
    density_4_only = map(float, density_4_only)
    # plt.ylabel()
    plt.xlabel('time(30s)')
    plt.plot(t, density_no, label='no control')
    plt.plot(t, density_4_only, label='entrance only 4s')
    plt.plot(t, density_6_only, label='entrance only 6s')
    plt.legend()
    plt.savefig('pic/density-time.png')
    plt.show()


def day_flow_figure(monitor_point, date):
    df = pd.read_csv('TAB_VEH_15MIN_ADDBLACK.csv', encoding='utf-8').fillna(0)
    flow = list()
    speed = list()
    date_list = list()
    for index, row in df.iterrows():
        if row['SBBH'] == monitor_point and row['JCSJ'].startswith(date):
            flow.append(row['VEH_TOTAL'])
            speed.append(row['AVG_SPEED'])
            date_list.append(row['JCSJ'])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    d = '2016-3-4 00:00'
    x = pd.date_range(d, periods=96, freq='15min')
    ax.plot(x, flow, label='True Data')
    date_format = mpl.dates.DateFormatter("%H:%M")
    ax.xaxis.set_major_formatter(date_format)
    fig.autofmt_xdate()
    plt.xlabel('Time of Day')
    plt.ylabel('Flow')

    plt.show()


def search_data(monitor_point, date):
    df = pd.read_csv('TAB_VEH_15MIN_ADDBLACK.csv', encoding='utf-8').fillna(0)
    flow = list()
    for index, row in df.iterrows():
        if row['SBBH'] == monitor_point and row['JCSJ'].startswith(date):
            flow.append(row['VEH_TOTAL'])
    if len(flow) == 96:
        print date


def read_chunk():
    df = pd.read_csv('TT_VEHICLE_T.csv', encoding='utf-8', chunksize=1)
    chunk = df.get_chunk(1)
    print chunk


if __name__ == '__main__':
    general_flow_figure()
    general_speed_figure()
    general_density_figure()



