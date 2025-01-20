
from dexprice.modules.utilis.define  import TokenInfo,FilterCriteria
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

def normal_token_filter(token_info: TokenInfo, criteria: FilterCriteria) -> bool:
    """
    根据 FilterCriteria 中的条件过滤 TokenInfo 对象。

    :param token_info: 要过滤的 TokenInfo 对象。
    :param criteria: 包含筛选条件的 FilterCriteria 对象。
    :return: 满足所有条件则返回 True，否则返回 False。
    """
    # 计算配对的年龄（小时）
    if token_info.creattime:
        pair_age_hours = (datetime.now() - datetime.fromisoformat(token_info.creattime)).total_seconds() / 3600
    else:
        pair_age_hours = None

    # 检查流动性
    if criteria.liquidity_usd_min is not None and token_info.liquidity_usd < criteria.liquidity_usd_min:
        return False
    if criteria.liquidity_usd_max is not None and token_info.liquidity_usd > criteria.liquidity_usd_max:
        return False

    # 检查 FDV
    if criteria.fdv_min is not None and token_info.fdv < criteria.fdv_min:
        return False
    if criteria.fdv_max is not None and token_info.fdv > criteria.fdv_max:
        return False

    # 检查配对年龄
    if pair_age_hours is not None:
        if criteria.pair_age_min_hours is not None and pair_age_hours < criteria.pair_age_min_hours:
            return False
        if criteria.pair_age_max_hours is not None and pair_age_hours > criteria.pair_age_max_hours:
            return False
    #检查购买里
    
    
    
    return True
def liquid_token_filter(TokenInfo:TokenInfo):
    if TokenInfo.liquidity_usd > 1000 and TokenInfo.liquidity_usd > 1000:
        return 1
    else:
        return 0

def fdv_token_filter(TokenInfo):
    if TokenInfo.fdv > 1000 and TokenInfo.fdv < 1000000:
        return 1
    else:
        return 0


def eth_big(TokenInfo):
    #fdv 1000k
    #liquidity_usd 100k
    if TokenInfo.fdv > 1000000 and TokenInfo.liquidity_usd > 100000:
        return 1
    else:
        return 0