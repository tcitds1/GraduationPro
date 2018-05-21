from pymongo import MongoClient
class MongoDb(object):
    def __init__(self, host, port, db_name):
        self.client = MongoClient(host, port)
        self.db_name = db_name
        self.db = self.client[db_name]
        self.name = 'douban_user'

    def changeTable(self, name):
        self.name = name


    def get(self, user_name):
        data = self.db[self.name].find_one({'user_name': user_name})
        return data if data != None else None

    def put(self, data_dict):
        if self.db[self.name].find_one({'user_name': data_dict['user_name']}):
            return None
        else:
            self.db[self.name].insert(data_dict)

        # 删除某个ip

    def delete(self, user_name):
        self.db[self.name].remove({'user_name': user_name})

    def pop(self):
        # 随机从数据库中取出一个
        data = list(self.db[self.name].aggregate([{'$sample': {'size': 1}}]))
        if data:
            self.delete(data['user_name'])
            return data
        return None

        # 取所有

    def getAll(self):
        return list(self.db[self.name].find())

    def clean(self):
        self.client.drop_database(self.db_name)

    def delete_all(self):
        self.db[self.name].remove()

    def update(self, user_name, newdata_dic):
        self.db[self.name].update({'user_name': user_name}, {'$set': newdata_dic})

    # 看是否存在某数据
    def exists(self, key):
        return True if self.db[self.name].find_one({'user_name': key}) != None else False

    def getNumber(self):
        return self.db[self.name].count()

    # def getProxyDbState(self, name):
    #     methods_dic = GetFreeProxy.getProxyMethods()
    #     dbStatus_dic = dict()
    #     for key in methods_dic:
    #         count = self.db[name].find({'from': key}).count()
    #         dbStatus_dic[methods_dic[key]] = count
    #         if (name == 'raw_proxy' and count == 0):
    #             return 0
    #     return dbStatus_dic
if __name__ == '__main__':
    # db = client.test_database
    client = MongoDb('localhost', 27017, 'douban')
    client.put({'user_name':'ywx', 'id': 1234})