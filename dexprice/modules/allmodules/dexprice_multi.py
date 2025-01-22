from dexprice.modules.utilis.define import FilterCriteria
import dexprice.modules.PriceMonitor.tokenflitter as tokenflitter
import dexprice.modules.proxy.proxymultitheread as proxymultitheread
import dexprice.modules.PriceMonitor.dexscreen_parrel as dexscreen_parrel
import dexprice.modules.utilis.define as define
import dexprice.modules.db.insert_db as insert_db
import os
import dexprice.modules.utilis.findroot as findroot


def dexprice_multi_fordb_token(chain_addresses,criteria):
    tokenreal = []
    for chain, pairaddresses in chain_addresses.items():
        print(f"we check Chain: {chain} ")
        rate = 5
        capacity = 300
        chainid = chain
        sourcetype = define.Config.DEXS
        max_threads_per_proxy = 2
        clash_api_url = "http://127.0.0.1:9097"
        headers = {"Authorization": "Bearer 123"}
        startport = 50000
        proxys = proxymultitheread.get_one_ip_proxy_multithread(startport, clash_api_url, headers)
        task_manager = dexscreen_parrel.TaskManager(pairaddresses, sourcetype, chainid, proxys, rate, capacity,
                                                    max_threads_per_proxy, 'refresh ' + chainid)
        tokensinfo, failed_tasks = task_manager.run()
        for token in tokensinfo:
            if (tokenflitter.normal_token_filter(token, criteria)):
                if (token.creattime == '1970-01-01 00:00:00'):
                    pass
                else:
                    tokenreal.append(token)
    return tokenreal