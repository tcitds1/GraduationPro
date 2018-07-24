
from pymongo import MongoClient
from multiprocessing import Process,Manager,Queue
import re
import pymongo
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
        data = list(self.db[self.name].find())
        for item in data:
            user_name = item['user_name']
            user_page = item['user_page']
            user_fans = item['user_fans']
            # regular_v7 = re.findall(r"\D", "https://docs.python.org/3/whatsnew/3.6.html")
            if(re.findall(r"\d", user_name)):
                try:
                    user_count ='^' + str(int(re.sub('\D', '', user_name)))
                except:
                    continue
                user_fans = re.sub(user_count, '', str(user_fans))
                try:
                    user_fans = int(user_fans)
                except:
                    continue
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

    def minifyUser(self, skip, limit):
        dic = "河北山西内蒙古辽宁吉林黑龙江江苏浙江安徽福建江西山东河南湖北湖南广东广西海南四川贵州云南西藏陕西甘肃青海宁夏新疆"
        # dic = {'河北': '1', '山西': '1', '内蒙古': '1', '辽宁': '1',
        #         '吉林': '1', '黑龙江': '1', '江苏': '1', '浙江': '1', '安徽': '1',
        #         '福建': '1', '江西': '1', '山东': '1', '河南': '1', '湖北': '1', '湖南': '1',
        #         '广东': '1', '广西': '1', '海南': '1', '四川': '1', '贵州': '1',
        #          '云南': '1', '西藏': '1', '陕西': '1', '甘肃': '1', '青海': '1', '宁夏': '1', '新疆': '1'}

        data = self.db[self.name].find().skip(skip).limit(limit)
        data = list(data)
        count = skip

        for item in data:
            area1 = ''
            area2 = ''
            area = item['user_location']
            count += 1
            if (count % 500 == 0):
                print(count)
            if(re.findall('[a-z]',area)):
                continue
            area1 = area[:2]
            area2 = area[:3]

            if(dic.find(area1)):
                self.update_one(item['user_page'],{'user_location':area1})
                continue
            if(dic.find(area2)):
                self.update_one(item['user_page'],{'user_location':area2})
                continue




    def dataHandle(self):
        self.changeTable('douban_user')
        data = self.db[self.name].find().sort('user_fans',pymongo.DESCENDING).limit(20)
        data = list(data)
        for item in data:
            print(item)

    def datahandle_area(self):
        pipeline = [
            {'$group': {'_id': '$user_location', "count": {'$sum': 1}}},
            {'$sort': {'count': -1}},
            {'$limit': 40}
        ]
        data = self.db[self.name].aggregate(pipeline)
        data = list(data)
        for item in data:
            print(item)

    def datahandle_waiguo(self):
        arry = ['北京', '上海','重庆','天津','香港','河北', '山西', '内蒙古', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南', '广东', '广西',
               '海南', '四川', '贵州', '云南', '西藏', '陕西', '甘肃', '青海', '宁夏', '新疆']
        pipeline = [
            {'$match':{'user_location':{'$nin':arry}}},
            {'$group': {'_id': '$user_location', "count": {'$sum': 1}}},
            {'$sort': {'count': -1}},
            {'$limit': 40}
        ]
        data = self.db[self.name].aggregate(pipeline)
        data = list(data)
        for item in data:
            print(item)


def run(colname, skip, limit):
    client = MongoDb('localhost', 27017, 'douban_user')
    client.backUp(colname, skip, limit)

def run1(skip, limit):
    client = MongoDb('localhost', 27017, 'douban_user')
    client.filter_withcount(skip, limit)

def run2(skip, limit):
    client = MongoDb('localhost', 27017, 'douban_user')
    client.minifyUser(skip, limit)


def main(run_name):
    # 需要修改的三个参数
    # 从哪里取出来 在run1中修改
    # 存入哪里 在analyse里面修改
    # 未成功爬取的存到哪里
    skip = 0
    pl = []
    for i in range(5):
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
    # main(run2)
    client = MongoDb('localhost', 27017, 'douban_user')
    client.backUp('user_test')
    # data = client.db[client.name].find({'user_location':'黑龙'})
    # data = list(data)
    # for item in data:
    #     client.update_one(item['user_page'], {'user_location':'黑龙江'})
    # # client.datahandle_area()
    # client.dataHandle()
    # client.fixBug()
    # client.filter_withcount(0,1)
    # client.fixBug()
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