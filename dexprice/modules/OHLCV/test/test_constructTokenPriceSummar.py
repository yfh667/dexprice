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

results = [results1, results2]

t = constructTokenPriceSummar.constructTokenPriceSummar(results)
print(t)


