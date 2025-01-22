
import dexprice.modules.allmodules.refreshmaindb as dexrefreshmaindb
from dexprice.modules.utilis.define import FilterCriteria

def refreshmaindb(db_folder,db_name):
    # we need refresh the whole db
    criteria = FilterCriteria(
        liquidity_usd_min=10000,
        liquidity_usd_max=None,
        fdv_min=10000,
        fdv_max=None,
        pair_age_min_hours=None,
        pair_age_max_hours= None,
        txn_buy=10,
        txn_sell=10,
        volume=10000
       )

    dexrefreshmaindb.refresh_database(db_name, db_folder, criteria)

