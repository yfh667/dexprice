import dexprice.modules.utilis.define as define

import dexprice.modules.tg.tgbot as tgbot

def mexctg(tokeninfos:list[define.CexTokenInfo]):
    string = ''
    for tokeninfo in tokeninfos:
        string = string+'\n'+tokeninfo.name
    return string

def mexctg2(chatid,tokeninfos:list[define.CexTokenInfo])  :
    string = mexctg(tokeninfos)
    tgbot.sendmessage_chatid(chatid,string,7890)

def longstring(chatid,string) :
    tgbot.sendmessage_chatid(chatid,string,7890)
