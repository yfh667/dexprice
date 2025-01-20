
import dexprice.modules.utilis.define as define





def deadallday(tokenprices:list[define.TokenPriceHistory]):
    for tokenprice in tokenprices:
          # 在这里编写逻辑处理 tokenprice
          if not (0.5 * tokenprice.open < tokenprice.close < 1.5 * tokenprice.open):
              return 0  # Return 0 if condition is met


    return 1



