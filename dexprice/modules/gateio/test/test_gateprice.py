import  dexprice.modules.gateio.cexprice as gateprice

import dexprice.modules.OHLCV.one_geck as one_geck
if __name__ == "__main__":
    currency_pair = "0DOG_USDT"
    interval = "1d"  # 日线
    limit = 2       # 数据点数量
    end_timestamp = one_geck.datetime_to_timestamp(2024, 12, 7, 0, 0, 0, is_utc=True)

    proxy_port = 50057  # 本地代理端口

   # result = gateprice.get_cex_ohlcv_data(currency_pair, interval, limit, end_timestamp, proxy_port=proxy_port)

    result =  gateprice.get_token_history2(currency_pair, interval, limit, end_timestamp, proxy_port)
    if result:
        print("K线数据获取成功：")
        print(result)
    else:
        print("K线数据获取失败。")

