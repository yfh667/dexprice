from datetime import datetime, timedelta
from datetime import datetime, timezone

def get_current_utc_date():
    """
    获取当前UTC日期并返回格式为 '2024-09-13' 的字符串
    """
    current_utc_time = datetime.utcnow()
    formatted_date = current_utc_time.strftime('%Y-%m-%d')
    return formatted_date

def get_past_utc_date(days_in_past):
    """
    获取过去指定天数的UTC日期并返回格式为 '2024-09-13' 的字符串
    :param days_in_past: 距离当前的天数
    """
    current_utc_time = datetime.utcnow()
    past_utc_time = current_utc_time - timedelta(days=days_in_past)
    formatted_date = past_utc_time.strftime('%Y-%m-%d')
    return formatted_date

def compare_utc_dates(utc_date1, utc_date2):
    """
    比较两个UTC日期，返回较早的日期
    :param utc_date1: 第一个UTC日期的字符串，格式为'%Y-%m-%d'
    :param utc_date2: 第二个UTC日期的字符串，格式为'%Y-%m-%d'
    :return: 返回较早的UTC日期
    """
    # 将日期字符串解析为 datetime 对象
    date1 = datetime.strptime(utc_date1, '%Y-%m-%d')
    if " " in utc_date2:  # 判断是否包含时间部分
        utc_date2 = utc_date2.split(" ")[0]

    date2 = datetime.strptime(utc_date2, '%Y-%m-%d')

    # 比较两个日期，返回较早的日期
    if date1 < date2:
        return 1  # date1 较早
    elif date1 > date2:
        return 0  # date2 较早
    else:
        return 1  # 日期相同

def format_date(datetime_str):
    """将日期时间字符串格式化为仅包含日期的字符串"""
    date_only = datetime_str.split(' ')[0]
    return date_only
#
# # 示例
# datetime_input = '2024-09-24 10:50:38'
# date_only = remove_time(datetime_input)
# print(date_only)  # 输出：2024-09-24
#

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

# import time
#
# current_timestamp = int(time.time())
# print(current_timestamp)