
import time
import dexprice.modules.tg.tgbot as tgbot
import threading
import dexprice.modules.pgpworker.read_from_newpair as read_from_newpair
import dexprice.modules.pgpworker.write_maindb as write_maindb
import dexprice.modules.pgpworker.refreshmaindb as refreshmaindb
import dexprice.modules.pgpworker.gettheovhl as gettheovhl
import dexprice.modules.pgpworker.strategy as strategy

Proxyport =7890


def refresh(db_folder,db_name):
    # while True:
        print("\nrefresh 10-minute cycle...")
        refreshmaindb.refreshmaindb(db_folder,db_name)
     #   tgbot.sendmessage_chatid("@jingou22", "refresh token", Proxyport)
     #   time.sleep(300)  # 5min

def ten_min_cycle(db_folder_newpair,db_name_newpair,db_folder_main,db_name_main):
    # while True:
        print("\nStarting 10-minute cycle...")
        tokennew = read_from_newpair.read_from_newpair(db_folder_newpair,db_name_newpair)
        write_maindb.write_maindb(tokennew,db_folder_main,db_name_main)
     #   time.sleep(600)  # 10分钟

def thirty_min_cycle(db_folder_main,db_name_main):
    # while True:
        print("\nStarting 30-minute cycle...")
        gettheovhl.gettheovhl(db_folder_main,db_name_main)
        strategy.strategy(db_folder_main,db_name_main,  Proxyport,0)
       # time.sleep(1800)  # 30分钟

if __name__ == "__main__":
    # 使用多线程分别运行 10 分钟和 30 分钟的任务


    db_folder = '/Users/admin/Desktop/single-dex/Data/Project'  # 数据库存储文件夹
    db_name = "newpair" + '.db'  # 数据库文件名

    db_folder_main = '/Users/admin/Desktop/single-dex/Data/Project'  # 数据库存储文件夹
    db_name_main = "main" + '.db'  # 数据库文件名

    ten_min_cycle(db_folder,db_name,db_folder_main,db_name_main)
    refresh(db_folder,db_name)
    thirty_min_cycle(db_folder_main,db_name_main)
    # ten_min_thread = threading.Thread(target=ten_min_cycle, args=(db_folder, db_name,db_folder_main, db_name_main))
    # refresh_thread = threading.Thread(target=refresh,args=(db_folder_main, db_name_main))
    # thirty_min_thread = threading.Thread(target=thirty_min_cycle,args=(db_folder_main, db_name_main))

    # ten_min_thread.start()
    # thirty_min_thread.start()
    # refresh_thread.start()

    #
    # ten_min_thread.join()
    # thirty_min_thread.join()
    # refresh_thread.join()

