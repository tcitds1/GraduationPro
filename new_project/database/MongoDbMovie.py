from pymongo import MongoClient
import pymongo
from multiprocessing import  Process
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
        # 删除某个数据

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

    def update_one(self, movie_url, dict):
        self.db[self.name].update({"movie_url": movie_url}, {'$set': dict})

    # 看是否存在某数据

    def exists(self, url):
        return True if self.db[self.name].find_one({'movie_url': url}) != None else False

    def getNumber(self):
        return self.db[self.name].count()

    # 数据拷贝,跳过skipcount个数据，再获取limitecount个数据
    def backUp(self, col_name, skipcount,limitcount):
        # 从600开始400 5.26
        # 从1000 开始 2000 6.1
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

    def backupNull(self):
        data = self.db[self.name].find({'year':None})
        self.changeTable('wait_movie')
        for item in list(data):
            self.put(item)

    def dataHandle(self):
        data = self.db[self.name].find(
            {'$and':
                 [
                     {'movie_types':'科幻'},
                     {'movie_types':{'$ne':'动画'}},
                     {'movie_tags':'科幻'},
                     {'movie_tags':{'$nin':['英剧','美剧', '韩剧', '电视剧', '短片']}},
                     {'movie_watched':{'$gt':150000}}]}).sort('movie_rate',pymongo.DESCENDING).limit(20)
        data = list(data)
        for item in data:
            print(item)

    def dataHandle_year(self):
        pipeline = [
            {'$group':{'_id':'$year', "count":{'$sum':1}}},
            {'$sort':{'_id':-1}}
        ]
        data = self.db[self.name].aggregate(pipeline)
        for item in list(data):
            print(item)

    def dataHandle_directors(self):
        pipeline = [
            {'$unwind':'$movie_directors'},
            {'$group': {'_id': '$movie_directors', "average": {'$avg': '$movie_rate'}}},
            {'$sort': {'count': -1}},
            {'$limit':20}
        ]
        data = self.db[self.name].aggregate(pipeline)
        for item in list(data):
            print(item)

    def dataHandle_casts(self):
        pipeline = [
            {'$unwind': '$movie_casts'},
            {'$group': {'_id': '$movie_casts', "count": {'$sum': 1}}},
            {'$sort': {'count': -1}},
            {'$limit': 20}
        ]
        data = self.db[self.name].aggregate(pipeline)
        for item in list(data):
            print(item)

    def dataHandle_country(self):
        pipeline = [
            {'$unwind': '$movie_areas'},
            {'$group': {'_id': '$movie_areas', "count": {'$sum': 1}}},
            {'$sort': {'count': -1}},
            {'$limit': 20}
        ]
        data = self.db[self.name].aggregate(pipeline)
        for item in list(data):
            print(item)

    def dataHandle_shit(self):
        pipeline = [
            {'$match':{'movie_areas': {'$in':['中国大陆', '台湾']},'movie_watched':{'$gt':200000}, 'movie_tags':{'$ne':'电视剧'}}},
            {'$sort': {'movie_rate': -1}},
            {'$limit': 20}
        ]
        data = self.db[self.name].aggregate(pipeline)
        for item in list(data):
            print(item)

    def data_floating(self, skip, limit):
        count = 0
        data = self.db[self.name].find().skip(skip).limit(limit)
        for item in data:
            rate = item['movie_rate']
            movie_rate = float(rate)
            self.update_one(item['movie_url'], {'movie_rate': movie_rate})
            count += 1
            if(count%500==0):
                print(count)

    def filterMovie(self):
        data = self.db[self.name].find({'year': None})
        for item in list(data):
            self.delete()
            self.changeTable('wait_movie')


def run(skip, limit):
    db = MongoDbMovie('localhost', 27017)
    db.data_floating(skip, limit)

def main(run_name):
    # 需要修改的三个参数
    skip = 0
    pl = []
    for i in range(5):
        skipcount = skip + 10000 * i
        limit = 10000
        Proc = Process(target=run_name, args=(skipcount, limit))
        pl.append(Proc)

    for item in pl:
        item.daemon = True
        item.start()

    for item in pl:
        item.join()


if __name__ == '__main__':
    main(run)

    # 检查初始化数据表，很重要
    #
    #
    # db = client.test_database
    client = MongoDbMovie('localhost', 27017)
    client.update_one('https://movie.douban.com/subject/1292402/', {'movie_rate':8.7})

    # 数据分析
    # client.dataHandle_shit() wait
    # client.dataHandle_country()

    # client.dataHandle_directors()

    # client.dataHandle_casts()
    # client.dataHandle_year()
    # client.dataHandle_year()

    # client.backUp('movie_backup', 1000, 2000)

    # client.backUp('movie_backup',600, 400)

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