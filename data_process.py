#coding:utf-8
#!/usr/bin/env python
import pandas as pd


def data_search(monitor_point, date):
    df = pd.read_csv('TAB_VEH_15MIN_ADDBLACK.csv', encoding='utf-8').fillna(0)
    flow = list()
    speed = list()
    print type(df)
    for index, row in df.iterrows():
        if row['SBBH'] == monitor_point:
            flow.append(row['VEH_TOTAL'])
            speed.append(row['AVG_SPEED'])
    print flow
    print speed


if __name__ == '__main__':
    data_search('HD001065', 1)




