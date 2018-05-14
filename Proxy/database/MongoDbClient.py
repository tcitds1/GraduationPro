from pymongo import  MongoClient
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
    def put(self, proxy, num=1):
        if self.db[self.name].find_one({'proxy': proxy}):
            return None
        else:
            self.db[self.name].insert({'proxy': proxy, 'num': num})

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
            return {'proxy': value, 'value': data['num']}
        return None

    # 取所有
    def getAll(self):
        return {p['proxy']: p['num'] for p in self.db[self.name].find()}

    # 删库跑路
    def clean(self):
        self.client.drop_database('proxy')

    # 删除集合里面所有数据
    def delete_all(self):
        self.db[self.name].remove()


    def update(self, key, value):
        self.db[self.name].update({'proxy': key}, {'$inc': {'num': value}})

    # 看是否存在某数据
    def exists(self, key):
        return True if self.db[self.name].find_one({'proxy': key}) != None else False

    # 获取数据量
    def getNumber(self):
        return self.db[self.name].count()

if __name__ == '__main__':
    client = MongoClient('localhost', 27017)
    db = client.proxy
    db['useful_proxy'].insert_one({'proxy':'1.1.1.1:8888', 'num': 1})

