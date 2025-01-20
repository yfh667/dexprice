

import  dexprice.modules.utilis.define as define
from datetime import datetime, timedelta
import dexprice.modules.utilis.define as define
from dexprice.modules.utilis.define import OvhlRawPrice
import dexprice.modules.db.insert_db as insert_db
from datetime import datetime, timedelta
import dexprice.modules.utilis.define as define

def PriceIntoOvhl(datas: list[define.OvhlRawPrice], interval: str):
    # 定义时间间隔映射
    interval_mapping = {
        "15min": timedelta(minutes=15),
        "1h": timedelta(hours=1),
        "4h": timedelta(hours=4),
        "8h": timedelta(hours=8),
        "12h": timedelta(hours=12),
        "24h": timedelta(hours=24)
    }

    # 检查 interval 是否有效
    if interval not in interval_mapping:
        raise ValueError(f"Unsupported interval: {interval}")

    # 获取时间间隔
    interval_delta = interval_mapping[interval]

    # 将数据按时间排序
    datas.sort(key=lambda x: x.time)

    # 获取第一个数据的 UTC 开始时间，按照 interval 进行对齐
    first_time = datetime.strptime(datas[0].time, "%Y-%m-%d %H:%M:%S")
    aligned_start_time = first_time.replace(minute=0, second=0, microsecond=0)
    while aligned_start_time > first_time:
        aligned_start_time -= interval_delta

    # 初始化时间窗口
    current_start = aligned_start_time
    current_end = aligned_start_time + interval_delta

    # 初始化存储每个间隔的价格数据
    group_prices = []
    ohlc_data = []

    for data in datas:
        data_time = datetime.strptime(data.time, "%Y-%m-%d %H:%M:%S")

        # 如果当前数据不在当前时间段内，计算并保存当前时间段的 OHLC 值
        while data_time >= current_end:
            if group_prices:
                open_price = group_prices[0]
                high_price = max(group_prices)
                low_price = min(group_prices)
                close_price = group_prices[-1]
                # 使用 TokenPriceHistory 类来保存结果
                ohlc_data.append(
                    define.TokenPriceHistory(
                        tokenid=data.tokenid,
                        open=open_price,
                        high=high_price,
                        low=low_price,
                        close=close_price,
                        time=current_start.strftime("%Y-%m-%d %H:%M:%S"),
                        volume=0  # 假设没有 volume 数据
                    )
                )

            # 移动到下一个时间段
            current_start = current_end
            current_end += interval_delta
            group_prices = []

        # 当前价格在当前时间段内，添加到当前分组
        group_prices.append(data.price)

    # 处理最后一个时间段的数据
    if group_prices:
        open_price = group_prices[0]
        high_price = max(group_prices)
        low_price = min(group_prices)
        close_price = group_prices[-1]
        ohlc_data.append(
            define.TokenPriceHistory(
                tokenid=datas[0].tokenid,  # 假设所有数据都是同一个 token
                open=open_price,
                high=high_price,
                low=low_price,
                close=close_price,
                time=current_start.strftime("%Y-%m-%d %H:%M:%S"),
                volume=0  # 假设没有 volume 数据
            )
        )

    # 输出结果
    # for entry in ohlc_data:
    #     print(entry)
    return ohlc_data
def process_and_store_price_data(token_new, db:insert_db.DatabaseInterface, interval='15min'):
    """
    处理并存储价格数据。

    :param token_new: 包含 token 的列表
    :param db: 数据库对象
    :param interval: OHLC 的时间间隔，如 '15min'
    """
    for token in token_new:
        # 获取价格数据
        data = db.getpricedexscreen(token.tokenid)

        # 将数据转换为 OvhlRawPrice 对象列表
        price_records = [OvhlRawPrice(tokenid, price, time) for tokenid, price, time in data]

        # 根据指定的时间间隔生成 OHLC 数据
        ohlc_data = PriceIntoOvhl(price_records, interval)

        # 输出 OHLC 数据
        for ohlc in ohlc_data:
            print(ohlc)

        # 插入 OHLC 数据到数据库
        db.insertMultipricehistory(ohlc_data)
    db.delete_table()