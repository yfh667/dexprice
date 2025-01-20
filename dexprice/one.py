from datetime import datetime, timezone
import time
def datetime_to_timestamp(year, month, day, hour=0, minute=0, second=0, is_utc=True):
    """
    将指定的日期时间转换为时间戳（秒）。
    
    参数:
    - year, month, day, hour, minute, second: 日期时间组件
    - is_utc: 是否为 UTC 时间，如果为 False 则使用本地时间
    
    返回:
    - 时间戳（整数，单位为秒）
    """
    dt = datetime(year, month, day, hour, minute, second)
    if is_utc:
        dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp())

def timestamp_to_datetime(timestamp, to_utc=True):
    """
    将时间戳转换为日期时间格式。
    
    参数:
    - timestamp: 时间戳（秒）
    - to_utc: 是否返回 UTC 时间
    
    返回:
    - 日期时间格式
    """
    if to_utc:
        return datetime.fromtimestamp(timestamp, tz=timezone.utc)
    else:
        return datetime.fromtimestamp(timestamp)

# # 示例使用

# def  compare(creattime,now):
#
#     dt_object = datetime.strptime(creattime, "%Y-%m-%d %H:%M:%S")
#
#     # 转换为时间戳
#     creattimetimestamp = int(dt_object.timestamp())
#
#     print(creattimetimestamp)
#     print(now)
def compare(creattime, now):
    """
    比较 creattime 和 now 是否在同一个小时内，且 creattime 小于等于 now。

    参数:
    - creattime: 创建时间（字符串格式：%Y-%m-%d %H:%M:%S）
    - now: 当前时间的时间戳（单位：秒）

    返回:
    - 0: 如果 now 在 creattime 的同一个小时内
    - 1: 否则
    """
    # 将 creattime 转为 UTC 时间戳
    dt_object = datetime.strptime(creattime, "%Y-%m-%d %H:%M:%S")
    creattimetimestamp = int(dt_object.replace(tzinfo=timezone.utc).timestamp())

    # 获取 creattime 和 now 的小时起始时间戳
    creation_hour_start = creattimetimestamp - (creattimetimestamp % 3600)
    now_hour_start = now - (now % 3600)

    # 检查 now 是否在 creattime 的同一个小时
    if creation_hour_start == now_hour_start and creattimetimestamp <= now:
        return 0  # 同一小时内
    else:
        return 1  # 不在同一小时内
# 将当前本地时间转换为UTC时间戳
# current_timestamp = datetime_to_timestamp(2024, 11, 4, 0, 0, 0, is_utc=True)
# print("指定UTC时间转换后的时间戳:", current_timestamp)

# current_timestamp = int(time.time())


# before_timestamp = str(current_timestamp)  # 当前时间的时间戳
#
# print(before_timestamp)
#
print("转换后的UTC时间:", timestamp_to_datetime(1716376800))
# print("转换后的本地时间:", timestamp_to_datetime(current_timestamp, to_utc=False))
#
# # 将时间字符串解析为datetime对象
# dt_object = datetime.strptime("2024-11-17 09:38:38", "%Y-%m-%d %H:%M:%S")
#
# # 转换为时间戳
# timestamp = int(dt_object.timestamp())
# print("时间戳:", timestamp)
# if(compare("2024-11-17 06:38:38",current_timestamp)):
#     print("yes")
# else:
#     print("no")