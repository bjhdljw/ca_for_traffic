#coding:utf-8
#!/usr/bin/env python
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl


def general_figure(monitor_point, date):
    df = pd.read_csv('TAB_VEH_15MIN_ADDBLACK.csv', encoding='utf-8').fillna(0)
    flow = list()
    speed = list()
    date_list = list()
    for index, row in df.iterrows():
        if row['SBBH'] == monitor_point and row['JCSJ'].startswith(date):
            flow.append(row['VEH_TOTAL'])
            speed.append(row['AVG_SPEED'])
            date_list.append(row['JCSJ'])
    date_list.sort(reverse=False)
    print speed
    print flow
    print date_list
    plt.xlabel('flow(veh/15min)')
    plt.ylabel('speed(km/h)')
    plt.scatter(flow, speed, s=4)
    plt.savefig('pic/speed-flow-general-38.png')
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
    # general_figure('HD001038', '2015/3/10')
    date = '2015/12/9'
    day_flow_figure('HD001038', date)
    day_flow_figure('HD001039', date)
    # search_data('HD001038', '2015/1/16')



