from dexprice.modules.utilis.define import FilterCriteria
import dexprice.modules.PriceMonitor.tokenflitter as tokenflitter
import dexprice.modules.proxy.proxymultitheread as proxymultitheread
import dexprice.modules.PriceMonitor.dexscreen_parrel as dexscreen_parrel
import dexprice.modules.utilis.define as define
import dexprice.modules.db.insert_db as insert_db
import os
import dexprice.modules.utilis.findroot as findroot
import dexprice.modules.allmodules.realtoken as realtoken
def refreshmaindb():
    # we need refresh the whole db
    criteria = FilterCriteria(
        liquidity_usd_min=1000,
        liquidity_usd_max=None,
        fdv_min=1000,
        fdv_max=None,
        pair_age_min_hours=None,
        pair_age_max_hours= None
    )
    current_dir = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = findroot.find_project_root(current_dir)
    DATA_FOLDER = os.path.join(PROJECT_ROOT, "Data")
    db_folder = DATA_FOLDER
    db_name =   'all.db'  # 数据库文件名
    refresh_database(db_name, db_folder, criteria)



## here we need refresh the database for some criteria
def refresh_database(db_name,db_folder,criteria):
    db = insert_db.SQLiteDatabase(db_folder, db_name)
    db.connect()
    token_new = db.readdbtoken()
    # 初始化字典，用链名作为键，地址列表作为值
    chain_addresses = {
        'solana': [],
        'base': [],
        'ethereum': [],
        'bsc': []
    }
    # we need jilu the raw address
    pair_addresses = []
    # 遍历 token_new，根据链名将地址加入对应的列表
    for token in token_new:
        # 确保 token.chainid 是链名，并存在于字典的键中
        if token.chainid in chain_addresses:
            pair_addresses.append(token.pair_address)

    tokenreal = realtoken.extract_valid_tokens(token_new,criteria)

    realpairaddress = []
    for token in tokenreal:
        realpairaddress.append(token.pair_address)

    missing_addresses = set(pair_addresses) - set(realpairaddress)
    # 输出结果
    print("在 paireaddress 中存在但不在 realpairaddress 中的地址：")
    for address in missing_addresses:
        db.delete_token(address)
        print(address)

    db.close()
    return tokenreal



