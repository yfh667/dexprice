import dexprice.modules.utilis.define as define
import dexprice.modules.stringtime.timestr as timestr
# we got the big to small
def constructTokenPriceSummar(tokenhistorys: list[define.TokenPriceHistory]):
    open = tokenhistorys[0].open
    close = tokenhistorys[-1].close
    high = tokenhistorys[0].high
    low = tokenhistorys[0].low
    time = tokenhistorys[0].time
    for tokenhistory in tokenhistorys:
        if tokenhistory.high > high:
            high = tokenhistory.high
        if tokenhistory.low < low:
            low = tokenhistory.low

    realtokenhistory = define.TokenPriceHistory(

        tokenid=tokenhistorys[0].tokenid,
        open=open,
        high=high,
        low=low,
        close=close,
        time=time,  # Convert to a datetime object
        volume=0
    )
    return realtokenhistory


##

def mergeTokenHistoryByTimefr(tokenhistorys: list[define.TokenPriceHistory],klinetype):

    startidx=0
    endidx=0
    newtokenhistorys = []
    while(len(tokenhistorys)-1 >= startidx):

        start = tokenhistorys[startidx].time
        starttime =timestr.time_start(start,klinetype)
        endidx = startidx
        timestart =  startidx
        for tokenhistory in tokenhistorys[timestart+1:]:
            if(timestr.if_kline(starttime, tokenhistory.time, klinetype)):
                endidx = endidx+1
            else:
                break
        if(startidx == endidx):
            tokenhistorys_tmp = []
            tokenhistorys_tmp.append(tokenhistorys[startidx])

            newtokenhistory= constructTokenPriceSummar(tokenhistorys_tmp)
            newtokenhistorys.append(newtokenhistory)

            startidx = startidx + 1


        else:
            tokenhistorys_tmp = tokenhistorys[timestart:endidx+1]
            newtokenhistory=constructTokenPriceSummar(tokenhistorys_tmp)
            newtokenhistorys.append(newtokenhistory)

            startidx = endidx+1

    return newtokenhistorys


