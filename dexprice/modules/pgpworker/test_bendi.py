
import dexprice.modules.pgpworker.read_from_newpair as read_from_newpair
import dexprice.modules.pgpworker.write_maindb as write_maindb
import dexprice.modules.pgpworker.refreshmaindb as refreshmaindb
import dexprice.modules.pgpworker.gettheovhl as gettheovhl
import dexprice.modules.pgpworker.strategy as strategy
from dexprice.modules.utilis.define import FilterCriteria
import dexprice.modules.tg.tgbot as tgbot

Proxyport =7890

def refresh(db_folder,db_name,criteria):
    #while True:
        print("\nrefresh 10-minute cycle...")
        refreshmaindb.refreshmaindb(db_folder,db_name,criteria)
      #  tgbot.sendmessage_chatid("@jingou22", "refresh token", Proxyport)
       # time.sleep(300)  # 5min

def ten_min_cycle(db_folder_newpair,db_name_newpair,db_name_main,criteria,send_dbname):
   # while True:
      #  print("\nStarting 10-minute cycle...")
        tokennew = read_from_newpair.read_from_newpair(db_folder_newpair,db_name_newpair,send_dbname)
        write_maindb.write_maindb(tokennew,db_folder_newpair,db_name_main,criteria)
      #  time.sleep(600)  # 10分钟

def thirty_min_cycle(db_folder_main,db_name_main,send_dbname):
 #   while True:
    #    print("\nStarting 30-minute cycle...")
        gettheovhl.gettheovhl(db_folder_main,db_name_main)
        strategy.strategy(db_folder_main,db_name_main, send_dbname, Proxyport,0)
     #   time.sleep(1800)  # 30分钟

if __name__ == "__main__":
    # 使用多线程分别运行 10 分钟和 30 分钟的任务

    criteria = FilterCriteria(
        liquidity_usd_min=10000,
        liquidity_usd_max=None,
        fdv_min=500000,
        fdv_max=None,
        pair_age_min_hours=None,
        pair_age_max_hours= None,
        txn_buy=100,
        txn_sell=100,
        volume=10000
       )
    db_folder = '/Users/admin/Desktop/single-dex/Data/Project'  # 数据库存储文件夹
    db_name = "newpair" + '.db'  # 数据库文件名
    db_name_main = "main" + '.db'  # 数据库文件名
    send_dbname = "send" + '.db'

    ten_min_cycle(db_folder,db_name,db_name_main,criteria,send_dbname)
    refresh(db_folder,db_name,criteria)
    thirty_min_cycle(db_folder,db_name_main,send_dbname)
