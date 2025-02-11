import time
import dexprice.modules.tg.tgbot as tgbot
import threading
import dexprice.modules.pgpworker.read_from_newpair as read_from_newpair
import dexprice.modules.pgpworker.write_maindb as write_maindb
import dexprice.modules.pgpworker.refreshmaindb as refreshmaindb
import dexprice.modules.pgpworker.gettheovhl as gettheovhl
import dexprice.modules.pgpworker.strategy as strategy
from dexprice.modules.utilis.define import FilterCriteria
Proxyport =7890
def refresh(db_folder,db_name,criteria,senddbname):
    while True:
        print("\nrefresh 10-minute cycle...")
        refreshmaindb.refreshmaindb(db_folder,db_name,criteria,senddbname)
        tgbot.sendmessage_chatid("@jingou22", "refresh token", Proxyport)
        time.sleep(600)  # 10min

def ten_min_cycle(db_folder,db_name_newpair,db_name_main,criteria,senddbname):
    while True:
        print("\nStarting 10-minute cycle...")
        tokennew = read_from_newpair.read_from_newpair(db_folder,db_name_newpair,senddbname)
        write_maindb.write_maindb(tokennew,db_folder,db_name_main,criteria)
        time.sleep(300)  # 5分钟

def thirty_min_cycle(db_folder,db_name_main,senddbname):
    while True:
        print("\nStarting 30-minute cycle...")
        gettheovhl.gettheovhl(db_folder,db_name_main)
        strategy.strategy(db_folder,db_name_main, senddbname, Proxyport)
        time.sleep(1800)  # 30分钟


if __name__ == "__main__":
    # 使用多线程分别运行 10 分钟和 30 分钟的任务
    criteria = FilterCriteria(
        liquidity_usd_min=10000,
        liquidity_usd_max=None,
        fdv_min=500000,
        fdv_max=None,
        pair_age_min_hours=None,
        pair_age_max_hours= None,
        txn_buy=10,
        txn_sell=10,
        volume=1000
       )



    db_folder = '/home/yfh/Desktop/Data/NewPair'  # 数据库存储文件夹
    db_name = "newpair" + '.db'  # 数据库文件名

   # db_folder_main = '/home/yfh/Desktop/Data/Maindb'  # 数据库存储文件夹
    db_name_main = "main" + '.db'  # 数据库文件名
    senddbname = 'send'+'.db'
    ten_min_thread = threading.Thread(target=ten_min_cycle, args=(db_folder, db_name, db_name_main,criteria,senddbname))
    refresh_thread = threading.Thread(target=refresh,args=(db_folder, db_name_main, criteria,senddbname))
    #thirty_min_thread = threading.Thread(target=thirty_min_cycle,args=(db_folder, db_name_main,senddbname))

    ten_min_thread.start()
    #thirty_min_thread.start()
    refresh_thread.start()


    ten_min_thread.join()
   # thirty_min_thread.join()
    refresh_thread.join()

