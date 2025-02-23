import dexprice.modules.mexc.getalltoken as getalltoken
import dexprice.modules.cexdb.cexdb as cexdb

import dexprice.modules.utilis.define as define
import os
import dexprice.modules.utilis.findroot as findroot
import dexprice.modules.mexc.initial_timesta as initial_timesta
import dexprice.modules.mexc.initial_timesta_parall as initial_timesta_parall
import dexprice.modules.proxy.proxymultitheread as proxymultitheread
import dexprice.modules.mexc.mexcovhl_parall as mexcovhl_parall
import dexprice.modules.mexc.mexc_queue as mexc_queue
import dexprice.modules.OHLCV.one_geck as one_geck

if __name__ == '__main__':


    current_dir = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = findroot.find_project_root(current_dir)
    DATA_FOLDER = os.path.join(PROJECT_ROOT, "Data")

    db_folder = DATA_FOLDER + '/cex'  # 数据库存储文件夹
    db_name = "mexc_contract" + '.db'  # 数据库文件名
    db = cexdb.CexSQLiteDatabase(db_folder, db_name)

    db.connect()

   # symbol = getalltoken.getalltoken()
   # symbol  = ['BTC','SOL']
   # tokens = []

    rate =0.3
    capacity = 20
    max_threads_per_proxy = 1
    clash_api_url = "http://127.0.0.1:9097"
    headers = {"Authorization": "Bearer 123"}

    startport = 50000


    proxys = proxymultitheread.get_one_ip_proxy_multithread(startport, clash_api_url, headers)
    symbol = 'BTC_USDT'
    # 生成开始和结束时间的时间戳
    start_timestamp = one_geck.datetime_to_timestamp(2025, 2, 20, 0, 0, 0, is_utc=True)
    end_timestamp = one_geck.datetime_to_timestamp(2025, 2, 20, 3, 0, 0, is_utc=True)

    kline = 'Min'
    aggregate = '60'

    queue = mexc_queue.mexc_create_request_queue(symbol, start_timestamp, end_timestamp, kline, aggregate)
    print(queue)



    task_manager = mexcovhl_parall.MexcOvhlTaskManager(
        queue,
        proxys,
        rate,
        capacity,
        max_threads_per_proxy,

    )
    results, failed_tasks = task_manager.run()
    print(results)

  #  db.insert_Multidata(results)
    # 打印实例属性

    db.close()
