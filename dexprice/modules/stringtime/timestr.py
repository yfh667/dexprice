from datetime import datetime, timedelta

#klinetype :

from datetime import datetime
import dexprice.modules.utilis.define as define

def if_kline(starttime, timestamps, klinetype):
    # 将输入时间字符串解析为 datetime 对象
    starttime = datetime.strptime(starttime, '%Y-%m-%d %H:%M:%S')
    nowtimestamps = datetime.strptime(timestamps, '%Y-%m-%d %H:%M:%S')

    # 根据 K线类型设置时间间隔
    if klinetype == "15min":
        t = 15
    elif klinetype == "30min":
        t = 30
    else:
        raise ValueError("Unsupported klinetype. Use '15min' or '30min'.")

    # 判断是否在同一天和同一小时
    if (starttime.year == nowtimestamps.year and
            starttime.month == nowtimestamps.month and
            starttime.day == nowtimestamps.day and
            starttime.hour == nowtimestamps.hour):

        # 计算 K 线的起始时间
        start_minute = (starttime.minute // t) * t
        now_minute_start = (nowtimestamps.minute // t) * t

        # 创建起始时间对象
        start_time = starttime.replace(minute=start_minute, second=0, microsecond=0)
        now_time_start = nowtimestamps.replace(minute=now_minute_start, second=0, microsecond=0)

        # 判断两者是否在同一 K 线时间区间
        if start_time == now_time_start:
            return 1

    return 0

# 我们找到当前时间的初始
def time_start(starttime,klinetype):
    nowtimestamps = datetime.strptime(starttime, '%Y-%m-%d %H:%M:%S')
    if klinetype == "15min":
        t = 15
    elif klinetype == "30min":
        t = 30
    else:
        raise ValueError("Unsupported klinetype. Use '15min' or '30min'.")
    start_minute = (nowtimestamps.minute // t) * t
    start_time = nowtimestamps.replace(minute=start_minute, second=0, microsecond=0)
    dt_string = start_time.strftime('%Y-%m-%d %H:%M:%S')

    return dt_string


# # 示例5分钟K线时间序列
# timestamps = [
#     '2025-01-22 21:00:00',
#     '2025-01-22 21:05:00',
#     '2025-01-22 21:10:00',
#     '2025-01-22 21:15:00',
#     '2025-01-22 21:20:00',
#     '2025-01-22 21:25:00',
#     '2025-01-22 21:30:00',
#     '2025-01-22 21:35:00',
#     '2025-01-22 21:55:00',
# ]

def findnewinterval(timestamps,klinetype):
    startidx=0
    endidx=0
    timestamps_re = []
    while(len(timestamps)-1 >= startidx):

        start = timestamps[startidx]
        starttime =time_start(start,klinetype)
        endidx = startidx
        timestart =  startidx
        for timestamp in timestamps[timestart+1:]:
            if(if_kline(starttime, timestamp, klinetype)):
                endidx = endidx+1
            else:
                break
        if(startidx ==endidx):
            startidx = startidx + 1
        else:
            startidx = endidx+1

        timestamps_re.append(starttime)

