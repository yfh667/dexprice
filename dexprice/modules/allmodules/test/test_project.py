import dexprice.modules.allmodules.project as project
from dexprice.modules.utilis.define import FilterCriteria

if __name__ == "__main__":
    criteria = FilterCriteria(
        liquidity_usd_min=100000,
        liquidity_usd_max=None,
        fdv_min=100000,
        fdv_max=None,
        pair_age_min_hours=None,
        pair_age_max_hours= None
    )
    project.setproject_linshi('test222',criteria)
