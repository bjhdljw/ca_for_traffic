#coding:utf-8
#!/usr/bin/env python
import numpy as np
import sys
import random
import csv
import ConfigParser

HAVECAR = 1
WALL = 3
EMPTY = 0
CONGESTION = 2
PROBSLOW = 0.1


class Road(object):
    def __init__(self):
        # 从road.conf配置文件获取道路初始化参数
        cp = ConfigParser.SafeConfigParser()
        cp.read('road.conf')
        # 仿真时长（时间步数）
        self.simulation_times = cp.getint('road', 'simulation_times')
        # 车道数量
        self.lanes = cp.getint('road', 'lanes')
        # 车道长度（单位：元胞）
        self.length = cp.getint('road', 'road_length')
        # 初始化道路信息数组
        self.positionArray = np.zeros((self.lanes + 2, self.length))
        # 初始化车速信息数组
        self.speedArray = np.zeros((self.lanes + 2, self.length))
        # 行程时间计数数组（单位：时间步）
        self.speedCounter = np.zeros((self.lanes + 2, self.length))
        # 停车等待时长数组
        self.timeWaited = np.zeros((self.lanes + 2, self.length))
        # 初始化道路左右边界
        self.positionArray[0, :] = WALL
        self.positionArray[self.lanes + 1, :] = WALL
        self.speedArray[0, :] = WALL
        self.speedArray[self.lanes + 1, :] = WALL
        self.speedCounter[0, :] = WALL
        self.speedCounter[self.lanes + 1, :] = WALL
        self.timeWaited[0, :] = WALL
        self.timeWaited[self.lanes + 1, :] = WALL
        # 获取车辆最大速度
        self.vmax = cp.getint('road', 'vmax')
        # 获取进车概率
        self.prob_in = cp.getfloat('road', 'pro_in')
        # 获取限速开关
        self.is_limit = cp.getboolean('road', 'islimit')
        # 获取限速区速起始位置
        self.limit_begin = cp.getint('road', 'limit_begin')
        # 获取限速区结束位置
        self.limit_end = cp.getint('road', 'limit_end')
        # ？？？
        self.lane_for_st_figure = cp.getint('road', 'lane_for_st_figure')
        self.count_flow = 0
        self.travel_time = 0
        self.travel_speed = 0
        # 设置换道概率
        self.switch_lane_prob = cp.getint('road', 'switch_lane_prob')
        # 换道次数统计
        self.switch_counter = 0
        # 获取限速区限速值
        self.limit_speed = cp.getint('road', 'limit_speed')
        # 获取事故点开关
        self.iscongestion = cp.getboolean('road', 'iscongestion')
        # 获取单车道限速值
        # TODO 车道数量不应该写死
        self.vmax1 = cp.getint('road', 'vmax1')
        self.vmax2 = cp.getint('road', 'vmax2')
        self.vmax3 = cp.getint('road', 'vmax3')
        if self.iscongestion:
            # 获取事故点车道
            self.congestion_point_lane = cp.getint('road', 'congestion_point_lane')
            # 获取事故点起始位置
            self.congestion_point_point = cp.getint('road', 'congestion_point_point')
            # 获取事故点长度
            self.congestion_length = cp.getint('road', 'congestion_length')
            # 设置道路信息数组的事故点
            self.positionArray[self.congestion_point_lane,
            self.congestion_point_point: self.congestion_point_point + self.congestion_length] = CONGESTION
        # 获取停车等待时间
        self.time_can_wait = cp.getint('road', 'time_can_wait')
        self.switch_left_prob = cp.getfloat('road', 'switch_left_prob')

    """获取当前车道限制速度"""
    def get_vmax(self, lane):
        if lane == 1:
            return self.vmax1
        elif lane == 2:
            return self.vmax2
        elif lane == 3:
            return self.vmax3

    # def progeress_dqn(self, speed, input_actions):
    #     self.progress(speed)

    """道路状态演化函数"""
    def progress(self, speed):
        """中间变量 start"""
        """这些中间变量感觉可以尝试不放在循环里"""
        limit_speed = speed
        positionArray = self.positionArray
        speedArray = self.speedArray
        speedCounter = self.speedCounter
        timeWaited = self.timeWaited
        islimit = False
        '''中间变量 end'''
        '''中间变量：减速步使用 start'''
        gap = np.zeros(positionArray.shape)
        left_change_condition = np.zeros(positionArray.shape)
        right_change_condition = np.zeros(positionArray.shape)
        left_change_real = np.zeros(positionArray.shape)
        right_change_real = np.zeros(positionArray.shape)
        '''中间量：减速步使用 end'''
        """第一个循环：计算gap数组、执行加速步、时间步计数begin"""
        for i in range(1, positionArray.shape[0] - 1):
            gap_position_temp = sys.maxint
            """从道路最前面的一辆车开始遍历"""
            for j in range(positionArray.shape[1] - 1, -1, -1):
                '''确定当前的vmax：vmax or limit_speed start'''
                vmax = self.get_vmax(i)
                if positionArray[i, j] == 1:
                    """如果存在限速区，并且当前车辆位于限速区内，更新最大限制速度"""
                    if positionArray[i, j] == 1 and self.is_limit and self.limit_begin <= j <= self.limit_end:
                        islimit = True
                        vmax = limit_speed
                    else:
                        islimit = False
                '''确定当前的vmax：vmax or limit_speed end'''
                '''加速步骤begin'''
                speedArray[i, j] = min(speedArray[i, j] + 1, vmax)
                '''加速步骤end'''
                '''计算前车距离begin'''
                if positionArray[i, j] == 1 or positionArray[i, j] == 2:
                    """检查车辆间距是否计算正确，不正确抛出异常"""
                    if gap_position_temp - j - 1 < 0:
                        raise RuntimeError('gap error')
                    """如果是道路最前面的一辆车，gap为 sys.maxint - j - 1 """
                    gap[i, j] = gap_position_temp - j - 1
                    gap_position_temp = j
                '''计算前车距离end'''
                '''行程开始时间累计（单位：时间步）begin'''
                if self.limit_begin <= j <= self.limit_end and speedCounter[i, j] != 0:
                    speedCounter[i, j] += 1
                '''行程开始时间累计（单位：时间步）end'''
        """第一个循环：计算gap数组、执行加速步、时间步计数end"""
        '''第二个循环：逐车道换道begin'''
        for i in range(1, self.lanes + 1):
            switch_lane(positionArray, i, self.lanes, self.vmax, right_change_condition, left_change_condition,
                        speedArray, gap, left_change_real, right_change_real, self.switch_lane_prob, speedCounter, self, timeWaited, islimit)
        '''第二个循环：逐车道换道end'''
        '''第三个循环：换道后更新前车距离begin'''
        gap = np.zeros(positionArray.shape)
        for i in range(1, positionArray.shape[0] - 1):
            gap_position_temp = sys.maxint
            for j in range(positionArray.shape[1] - 1, -1, -1):
                if positionArray[i, j] == 1 or positionArray[i, j] == 2:
                    if gap_position_temp - j - 1 < 0:
                        raise RuntimeError('gap error')
                    gap[i, j] = gap_position_temp - j - 1
                    gap_position_temp = j
        '''第三个循环：换道后更新前车距离end'''
        '''第四个循环：减速步、随机慢化步begin'''
        for i in range(1, positionArray.shape[0] - 1):
            # 计数器，第1辆车和第2辆车减速步特殊处理：第1辆车不需要减速
            count = 1
            """记录前车距离的临时变量"""
            gap_position_temp2 = sys.maxint
            for j in range(positionArray.shape[1] - 1, -1, -1):
                '''确定当前的vmax：vmax or limit_speed'''
                vmax = limit_speed if (positionArray[i, j] == 1 and self.is_limit and self.limit_begin <= j <= self.limit_end) else self.vmax
                '''确定当前的vmax：vmax or limit_speed'''
                '''减速步begin'''
                if positionArray[i, j] == 1 or positionArray[i, j] == 2:
                    if positionArray[i, j] == 2:
                        pass
                    # 如果前方不是车辆，而是障碍物的话，不需要考虑前车速度，使用NaSch模型减速步
                    elif gap_position_temp2 < positionArray.shape[1] and positionArray[i, gap_position_temp2] == 2:
                        temp_speed = min(speedArray[i, j], gap[i, j])
                        speedArray[i, j] = max(temp_speed, 0)
                    elif count == 1:
                        pass
                    elif count == 2:
                        temp_speed = min(speedArray[i, j], gap[i, j])
                        speedArray[i, j] = max(temp_speed, 0)
                    # 如果前方是车辆的话，为了更快行进，会考虑前车速度，使用VE减速步
                    else:
                        d = max(0, gap[i, gap_position_temp2] - 1)
                        vmax_before = limit_speed if (self.is_limit and self.limit_begin <= gap_position_temp2 <= self.limit_end) else self.vmax
                        vq = min(vmax_before - 1, d)
                        vq = min(vq, speedArray[i, gap_position_temp2])
                        speedArray[i, j] = min(speedArray[i, j], gap[i, j] + vq)
                        if speedArray[i, j] > d + gap[i, j]:
                            raise RuntimeError('ve error')
                    count += 1
                    gap_position_temp2 = j
                    if speedArray[i, j] < 0:
                        raise RuntimeError('v error')
                '''减速步end'''
                '''随机慢化步begin'''
                if positionArray[i, j] == 1 and random.uniform(0, 1) <= PROBSLOW:
                    speedArray[i, j] = max(speedArray[i, j] - 1, 0)
                '''随机慢化步end'''
        '''第四个循环：减速步、随机慢化步end'''
        '''第五个循环：监测点统计数据、位置更新 begin'''
        for i in range(1, positionArray.shape[0] - 1):
            for j in range(positionArray.shape[1] - 1, -1, -1):
                '''Nasch位置更新步begin'''
                if positionArray[i, j] == 1:
                    position_next = int(j + speedArray[i, j])
                    if position_next != j:
                        '''流量&总行程时间&总行程车速统计begin'''
                        '''限速区末端为计数点'''
                        if j <= self.limit_end <= position_next:
                            self.count_flow += 1
                            self.travel_time += speedCounter[i, j]
                            self.travel_speed += (self.limit_end - self.limit_begin) / speedCounter[i, j]
                        '''流量&总行程时间&总行程车速统计end'''
                        if position_next < positionArray.shape[1]:
                            positionArray[i, position_next] = 1
                            speedArray[i, position_next] = speedArray[i, j]
                            speedCounter[i, position_next] = speedCounter[i, j]
                            timeWaited[i, position_next] = 0
                        positionArray[i, j] = 0
                        speedArray[i, j] = 0
                        speedCounter[i, j] = 0
                        timeWaited[i, j] = 0
                    elif position_next == j and j != 0:
                        timeWaited[i, j] += 1
                '''Nasch位置更新步end'''
        '''第五个循环：监测点统计数据、位置更新 end'''
        return positionArray


# def prepare_space_time(positionArray, lane):
#     out = open('space_time.csv', mode='a')
#     csv_writer = csv.writer(out, dialect='excel')
#     csv_writer.writerow(positionArray[lane, :])


def switch_lane(positionArray, i, lanes, vmax, right_change_condition, left_change_condition, speedArray, gap, left_change_real, right_change_real, switch_lane_prob, speedCounter, road, timeWaited, islimit):
    for j in range(positionArray.shape[1] - 1, -1, -1):
        change_force = False
        if positionArray[i, j] == 1 and road.iscongestion and i == road.congestion_point_lane and j < road.congestion_point_point and j + vmax > road.congestion_point_point:
            change_force = True
        if (timeWaited[i, j] != 0 and timeWaited[i, j] % (road.time_can_wait * 2) == 0) or change_force:
            '''计算换道条件begin'''
            if positionArray[i, j] == 1:
                if i == 1:
                    change = True
                    if positionArray[i + 1, j] == 1 or positionArray[i + 1, j] == 2:
                        change = False
                    right_change_condition[i, j] = change
                elif i == lanes:
                    change = True
                    if positionArray[i - 1, j] == 1 or positionArray[i - 1, j] == 2:
                        change = False
                    left_change_condition[i, j] = change
                elif 1 < i < lanes:
                    change_left = True
                    change_right = True
                    if positionArray[i - 1, j] == 1 or positionArray[i - 1, j] == 2:
                        change_left = False
                    if positionArray[i + 1, j] == 1 or positionArray[i + 1, j] == 2:
                        change_right = False
                    left_change_condition[i, j] = change_left
                    right_change_condition[i, j] = change_right
            '''计算换道条件end'''
            '''计算是否满足换道动机（即是否换道）begin'''
            if positionArray[i, j] == 1:
                if i == 1:
                    if (gap[i, j] == 0 and right_change_condition[i, j] == 1 and random.uniform(0, 1) < switch_lane_prob) or (change_force and right_change_condition[i, j] == 1):
                        right_change_real[i, j] = 1
                elif 1 < i < lanes:
                    if (gap[i, j] == 0 and right_change_condition[i, j] == 1 and random.uniform(0, 1) < switch_lane_prob) or (change_force and right_change_condition[i, j] == 1):
                        right_change_real[i, j] = 1
                    if (gap[i, j] == 0 and left_change_condition[i, j] == 1 and random.uniform(0, 1) < switch_lane_prob) or (change_force and left_change_condition[i, j] == 1):
                        left_change_real[i, j] = 1
                elif i == lanes:
                    if (gap[i, j] == 0 and left_change_condition[i, j] == 1 and random.uniform(0, 1) < switch_lane_prob) or (change_force and left_change_condition[i, j] == 1):
                        left_change_real[i, j] = 1
            '''计算是否满足换道动机（即是否换道）end'''
            '''进行换道begin'''
            if positionArray[i, j] == 1 and (left_change_real[i, j] == 1 or right_change_real[i, j] == 1):
                if i == 1:
                    if positionArray[i + 1, j] == 1:
                        print 'lane= %d' % i
                        print 'j= %d' % j
                        raise RuntimeError('switch error')
                    positionArray[i + 1, j] = 1
                    speedArray[i + 1, j] = speedArray[i, j]
                    speedCounter[i + 1, j] = speedCounter[i, j]
                    timeWaited[i + 1, j] = 0
                elif 1 < i < lanes and left_change_real[i, j] == 1 and random.uniform(0, 1) < road.switch_left_prob:
                    if left_change_real[i, j] == 1 and right_change_real[i, j] != 1:
                        if positionArray[i - 1, j] == 1:
                            print 'lane= %d' % i
                            print 'j= %d' % j
                            raise RuntimeError('switch error')
                        positionArray[i - 1, j] = 1
                        speedArray[i - 1, j] = speedArray[i, j]
                        speedCounter[i - 1, j] = speedCounter[i, j]
                        timeWaited[i - 1, j] = 0
                    if left_change_real[i, j] != 1 and right_change_real[i, j] == 1:
                        if positionArray[i + 1, j] == 1:
                            print 'lane= %d' % i
                            print 'j= %d' % j
                            raise RuntimeError('switch error')
                        positionArray[i + 1, j] = 1
                        speedArray[i + 1, j] = speedArray[i, j]
                        speedCounter[i + 1, j] = speedCounter[i, j]
                        timeWaited[i + 1, j] = 0
                    if left_change_real[i, j] == 1 and right_change_real[i, j] == 1 and random.uniform(0, 1) < road.switch_left_prob:
                        if positionArray[i - 1, j] == 1:
                            print 'lane= %d' % i
                            print 'j= %d' % j
                            raise RuntimeError('switch error')
                        positionArray[i - 1, j] = 1
                        speedArray[i - 1, j] = speedArray[i, j]
                        speedCounter[i - 1, j] = speedCounter[i, j]
                        timeWaited[i - 1, j] = 0
                    elif right_change_real[i, j] == 1 and left_change_real[i, j] == 1:
                        if positionArray[i + 1, j] == 1:
                            print 'lane= %d' % i
                            print 'j= %d' % j
                            raise RuntimeError('switch error')
                        positionArray[i + 1, j] = 1
                        speedArray[i + 1, j] = speedArray[i, j]
                        speedCounter[i + 1, j] = speedCounter[i, j]
                        timeWaited[i + 1, j] = 0
                elif i == lanes:
                    if positionArray[i - 1, j] == 1:
                        print 'lane= %d' % i
                        print 'j= %d' % j
                        raise RuntimeError('switch error')
                    positionArray[i - 1, j] = 1
                    speedArray[i - 1, j] = speedArray[i, j]
                    speedCounter[i - 1, j] = speedCounter[i, j]
                    timeWaited[i - 1, j] = 0
                positionArray[i, j] = 0
                speedArray[i, j] = 0
                speedCounter[i, j] = 0
                road.switch_counter += 1
                timeWaited[i, j] = 0
            elif positionArray[i, j] == 1 and j != 0 and (left_change_real[i, j] != 1 and right_change_real[i, j] != 1):
                timeWaited[i, j] += 1
            '''进行换道end'''
        else:
            '''计算换道条件begin'''
            if positionArray[i, j] == 1:
                if i == 1:
                    change = True
                    tempvmax = vmax if islimit else road.get_vmax(i + 1)
                    for r in range(j - tempvmax - 1, j + 1):
                        if positionArray[i + 1, r] == 1 or positionArray[i + 1, r] == 2:
                            change = False
                            break
                    right_change_condition[i, j] = change
                elif i == lanes:
                    change = True
                    tempvmax = vmax if islimit else road.get_vmax(i - 1)
                    for l in range(j - tempvmax - 1, j + 1):
                        if positionArray[i - 1, l] == 1 or positionArray[i - 1, l] == 2:
                            change = False
                            break
                    left_change_condition[i, j] = change
                elif 1 < i < lanes:
                    change_left = True
                    change_right = True
                    tempvmaxl = vmax if islimit else road.get_vmax(i - 1)
                    tempvmaxr = vmax if islimit else road.get_vmax(i + 1)
                    for l in range(j - tempvmaxl - 1, j + 1):
                        if positionArray[i - 1, l] == 1 or positionArray[i - 1, l] == 2:
                            change_left = False
                            break
                    for r in range(j - tempvmaxr - 1, j + 1):
                        if positionArray[i + 1, r] == 1 or positionArray[i + 1, r] == 2:
                            change_right = False
                            break
                    left_change_condition[i, j] = change_left
                    right_change_condition[i, j] = change_right
            '''计算换道条件end'''
            '''计算是否满足换道动机（即是否换道）begin'''
            if positionArray[i, j] == 1:
                if i == 1:
                    if min(speedArray[i, j] + 1, vmax) > gap[i, j] and right_change_condition[
                        i, j] == 1 and random.uniform(
                            0, 1) < switch_lane_prob:
                        right_change_real[i, j] = 1
                elif 1 < i < lanes:
                    if min(speedArray[i, j] + 1, vmax) > gap[i, j] and right_change_condition[
                        i, j] == 1 and random.uniform(
                            0, 1) < switch_lane_prob:
                        right_change_real[i, j] = 1
                    if min(speedArray[i, j] + 1, vmax) > gap[i, j] and left_change_condition[
                        i, j] == 1 and random.uniform(
                            0, 1) < switch_lane_prob:
                        left_change_real[i, j] = 1
                elif i == lanes:
                    if min(speedArray[i, j] + 1, vmax) > gap[i, j] and left_change_condition[
                        i, j] == 1 and random.uniform(
                            0, 1) < switch_lane_prob:
                        left_change_real[i, j] = 1
            '''计算是否满足换道动机（即是否换道）end'''
            '''进行换道begin'''
            if positionArray[i, j] == 1 and (left_change_real[i, j] == 1 or right_change_real[i, j] == 1):
                if i == 1:
                    if positionArray[i + 1, j] == 1:
                        print 'lane= %d' % i
                        print 'j= %d' % j
                        raise RuntimeError('switch error')
                    positionArray[i + 1, j] = 1
                    speedArray[i + 1, j] = speedArray[i, j]
                    speedCounter[i + 1, j] = speedCounter[i, j]
                    timeWaited[i + 1, j] = 0
                elif 1 < i < lanes:
                    if left_change_real[i, j] == 1 and right_change_real[i, j] != 1:
                        if positionArray[i - 1, j] == 1:
                            print 'lane= %d' % i
                            print 'j= %d' % j
                            raise RuntimeError('switch error')
                        positionArray[i - 1, j] = 1
                        speedArray[i - 1, j] = speedArray[i, j]
                        speedCounter[i - 1, j] = speedCounter[i, j]
                        timeWaited[i - 1, j] = 0
                    if right_change_real[i, j] == 1 and left_change_real[i, j] != 1:
                        if positionArray[i + 1, j] == 1:
                            print 'lane= %d' % i
                            print 'j= %d' % j
                            raise RuntimeError('switch error')
                        positionArray[i + 1, j] = 1
                        speedArray[i + 1, j] = speedArray[i, j]
                        speedCounter[i + 1, j] = speedCounter[i, j]
                        timeWaited[i + 1, j] = 0
                    if right_change_real[i, j] == 1 and left_change_real[i, j] == 1 and random.uniform(0, 1) < road.switch_left_prob:
                        if positionArray[i - 1, j] == 1:
                            print 'lane= %d' % i
                            print 'j= %d' % j
                            raise RuntimeError('switch error')
                        positionArray[i - 1, j] = 1
                        speedArray[i - 1, j] = speedArray[i, j]
                        speedCounter[i - 1, j] = speedCounter[i, j]
                        timeWaited[i - 1, j] = 0
                    elif right_change_real[i, j] == 1 and left_change_real[i, j] == 1:
                        if positionArray[i + 1, j] == 1:
                            print 'lane= %d' % i
                            print 'j= %d' % j
                            raise RuntimeError('switch error')
                        positionArray[i + 1, j] = 1
                        speedArray[i + 1, j] = speedArray[i, j]
                        speedCounter[i + 1, j] = speedCounter[i, j]
                        timeWaited[i + 1, j] = 0
                elif i == lanes:
                    if positionArray[i - 1, j] == 1:
                        print 'lane= %d' % i
                        print 'j= %d' % j
                        raise RuntimeError('switch error')
                    positionArray[i - 1, j] = 1
                    speedArray[i - 1, j] = speedArray[i, j]
                    speedCounter[i - 1, j] = speedCounter[i, j]
                    timeWaited[i - 1, j] = 0
                positionArray[i, j] = 0
                speedArray[i, j] = 0
                speedCounter[i, j] = 0
                road.switch_counter += 1
                timeWaited[i, j] = 0
            elif positionArray[i, j] == 1 and j != 0 and (left_change_real[i, j] != 1 and right_change_real[i, j] != 1):
                timeWaited[i, j] += 1
            '''进行换道end'''


