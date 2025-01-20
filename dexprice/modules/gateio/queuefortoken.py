from typing import Optional, List, Tuple
from datetime import datetime, timedelta, timezone
import math
import  dexprice.modules.OHLCV.geck as geck
from typing import Optional, List, Tuple
from datetime import datetime, timedelta, timezone
import math
class namequeue:
    def __init__(self, name, kline, aggregate, before_timestamp, limit,  ):
        """
        初始化请求参数类的实例。

        :param pool_addresses: List[str], 目标池地址列表。
        :param kline: str, K线类型（'minute', 'hour', 'day'）。
        :param aggregate: str, 聚合时间段（例如 '1', '5', '15'）。
        :param before_timestamp: str, 请求之前的时间戳（UTC Unix 时间戳）。
        :param limit: int, 返回的最大数据条数。
        :param currency: str, 使用的货币类型，默认 "usd"。
        :param token: str, 代币类型，默认 "base"。
        """
        self.name = name
        self.kline = kline
        self.aggregate = aggregate
        self.before_timestamp = before_timestamp
        self.limit = limit

    def __repr__(self):
        """
        定义对象的字符串表示。
        """
        return (f"namequeue(name={self.name}, kline={self.kline}, "
                f"aggregate={self.aggregate}, before_timestamp={self.before_timestamp}, "
                f"limit={self.limit},  )")

    def to_tuple(self):
        """
        转换实例为元组形式。
        :return: tuple, 包含实例所有属性的元组。
        """
        return (self.name, self.kline, self.aggregate, self.before_timestamp,
                self.limit,   )


def create_request_queue(name: str,
                         start_timestamp: int,
                         end_timestamp: int,
                         kline: str,
                         aggregate: str,
                         ) -> List[Tuple]:
    """
    创建一个请求队列，用于获取指定时间戳范围内的 k 线数据。

    队列中的每个元素都是一个元组：
    (pool_address, kline, aggregate, before_timestamp, limit, currency, token)

    参数:
        pool_address (str): 池地址。
        start_timestamp (int): 开始时间的 Unix 时间戳（秒）。
        end_timestamp (int): 结束时间的 Unix 时间戳（秒）。
        kline (str): K 线类型（'day'、'hour' 或 'minute'）。
        aggregate (str): 聚合间隔（'1'、'5'、'15'、'4'、'12'）。
        currency (str, optional): 货币类型，默认为 'usd'。
        token (str, optional): 代币类型，默认为 'base'。

    返回:
        List[Tuple]: 每个请求批次的参数元组列表。
    """
    # 验证时间戳
    if end_timestamp <= start_timestamp:
        raise ValueError("结束时间戳必须大于开始时间戳。")

    # 将时间戳转换为 datetime 对象
    start_dt = datetime.fromtimestamp(start_timestamp, tz=timezone.utc)
    end_dt = datetime.fromtimestamp(end_timestamp, tz=timezone.utc)

    # 根据 kline 和 aggregate 定义每个 k 线的持续时间
    try:
        agg = int(aggregate)
    except ValueError:
        raise ValueError(f"聚合值必须是整数，收到的值：{aggregate}")

    if kline == 'm':
        kline_duration = timedelta(minutes=agg)
    elif kline == 'h':
        kline_duration = timedelta(hours=agg)
    elif kline == 'd':
        kline_duration = timedelta(days=agg)
    else:
        raise ValueError(f"无效的 kline 值：{kline}，应为 'minute'、'hour' 或 'day'。")

    # 计算所需的总 k 线数量
    total_seconds = (end_dt - start_dt).total_seconds()
    kline_seconds = kline_duration.total_seconds()
    total_k_lines = int(math.ceil(total_seconds / kline_seconds))

    # 初始化请求队列
    request_queue = []

    # 每次请求的最大限制
    max_limit = 1000

    # 从结束时间开始向前迭代
    current_endtime = end_dt

    while total_k_lines > 0:
        # 确定当前批次的 limit
        limit = min(max_limit, total_k_lines)

        # before_timestamp 是当前结束时间的 Unix 时间戳
        before_timestamp = str(int(current_endtime.timestamp()))


        request_queue.append(namequeue(
            name=name,
            kline=kline,
            aggregate=aggregate,
            before_timestamp=before_timestamp,
            limit=limit,


        ))

        # 更新 total_k_lines 和 current_endtime 以进行下一次迭代
        total_k_lines -= limit
        # 将 current_endtime 向前移动 (limit * kline_duration)
        time_delta = kline_duration * limit
        current_endtime -= time_delta

        # 确保不会早于 start_dt
        if current_endtime <= start_dt:
            break

    return request_queue
