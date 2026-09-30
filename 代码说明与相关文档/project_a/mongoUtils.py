from pymongo import MongoClient
from datetime import datetime
import conf


#mongodb操作
#插入数据
def insertData(roomid, msg):
    client = MongoClient(conf.dburl)
    db = client.fiveseven
    db[roomid].insert({'msg': msg, 'utcTime': datetime.utcnow()})


#查询数据
def query(roomid):
    client = MongoClient(conf.dburl)
    db = client.fiveseven
    bulletScreen = db[roomid]
    msg_data = bulletScreen.find().sort("utcTime", -1).limit(50)
    datalist = []
    for x in msg_data:
        datalist.append(x['msg'])
    return datalist


#判断数据是否已存在
def exists(roomid, msg):
    client = MongoClient(conf.dburl)
    db = client.fiveseven
    bulletScreen = db[roomid]
    res = bulletScreen.find({'msg': msg})
    reslist = list(res)
    if len(reslist) != 0:
        return True
    return False
