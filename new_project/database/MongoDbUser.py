
from pymongo import MongoClient
from multiprocessing import Process,Manager,Queue
import re
import time
class MongoDb(object):
    def __init__(self, host, port, col_name):
        self.client = MongoClient(host, port)
        self.db_name = 'douban'
        self.db = self.client[self.db_name]
        self.name = col_name

    def changeTable(self, name):
        self.name = name


    def get(self, user_name):
        data = self.db[self.name].find_one({'user_name': user_name})
        return data if data != None else None

    def put(self, data_dict):
        if self.db[self.name].find_one({'user_page': data_dict['user_page']}):
            return None
        else:
            self.db[self.name].insert(data_dict)
            return True

    # 删除某个用户
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
        count = 0
        # 第一次用户筛选60156个数据
        # 跳过60156备份用户数据
        if(limitcount):
            data = list(self.db[self.name].find().skip(skipcount).limit(limitcount))
        else:
            data = list(self.db[self.name].find())
        print(len(data))
        self.changeTable(col_name)
        for item in data:
            self.put(item)
            count += 1
            if(count%1000==0):
                print(count)

    def filter_user(self):
        self.changeTable('douban_user')
        unspider_user =  list(self.db[self.name].find({'$or':[{'jointime':None}, {'jointime':'unknow'}]}))
        return unspider_user

    def filter_withcount(self, skipcount, limitcount):
        count = 0;
        unspider_user = self.db[self.name].find({'$or':[{'jointime':None}, {'jointime':'unknow'}]}).skip(skipcount).limit(limitcount)
        for item in unspider_user:
            self.changeTable('douban_user')
            self.delete(item['user_page'])
            self.changeTable('unvisited_user')
            self.put({'user_page':item['user_page']})
            count+=1
            if(count%500==0):
                print(count)

    def fixBug(self):
        self.changeTable('douban_user')
        count = 0
        for item in list(self.db[self.name].find()):
            user_name = item['user_name']
            user_page = item['user_page']
            user_fans = item['user_fans']
            # regular_v7 = re.findall(r"\D", "https://docs.python.org/3/whatsnew/3.6.html")
            if(re.findall(r"\d", user_name)):
                user_count ='^' + re.sub('\D', '', user_name)
                user_fans = re.sub(user_count, '', str(user_fans))
                user_fans = int(user_fans)
                self.update_one(user_page, {'user_fans':user_fans})
                count = count + 1
                if(count%50==0):
                    print(count)

    def backUnspider(self):
        data = self.filter_user()
        self.changeTable('wait_user')
        count = 0
        start = time.time()
        for i in data:
            self.put(i)
            count +=1
            if(count%100==0):
                print(count)
        print(time.time()-start)

    def remove_failuser(self):
        data = list

def run(colname, skip, limit):
    client = MongoDb('localhost', 27017, 'douban_user')
    client.backUp(colname, skip, limit)

def run1(skip, limit):
    client = MongoDb('localhost', 27017, 'douban_user')
    client.filter_withcount(skip, limit)


def main(run_name):
    # 需要修改的三个参数
    # 从哪里取出来 在run1中修改
    # 存入哪里 在analyse里面修改
    # 未成功爬取的存到哪里
    skip = 0
    pl = []
    for i in range(4):
        skipcount = skip + 10000*i
        limit = 10000
        Proc = Process(target=run_name, args=(skipcount, limit))
        pl.append(Proc)

    for item in pl:
        item.daemon = True
        item.start()

    for item in pl:
        item.join()

if __name__ == '__main__':
    # main(run)
    main(run1)

    client = MongoDb('localhost', 27017, 'douban_user')
    # client.filter_withcount(0,1)
    client.fixBug()
    # for i in range(5):
    #     print (i)
    # client.changeTable('unvisited_user')
    # client.update_one('https:wwww.test.com/pepole',{'user_page':'https:wwww.test.com/pepole'})
    #

    # client.backUp('user_backup', None, None)

    # print(len(client.filter_user()))
    # client.fixBug()

    # # 用户数据备份
    # client.backUp('wait_user',0, 10)
    #

    # start = time.time()
    # data = client.getAll()
    # client.changeTable('user_backup')
    # client.db[client.name].insert_many(data)
    # client.backUp('user_test1',0,100)

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