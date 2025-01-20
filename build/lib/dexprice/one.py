from datetime import datetime, timezone

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

# 示例使用
timestamp_example = 1730845729000
print("转换后的UTC时间:", timestamp_to_datetime(timestamp_example))
print("转换后的本地时间:", timestamp_to_datetime(timestamp_example, to_utc=False))

# 将当前本地时间转换为UTC时间戳
current_timestamp = datetime_to_timestamp(2024, 11, 4, 0, 0, 0, is_utc=True)
print("指定UTC时间转换后的时间戳:", current_timestamp)
