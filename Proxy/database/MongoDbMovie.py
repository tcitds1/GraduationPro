from pymongo import MongoClient

class MongoDbMovie(object):

    def __init__(self, host, port):
        self.client = MongoClient(host, port)
        self.db = self.client.douban
        self.name = 'movie'


    def get(self, title):
        data = self.db[self.name].find_one({'movie_title': title})
        return data if data != None else None

    def put(self, data_dict):
        # if self.db[self.name].find_one({'user_name': data_dict['user_name']}):
        #     return None
        # else:
        self.db[self.name].insert(data_dict)
        # 删除某个ip

    def delete(self, title):
        self.db[self.name].remove({'movie_title': title})

    # 取所有
    def getAll(self):
        return list(self.db[self.name].find())

    def clean(self):
        self.client.drop_database(self.db_name)

    def delete_all(self):
        self.db[self.name].remove()

    def update(self, title, newdata_dic):
        self.db[self.name].update({'movie_title': title}, {'$set': newdata_dic})

    # 看是否存在某数据

    def exists(self, title):
        return True if self.db[self.name].find_one({'movie_title': title}) != None else False

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
    client = MongoDbMovie('localhost', 27017)
    # print(client.exists('肖申克的救赎'))

    # client.put({'title':'ywx', 'id': 1234})