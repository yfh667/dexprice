def find_monotonic(dates, opens, highs, lows, closes,  ):
    """
    寻找所有单调区间,严格单调区间
    """
    stable_intervals = []
    n = len(dates)
    start = 0
    intflag = 1
    # first we asscump the first flag is zhang
    while start < n:
        end = start     # 每个区间至少包含两天


        while end < n:
            # 检查每日波动幅度
            flag = 1 if closes[end] > opens[end] else 0
            #flag =1 : zhang
            #flag =0 :die
            if flag != intflag:
                intflag =flag
                break

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
def monotonic_intervals(dates, opens, highs, lows, closes):
    """
    寻找所有单调区间
    """
    stable_intervals = []
    n = len(dates)
    start = 0

    while start < n:
        end = start  # 每个区间至少包含两天
        intflag = 1 if closes[end] > opens[end] else 0  # 初始趋势设定为上涨（1）或下跌（0）

        while end < n:
            # 检查每日波动幅度
            flag = 1 if closes[end] > opens[end] else 0
            if flag != intflag:
                if end + 1 < n:
                    nextflag = 1 if closes[end+1] > opens[end+1] else 0
                    if nextflag != intflag:
                        intflag = flag
                        break
                else:
                    break
            # 如果满足条件，继续扩展区间
            end += 1

        # 只有满足区间长度条件的才添加到结果
        if end - start >= 3:
            y_min = min(lows[start:end-1])
            y_max = max(highs[start:end-1])
            x_start = dates[start]
            x_end = dates[end - 1]
            intervalflag = 1 if closes[start] > opens[start] else 0  # 初始趋势设定为上涨（1）或下跌（0）
            stable_intervals.append((x_start, x_end, y_min, y_max, intervalflag))
            start = end
        else:
            # 更新 start 到当前 end 的位置
            start += 1

    # 检查最后一个 interval
    if len(stable_intervals) > 0:
        last_interval = stable_intervals[-1]

        # 检查最后一个 interval 是否是上涨的
        if last_interval[4] == 1:  # 第五个元素表示趋势：1 为上涨
            x_start = last_interval[0]
            x_end = last_interval[1]

            # 获取起止日期在 dates 中的索引
            x_start_index = dates.index(x_start)
            x_end_index = dates.index(x_end)
            if(x_end !=dates[-1]):
                return 0
            # 检查时间跨度是否大于 5 个单位
            if (x_end_index - x_start_index) >= 5:  # 确保区间至少有 5 个单位
                return 1  # 条件满足时返回 1

    return 0