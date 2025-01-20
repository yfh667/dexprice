import  dexprice.modules.strategy.normal as normal



def analyze_niuqi_intervals(dates, opens, highs, lows, closes, find_all_stable_ranges):
    """
    分析两个平稳区间之间的间隔内的波动：
    如果间隔内有某条K线的波动超过500%，且后一个区间均值大于前一个区间均值的两倍，则输出 1，否则输出 0。

    参数：
    - dates: 日期列表
    - opens: 开盘价列表
    - highs: 最高价列表
    - lows: 最低价列表
    - closes: 收盘价列表
    - find_all_stable_ranges: 函数，用于找到所有的平稳区间

    返回：
    - result: 1 如果满足条件，间隔内某条K线波动超过500%，否则返回 0。
    """

    # 获取所有平稳区间
    intervals = find_all_stable_ranges(dates, opens, highs, lows, closes)

    # 遍历每个平稳区间，分析两个平稳区间之间的间隔
    for i in range(1, len(intervals)):
        # 获取前一个区间和当前区间的均值
        prev_avg = (intervals[i - 1][2] + intervals[i - 1][3]) / 2
        curr_avg = (intervals[i][2] + intervals[i][3]) / 2

        # 如果当前区间均值大于前一个区间均值的两倍
        if curr_avg > 2 * prev_avg:
            # 获取前一个区间的结束点和当前区间的起始点
            start_date = intervals[i - 1][1]  # 前一个区间的结束日期
            end_date = intervals[i][0]       # 当前区间的起始日期

            # 找到这些日期在 dates 列表中的索引
            start_idx = dates.index(start_date)
            end_idx = dates.index(end_date)

            # 遍历区间间隔内的每一条K线
            for j in range(start_idx + 1, end_idx):  # +1 确保间隔从前一个区间的结束后开始
                if highs[j] > 5 * lows[j]:  # 判断波动是否超过 500%
                    return 1  # 如果存在，则返回 1

    # 如果所有间隔内都没有满足条件的K线，则返回 0
    return 0

def niuqi_interval(dates, opens, highs, lows, closes, daily_threshold=0.5, range_threshold=1):
    # 找到所有初始稳定区间
    stable_intervals = normal.find_all_stable_ranges2(dates, opens, highs, lows, closes,daily_threshold,range_threshold)
  #  print(stable_intervals)
   # return stable_intervals
    length = len(stable_intervals)
    # print(f" length is{length}")
    i = length - 1  # 从最后一个区间开始向前遍历
    while i > 0:
        # 当前区
     #   print(stable_intervals)
      #  print(i)
        current_interval = stable_intervals[i]
        y_now_min = current_interval[2]
        y_now_max = current_interval[3]
        x_now_start = current_interval[0]

        # 前一个区间
        previous_interval = stable_intervals[i - 1]
        y_before_min = previous_interval[2]
        y_before_max = previous_interval[3]
        x_before_end = previous_interval[1]

        # 获取日期索引
        now_id = dates.index(x_now_start)
        before_id = dates.index(x_before_end)
     #   print(previous_interval)
        # 检查是否满足合并条件
        if y_now_min <= y_before_min and y_now_max >= y_before_max:
            if before_id + 2 == now_id:  # 如果两个区间的日期只相隔 1 个
                # 合并区间
                x_modify_start = previous_interval[0]
                x_modify_end = current_interval[1]
                y_modify_min =   current_interval[2]
                y_modify_max =  current_interval[3]

                # 用合并后的区间替换当前区间
                merged_interval = (x_modify_start, x_modify_end, y_modify_min, y_modify_max)
                stable_intervals[i - 1] = merged_interval

                # 删除当前区间
                stable_intervals.pop(i)
                length -= 1  # 更新长度
                i-=1
        else:
            i -= 1  # 如果不满足条件，继续向前遍历

    return stable_intervals
