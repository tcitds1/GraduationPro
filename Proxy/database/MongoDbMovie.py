from pymongo import MongoClient

class MongoDbMovie(object):

    def __init__(self, host, port):
        self.client = MongoClient(host, port)
        self.db = self.client.douban
        self.name = 'movie'

    def changeTable(self, name):
        self.name = name

    def get(self, title):
        data = self.db[self.name].find_one({'movie_title': title})
        return data if data != None else None

    def put(self, data_dict):
        if self.db[self.name].find_one({'movie_url': data_dict['movie_url']}):
            return None
        else:
            self.db[self.name].insert(data_dict)
        # 删除某个ip

    def delete(self, url):
        self.db[self.name].remove({'movie_url': url})

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

    def exists(self, url):
        return True if self.db[self.name].find_one({'movie_url': url}) != None else False

    def getNumber(self):
        return self.db[self.name].count()


    def backUp(self, col_name, skipcount,limitcount):
        if(limitcount):
            data = list(self.db[self.name].find().skip(skipcount).limit(limitcount))
        else:
            data = list(self.db[self.name].find())
        self.changeTable(col_name)
        for item in data:
            self.put(item)

    def pop(self):
        # 随机从数据库中取出一个
        data = list(self.db[self.name].aggregate([{'$sample': {'size': 1}}]))
        if data:
            data = data[0]
            url = data['movie_url']
            self.delete(url)
            return data
        return None
    def quchong(self):

        # data = list(self.db[self.name].aggregate([{'$sample': {'size': 1}}]))
        pipeline = [
            {"$group": {"_id": "$movie_url", "count": {"$sum": 1}}},
            {"$match": {"count": {"$gt":1}}}
        ]

        data  = self.db[self.name].aggregate(pipeline)

        for item in list(data):
            print(item)
            count = item['count']
            print(item['_id']+'去重')
            for i in range(1, count):
                self.db[self.name].remove({'movie_url':item['_id']},0)

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

    # update数据
    # client.backUp("movie_backup",0,5)
    # client.changeTable('movie_backup')
    # client.db[client.name].update_one({"movie_title":"七宗罪"},{'$inc': {'x': 3}})

    # 无论前后都是先skip再limit
    # client.changeTable('movie_backup')
    # data1 = client.db[client.name].find().skip(40).limit(5)
    # data2 = client.db[client.name].find().limit(5).skip(40)
    # for i in list(data1):
    #     print(i)
    # for i in list(data2):
    #     print(i)


    # client.changeTable('movie_backup')
    # client.quchong()

    # print(client.exists('肖申克的救赎'))

    # client.put({'title':'ywx', 'id': 1234})