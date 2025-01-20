
from modules.PriceMonitor.multi_dexscreen_priceapi import DexscreenApiManager  # 导入类

from modules.utilis.define import Config,TokenInfo
from tqdm import tqdm  # 导入 tqdm



from modules.db.create_db import initialize_table
import modules.db.insert_db as insert_db

from modules.PriceMonitor.multi_geck_dexscreen_api import Get_DEX_From_GECK  # 导入类
from modules.PriceMonitor.tokenflitter import liquid_token_filter,fdv_token_filter

import modules.db.readjson as readjson

import dexprice.modules.utilis.define as define

import  modules.OHLCV.coinmarket as coinmarket  # 导入类
# 示例使用



def deadallday(tokenprices:list[define.TokenPriceHistory]):
    for tokenprice in tokenprices:
          # 在这里编写逻辑处理 tokenprice
        if((tokenprice.high-tokenprice.low)/tokenprice.low>0.2):
         #   print(tokenprice.high-tokenprice.low)
        #    print(tokenprice.low)
            return 0

    return 1



