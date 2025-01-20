from datetime import datetime, timezone
import time
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
def compare(creattime, now):
    """
    比较 creattime 和 now 是否在同一个小时内，且 creattime 小于等于 now。

    参数:
    - creattime: 创建时间（字符串格式：%Y-%m-%d %H:%M:%S）
    - now: 当前时间的时间戳（单位：秒）

    返回:
    - 1: 如果 now 在 creattime 的同一个小时内
    - 0: 否则
    """
    # 将 creattime 转为 UTC 时间戳
    dt_object = datetime.strptime(creattime, "%Y-%m-%d %H:%M:%S")
    creattimetimestamp = int(dt_object.replace(tzinfo=timezone.utc).timestamp())

    # 获取 creattime 和 now 的小时起始时间戳
    creation_hour_start = creattimetimestamp - (creattimetimestamp % 3600)
    now_hour_start = now - (now % 3600)

    # 检查 now 是否在 creattime 的同一个小时
    if creation_hour_start == now_hour_start and creattimetimestamp <= now:
        return 1  # 同一小时内
    else:
        return 0  # 不在同一小时内

# 获取当前 UTC 时间戳
current_timestamp = int(time.time())  # 当前 UTC 时间戳
print(current_timestamp)

print(timestamp_to_datetime(current_timestamp))

# 测试时间
creattime = "2024-11-12 01:45:38"  # 示例时间字符串（UTC 时间）

# 调用 compare 函数
result = compare(creattime, current_timestamp)

# 输出结果
if result == 0:
    print("no")  # 在同一个小时内
else:
    print("yes")  # 不在同一个小时内
