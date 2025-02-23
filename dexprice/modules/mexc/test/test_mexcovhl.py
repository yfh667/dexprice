import dexprice.modules.utilis.define as define
import dexprice.modules.mexc.mexcovhl as mexcovhl

import dexprice.modules.utilis.timedefine   as timedefine
#kline_data = mexcovhl.get_kline_data('BTC_USDT', 'Day1', 1740020707, 1740196980,7890)



historydatas = mexcovhl.mexc_token_history('BTC_USDT', 'Day1', 1740020707, 1740196980,7890)

print(historydatas)
