import dexprice.modules.allmodules.project as project
from modules.utilis.define import FilterCriteria

if __name__ == "__main__":
    criteria = FilterCriteria(
        liquidity_usd_min=1000,
        liquidity_usd_max=None,
        fdv_min=100000,
        fdv_max=500000,
        pair_age_min_hours=None,
        pair_age_max_hours= None
    )
    project.setproject('solana','solana_500kbelow',criteria)
