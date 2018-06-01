import sys
from pymongo import MongoClient
try:
    from FreeProxy.getFreeProxy import GetFreeProxy
except ModuleNotFoundError as e:
    sys.path.append('../')
    from FreeProxy.getFreeProxy import GetFreeProxy

class MongoDbClient(object):

    def __init__(self, host, port):
        self.name = 'raw_proxy'
        self.client = MongoClient(host, port)
        self.db = self.client.proxy

    def changeTable(self, name):
        self.name = name

    # 看某个ip的状态
    def get(self, proxy):
        data = self.db[self.name].find_one({'proxy': proxy})
        return data['num'] if data != None else None

    # 存入ip
    def put(self, proxy,from_method,num=1):
        if self.db[self.name].find_one({'proxy': proxy}):
            return None
        else:
            if from_method:
                pass
            else:
               from_method = 'unknow'
            self.db[self.name].insert({'proxy': proxy, 'from':from_method,'num': num})


    # 删除某个ip
    def delete(self, proxy):
        self.db[self.name].remove({'proxy': proxy})

    def pop(self):
        # 随机从数据库中取出一个
        data = list(self.db[self.name].aggregate([{'$sample': {'size': 1}}]))
        if data:
            data = data[0]
            value = data['proxy']
            self.delete(value)
            return {'proxy': value, 'value': data['num'], 'from':data['from']}
        return None

    # 取所有
    def getAll(self):
        return {p['proxy']: p['num'] for p in self.db[self.name].find()}

    def showAll(self):
        proxies =  list(self.db[self.name].find())
        for item in proxies:
            del item['_id']
        return proxies
    # 删库跑路
    def clean(self):
        self.client.drop_database('proxy')

    # 删除集合里面所有数据
    def deleteAll(self):
        self.db[self.name].remove()


    def update(self, key, num=1):
        self.db[self.name].update({'proxy': key}, {'$set': {'num': num}})

    # 看是否存在某数据
    def exists(self, key):
        return True if self.db[self.name].find_one({'proxy': key}) != None else False

    # 获取数据量
    def getNumber(self):
        return self.db[self.name].count()

    def getProxyDbState(self, name):
        methods_dic = GetFreeProxy.getProxyMethods()
        dbStatus_dic = dict()
        for key in methods_dic:
            count = self.db[name].find({'from':key}).count()
            dbStatus_dic[methods_dic[key]] = count
            if(name=='raw_proxy' and count==0):
                return 0
        return dbStatus_dic

if __name__ == '__main__':
    clientdb = MongoDbClient('localhost', 27017)
    print(clientdb.showAll())
    # print(clientdb.getProxyDbState('raw_proxy'))