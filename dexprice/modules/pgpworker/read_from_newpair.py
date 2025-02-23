
import dexprice.modules.db.insert_db as insert_db
import time
def try_delete_table_with_retry(db, retries=3, delay=5):
    for attempt in range(retries):
        try:
            db.delete_table2()
            print("Table deleted successfully.")
            return True
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("Max retries reached. Could not delete table.")
                return False

def read_from_newpair(db_folder,db_name,send_db_name):
   # db_folder = '/home/yfh/Desktop/Data/NewPair'  # 数据库存储文件夹
  #  db_name = "newpair" + '.db'  # 数据库文件名
   # here is the newpairdb
    db = insert_db.SQLiteDatabase(db_folder, db_name)
    db.connect()
    token_new = db.readdbtoken()
    success = try_delete_table_with_retry(db)
    db.close()
# we need check the token_new that dupicated in the senddb
    db = insert_db.SQLiteDatabase(db_folder, send_db_name)
    db.connect()
    token_new = [token for token in token_new if not db.check_ca_exists(token.address)]
    db.close()

    if(success):
        print("Table successfully deleted.")
    return token_new


