

import modules.strategy.strategy1 as strategy1
import modules.utilis.define as define

if __name__ == '__main__':

    # 示例数据
    data = [
        define.TokenPriceHistory(tokenid=1, open=2.362e-05, high=2.883e-05, low=2.204e-05, close='2.362e-05', time='2024-11-02 04:00:00', volume=0),
        define.TokenPriceHistory(tokenid=1, open=2.883e-05, high=3.000e-05, low=2.500e-05, close='2.883e-05', time='2024-11-02 05:00:00', volume=0),
        define.TokenPriceHistory(tokenid=1, open=2.204e-05, high=2.500e-05, low=2.100e-05, close='2.204e-05', time='2024-11-02 06:00:00', volume=0),
        define.TokenPriceHistory(tokenid=1, open=2.362e-05, high=2.600e-05, low=2.300e-05, close='2.362e-05', time='2024-11-02 07:00:00', volume=0)
    ]
    # 调用 simple 函数并传递数据
    strategy1.simple(data)

