from dexprice.modules.utilis.define import FilterCriteria
import dexprice.modules.db.insert_db as insert_db
import os
import dexprice.modules.utilis.findroot as findroot
import dexprice.modules.allmodules.realtoken as realtoken

def setproject(dbname:str,criteria: FilterCriteria,progress_callback=None):


    current_dir = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = findroot.find_project_root(current_dir)
    DATA_FOLDER = os.path.join(PROJECT_ROOT, "Data")

    db_folder = DATA_FOLDER

    db_name = 'all.db'  # 数据库文件名

    db = insert_db.SQLiteDatabase(db_folder, db_name)
    db.connect()
    token_new = db.readdbtoken()
    tokenreal = realtoken.extract_valid_tokens(token_new,criteria)
    db.close()

    db_folder2 = DATA_FOLDER+'/Project'
    db_name2 = dbname+'.db'  # 数据库文件名
    db = insert_db.SQLiteDatabase(db_folder2, db_name2)
    db.connect()
    db.insert_multiple_tokeninfo(tokenreal)
    db.close()




def setproject_cex(dbname:str,criteria: FilterCriteria,progress_callback=None):


    current_dir = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = findroot.find_project_root(current_dir)
    DATA_FOLDER = os.path.join(PROJECT_ROOT, "Data")

    db_folder = DATA_FOLDER

    db_name = 'all.db'  # 数据库文件名

    db = insert_db.SQLiteDatabase(db_folder, db_name)
    db.connect()
    token_new = db.readdbtoken()
    tokenreal = realtoken.extract_valid_tokens(token_new,criteria)
    db.close()

    db_folder2 = DATA_FOLDER+'/cex'
    db_name2 = dbname+'.db'  # 数据库文件名
    db = insert_db.SQLiteDatabase(db_folder2, db_name2)
    db.connect()
    db.insert_multiple_tokeninfo(tokenreal)
    db.close()












