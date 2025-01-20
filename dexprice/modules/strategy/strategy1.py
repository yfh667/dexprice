
import dexprice.modules.utilis.define as define
from datetime import datetime, timedelta
import statistics

def is_active_std_dev(sorted_data, std_dev_threshold=0.05, num_points=5):
    if len(sorted_data) < num_points:
        return False

    recent_data = sorted_data[-num_points:]
    closing_prices = [item.close for item in recent_data]

    if len(set(closing_prices)) == 1:
        return False  # 价格没有变化

    std_dev = statistics.stdev(closing_prices)
    mean_price = statistics.mean(closing_prices)

    if mean_price == 0:
        return False

    coef_var = std_dev / mean_price

    if coef_var > std_dev_threshold:
        return True  # 活跃
    else:
        return False  # “死”了
class WindowData:
    def __init__(self, start, end, high, low, flag):
        """
        初始化窗口数据类

        :param start: 窗口的起始下标
        :param end: 窗口的结束下标
        :param high: 窗口期间的最高点
        :param low: 窗口期间的最低点
        :param flag: 标志位，1表示上升窗口，0表示平稳窗口，-1表示下降窗口
        """
        self.start = start
        self.end = end
        self.high = high
        self.low = low
        self.flag = flag

    def __repr__(self):
        """
        返回类的字符串表示，便于调试和打印输出
        """
        return f"WindowData(start={self.start}, end={self.end}, high={self.high}, low={self.low}, flag={self.flag})"

# def sort_by_time(ovhldata: list[define.TokenPriceHistory]):
#     # 将ovhldata按照time属性从早到晚进行排序
#     sorted_data = sorted(ovhldata, key=lambda x: x.time)
#     return sorted_data


# attention ,the tokenpricehistory.tokeid is allways same
# data = [
#     define.TokenPriceHistory(tokenid=1, open=2.362e-05, high=2.883e-05, low=2.204e-05, close='2.362e-05', time='2024-11-02 04:00:00', volume=0),
#     define.TokenPriceHistory(tokenid=1, open=2.883e-05, high=3.000e-05, low=2.500e-05, close='2.883e-05', time='2024-11-02 05:00:00', volume=0),
#     define.TokenPriceHistory(tokenid=1, open=2.204e-05, high=2.500e-05, low=2.100e-05, close='2.204e-05', time='2024-11-02 06:00:00', volume=0),
#     define.TokenPriceHistory(tokenid=1, open=2.362e-05, high=2.600e-05, low=2.300e-05, close='2.362e-05', time='2024-11-02 07:00:00', volume=0)
# ]
def simple(ovhldata:list[define.TokenPriceHistory]):

    data = sort_by_time(ovhldata)

    print(data)

def congdichufa(ovhldata:list[define.TokenPriceHistory]):
    # 首先是时间从早到晚
    sorted_data = sort_by_time(ovhldata)
    littele = 100000
    time = ''
    # we find the lowest point
    for i in ovhldata:
        if(i.low<=littele):
            littele = i.low
            time = i.time
    # we
    if(len(ovhldata)>3):
        if((ovhldata[0].close+ovhldata[1].close+ovhldata[2].close)/3 > littele*5):
            return True
    return False

class WindowData:
    def __init__(self, start, end, high, low, flag):
        self.start = start
        self.end = end
        self.high = high
        self.low = low
        self.flag = flag

    def __repr__(self):
        return f"WindowData(start={self.start}, end={self.end}, high={self.high}, low={self.low}, flag={self.flag})"

def find_bullish_pattern(ovhldata: list[define.TokenPriceHistory]):

    windows = []
    sorted_data = sort_by_time(ovhldata)  # 假设 sort_by_time 函数已经实现，保证数据按时间顺序排列
    # 将字符串时间转换为 datetime 对象
# # 将字符串时间转换为 datetime 对象，并包含时间部分
#     start_time = datetime.strptime(sorted_data[0].time, "%Y-%m-%d %H:%M:%S")  # 请根据实际时间格式调整
#     end_time = datetime.strptime(sorted_data[-1].time, "%Y-%m-%d %H:%M:%S")  # 请根据实际时间格式调整
#
#
#     # 确保时间跨度至少有 30 天
#     if len(sorted_data) < 2 or (end_time - start_time).days < 30:
#         print("数据时间跨度不足30天，无法进行分析。")
#         return False  # 返回空列表，表示不符合分析条件

    i = 0
    flat_start = 0  # 平稳窗口的起始点
    while i < len(sorted_data):
        current_data = sorted_data[i]
        high = current_data.high
        low = current_data.low
        flag = 0  # 默认平稳窗口

        # 1. 检查上升窗口
        if current_data.close > current_data.open and (current_data.high - current_data.low) / current_data.low >= 0.5:
            # 如果当前有平稳窗口，先记录平稳窗口
            if i > flat_start:
                flat_window = WindowData(start=flat_start, end=i-1, high=sorted_data[flat_start].high,
                                         low=sorted_data[flat_start].low, flag=0)
                windows.append(flat_window)

            # 上升窗口
            flag = 1
            start = i
            end = i
            for j in range(i + 1, min(i + 5, len(sorted_data))):
                if sorted_data[j].high > high:
                    high = sorted_data[j].high
                    end = j
                    # 如果找到更高的点，再尝试往后找5天
                    for k in range(j + 1, min(j + 5, len(sorted_data))):
                        if sorted_data[k].high > high:
                            high = sorted_data[k].high
                            end = k
                        else:
                            break
                else:
                    break

            # 记录上升窗口
            windows.append(WindowData(start=start, end=end, high=high, low=low, flag=flag))
            flat_start = end + 1  # 更新平稳窗口的起点为下一个数据点
            i = end + 1  # 跳过已处理的窗口
            continue

        # 2. 检查下降窗口
        elif current_data.close < current_data.open and (current_data.low - current_data.high) / current_data.high <= -0.2:
            # 如果当前有平稳窗口，先记录平稳窗口
            if i > flat_start:
                flat_window = WindowData(start=flat_start, end=i-1, high=sorted_data[flat_start].high,
                                         low=sorted_data[flat_start].low, flag=0)
                windows.append(flat_window)

            # 下降窗口
            flag = -1
            start = i
            end = i
            for j in range(i + 1, min(i + 5, len(sorted_data))):
                if sorted_data[j].low < low:
                    low = sorted_data[j].low
                    end = j
                    # 如果找到更低的点，再尝试往后找5天
                    for k in range(j + 1, min(j + 5, len(sorted_data))):
                        if sorted_data[k].low < low:
                            low = sorted_data[k].low
                            end = k
                        else:
                            break
                else:
                    break

            # 记录下降窗口
            windows.append(WindowData(start=start, end=end, high=high, low=low, flag=flag))
            flat_start = end + 1  # 更新平稳窗口的起点为下一个数据点
            i = end + 1  # 跳过已处理的窗口
            continue

        # 3. 如果不是上升或下降窗口，继续平稳窗口
        i += 1

    # 处理最后的平稳窗口
    if flat_start < len(sorted_data):
        flat_window = WindowData(start=flat_start, end=len(sorted_data)-1, high=sorted_data[flat_start].high,
                                 low=sorted_data[flat_start].low, flag=0)
        windows.append(flat_window)
    if(check_overall_trend(windows)):
        return True
    return False

def find_no_less_time(ovhldata: list[define.TokenPriceHistory]):

    flag1 = 0
    flag2 = 0

    sorted_data = sort_by_time(ovhldata)  # 假设 sort_by_time 函数已经实现，保证数据按时间顺序排列
    if not sorted_data:
        return False
    if len(sorted_data) < 2:
        return False
    for item in sorted_data[1:]:
        if item.high > item.low * 5 and item.open < item.close:
            flag1=1
         #   print(item)

    if  sorted_data[0].open<sorted_data[-1].close:
        flag2=1

    if(is_active_std_dev(sorted_data, std_dev_threshold=0.05, num_points=5)):

        return flag1 and flag2
    else:
        return False


def check_overall_trend(windows: list[WindowData]) -> bool:
    # 计算所有窗口的 flag 总和
    total_flag = sum(window.flag for window in windows)
    # 如果总和大于 0，返回 True；否则返回 False
    return total_flag > 0