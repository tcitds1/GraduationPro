from pymongo import MongoClient
from multiprocessing import Process,Manager,Queue

import time
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
            return True

        # 删除某个ip

    def delete(self, user_page):
        self.db[self.name].remove({'user_page': user_page})

    def pop(self):
        # 随机从数据库中取出一个
        data = list(self.db[self.name].aggregate([{'$sample': {'size': 1}}]))
        if data:
            data = data[0]
            self.delete(data['user_page'])
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

    # 看是否存在某数据 根据用户url来，因为用户url是独一无二的
    def exists(self, user_page):
        return True if self.db[self.name].find_one({'user_page': user_page}) != None else False

    def getNumber(self):
        return self.db[self.name].count()

    def update_one(self, user_page, dict):
        self.db[self.name].update_one({"user_page": user_page}, {'$set': dict})

    def backUp(self, col_name, skipcount,limitcount):
        if(limitcount):
            data = list(self.db[self.name].find().skip(skipcount).limit(limitcount))
        else:
            data = list(self.db[self.name].find())
        self.changeTable(col_name)
        for item in data:
            self.put(item)

    # def getProxyDbState(self, name):
    #     methods_dic = GetFreeProxy.getProxyMethods()
    #     dbStatus_dic = dict()
    #     for key in methods_dic:
    #         count = self.db[name].find({'from': key}).count()
    #         dbStatus_dic[methods_dic[key]] = count
    #         if (name == 'raw_proxy' and count == 0):
    #             return 0
    #     return dbStatus_dic

# def popdata(queue):
#     while queue.qsize():
#         queue.get()
#
#
# def startA(msgQueue):
#     while msgQueue.qsize():
#         msgQueue.get()

# 第一次用户筛选60156个数据

if __name__ == '__main__':
    client = MongoDb('localhost', 27017, 'douban')
    client.backUp('user_test1',0,100)

    # 队列的使用  当数据库太大了的时候 会发生错误
    # queue = Queue()
    # for i in range(100):
    #     queue.put(i)
    # p1 = list()
    # for i in range(5):
    #     Proc = Process(target=startA, args=(queue,))
    #     p1.append(Proc)
    # for i in p1:
    #     i.daemon = True
    #     i.start()
    # for i in p1:
    #     i.join()

    # 用户数据备份
    # start = time.time()
    # data = client.getAll()
    # client.changeTable('user_backup')
    # client.db[client.name].insert_many(data)
    # p1 = list()
    #
    # for i in range(5):
    #     Prod = Process(target=popdata, args=(queue,))
    #     p1.append(Prod)

        # MSG_QUEUE = Queue(5)
        #
        # processA = Process(target=startA, args=(MSG_QUEUE,))
        # processB = Process(target=startA, args=(MSG_QUEUE,))
        #
        # processA.start()
        # print('processA start..')
        #
        # processB.start()
        # print('processB start..')



    #
    # print((time.time()-start))



        # print(item)
    # print(count)
    # inter = time.time() - start
    # print(inter)
    # print(client.exists('https://www.douban.com/people/fish6058/'))
    # client.put({'user_name':'ywx', 'id': 1234})