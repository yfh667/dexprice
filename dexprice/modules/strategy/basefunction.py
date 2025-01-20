
import dexprice.modules.utilis.define as define
from datetime import datetime, timedelta
import statistics

def sort_by_time(ovhldata: list[define.TokenPriceHistory]):
    # 将ovhldata按照time属性从早到晚进行排序
    sorted_data = sorted(ovhldata, key=lambda x: x.time)
    return sorted_data

def transform_data(ovhldata: list[define.TokenPriceHistory]):
    dates = []
    opens = []
    highs = []
    lows = []
    closes = []

    for entry in ovhldata:
        # Convert timestamp to UNIX timestamp
        timestamp = int(datetime.strptime(entry.time, "%Y-%m-%d %H:%M:%S").timestamp())
        dates.append(timestamp)
        opens.append(entry.open)
        highs.append(entry.high)
        lows.append(entry.low)
        closes.append(entry.close)

    return dates, opens, highs, lows, closes

