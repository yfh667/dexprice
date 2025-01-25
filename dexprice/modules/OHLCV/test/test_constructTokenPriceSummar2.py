import dexprice.modules.utilis.define as define
import dexprice.modules.OHLCV.constructTokenPriceSummar as constructTokenPriceSummar
import dexprice.modules.stringtime.timestr as timestr



results1 = define.TokenPriceHistory(
    tokenid=1,
    open=1,
    high=2,
    low=0.5,
    close=1.5,
    time='2025-01-25 09:00:00',  # Convert to a datetime object
    volume=16.893328525477497
)

results2 = define.TokenPriceHistory(
    tokenid=1,
    open=1.5,
    high=1.8,
    low=0.2,
    close=1.7,
    time='2025-01-25 09:05:00',  # Convert to a datetime object
    volume=16.893328525477497
)

results3 = define.TokenPriceHistory(
    tokenid=1,
    open=1.7,
    high=1.8,
    low=0.2,
    close=1.7,
    time='2025-01-25 09:10:00',  # Convert to a datetime object
    volume=16.893328525477497
)

results4 = define.TokenPriceHistory(
    tokenid=1,
    open=1.7,
    high=3,
    low=1.5,
    close=2.5,
    time='2025-01-25 09:15:00',  # Convert to a datetime object
    volume=16.893328525477497
)

results5 = define.TokenPriceHistory(
    tokenid=1,
    open=2.5,
    high=5,
    low=2,
    close=3,
    time='2025-01-25 09:20:00',  # Convert to a datetime object
    volume=16.893328525477497
)
results = [results1, results2,results3,results4,results5]
#
# t = constructTokenPriceSummar.constructTokenPriceSummar(results)
# print(t)

t = constructTokenPriceSummar.mergeTokenHistoryByTimefr(results, '15min')
print(t)

