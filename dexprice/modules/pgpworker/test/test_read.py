import  dexprice.modules.pgpworker.read_from_newpair as read_from_newpair


db_folder = '/Users/admin/Desktop/single-dex/Data/Project'  # 数据库存储文件夹

db_name = 'newpair.db'  # 数据库文件名

send_db_name='send.db'
tokennew = read_from_newpair.read_from_newpair(db_folder, db_name, send_db_name)
print(tokennew)