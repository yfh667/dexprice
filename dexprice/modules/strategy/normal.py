
import dexprice.modules.utilis.define as define
from datetime import datetime, timedelta
import statistics

import  dexprice.modules.strategy.basefunction as basefunction
def find_all_stable_ranges(dates, opens, highs, lows, closes, daily_threshold=0.5, range_threshold=1):
    """
    寻找所有平稳区间，并返回包含所有区间的列表。
    """
    stable_intervals = []
    n = len(dates)
    start = 0

    while start < n:
        end = start     # 每个区间至少包含两天

        while end < n:
            # 检查每日波动幅度
            fluctuation = (highs[end] - lows[end]) / opens[end]
            if abs(fluctuation) > daily_threshold:
                break
            if end-start>1:
                # 检查区间内的收盘价波动幅度
                close_min = min(lows[start:end])
                close_max = max(highs[start:end])
                close_range = (close_max - close_min) / close_min

                if close_range > range_threshold:
                    break
            else:
                pass
            # 如果满足条件，继续扩展区间
            end += 1

        # 只有满足区间长度条件的才添加到结果
        if end - start >= 3:
            y_min = min(lows[start:end-1])
            y_max = max(highs[start:end-1])
            x_start = dates[start]
            x_end = dates[end - 1]
            stable_intervals.append((x_start, x_end, y_min, y_max))
            start =end

        else:
            # 更新start到当前end的位置
            start = start+1

    return stable_intervals

def find_all_stable_ranges2(dates, opens, highs, lows, closes, daily_threshold=0.5, range_threshold=1):
    """
    寻找所有平稳区间，并返回包含所有区间的列表。
    """
    stable_intervals = []
    n = len(dates)
    start = 0

    while start < n:
        end = start     # 每个区间至少包含两天

        while end < n:
            # 检查每日波动幅度
            fluctuation = (opens[end] - closes[end]) / opens[end]
            if abs(fluctuation) > daily_threshold:
                break
            if end-start>1:
                # 检查区间内的收盘价波动幅度
                close_min = min(opens[start:end])
                close_max = max(closes[start:end])
                close_range = (close_max - close_min) / close_min

                if close_range > range_threshold:
                    break
            else:
                pass
            # 如果满足条件，继续扩展区间
            end += 1

        # 只有满足区间长度条件的才添加到结果
        if end - start >= 3:
            # 将两段列表直接拼接为一个大列表
            combined = opens[start:end - 1] + closes[start:end - 1]

            y_min = min(combined)
            y_max = max(combined)
            # y_min = min((opens[start:end-1]),(closes[start:end-1]))
            # y_max = max((opens[start:end-1]),(closes[start:end-1]))
            x_start = dates[start]
            x_end = dates[end - 1]
            stable_intervals.append((x_start, x_end, y_min, y_max))
            start =end

        else:
            # 更新start到当前end的位置
            start = start+1


    return stable_intervals



def analyze_stable_intervals(stable_intervals):
    """
    对稳定区间进行分析：
    1. 找到所有区间的 y_min。
    2. 找到所有区间的 y_min 的最小值。
    3. 比较最后一个区间的 y_min 是否大于最小值的两倍，若是则输出 1，否则输出 0。

    参数：
    - stable_intervals: List of tuples, 每个元素为 (x_start, x_end, y_min, y_max)

    返回：
    - result: 1 如果最后一个区间的 y_min > 最小 y_min 的两倍，否则返回 0。
    """
    # 提取所有区间的 y_min
    y_mins = [interval[2] for interval in stable_intervals]

    # 找到最小的 y_min
    min_y_min = min(y_mins)

    # 找到最后一个区间的 y_min
    last_y_min = stable_intervals[-1][2]

    # 比较最后一个区间的 y_min 是否大于最小值的两倍
    if last_y_min > 2 * min_y_min:
        return 1
    else:
        return 0


# 示例使用
# stable_intervals = find_all_stable_ranges(dates, opens, highs, lows, closes, daily_threshold=0.5, range_threshold=1)
# result = analyze_stable_intervals(stable_intervals)
#


# print("分析结果:", result)
def checknormalgui(ovhldata: list[define.TokenPriceHistory]):
    sortdata = basefunction.sort_by_time(ovhldata)
    dates, opens, highs, lows, closes = basefunction.transform_data(sortdata)


    return dates, opens, highs, lows, closes

def checknormalgui_one(ovhldata: list[define.TokenPriceHistory]):
    # 假设 basefunction.sort_by_time 和 basefunction.transform_data 是有效的
    sortdata = basefunction.sort_by_time(ovhldata)
    dates, opens, highs, lows, closes = basefunction.transform_data(sortdata)

    # 获取 open 的第一个元素，用于归一化
    open_0 = opens[0]

    # 对所有价格进行归一化（除以 opens[0]）
    opens = [x / open_0 for x in opens]  # 归一化 open
    highs = [x / open_0 for x in highs]  # 归一化 high
    lows = [x / open_0 for x in lows]    # 归一化 low
    closes = [x / open_0 for x in closes] # 归一化 close

    return dates, opens, highs, lows, closes

def checknormal(ovhldata: list[define.TokenPriceHistory]):
    sortdata = basefunction.sort_by_time(ovhldata)
    dates, opens, highs, lows, closes = basefunction.transform_data(sortdata)
        # time series
    stable_intervals =find_all_stable_ranges(dates, opens, highs, lows, closes, daily_threshold=0.5, range_threshold=1)
    if(len(stable_intervals)==0):
        return False
    else:
     return  analyze_stable_intervals(stable_intervals)