from pymongo import MongoClient
import copy
print('初始化数据mongodb数据库啦...')
client = MongoClient('localhost', 27017)
db = client.test_database
col = db.test_col
post = {
    'name':'lxq',
    'action': 'chifan',

}
for i in range(10):
    col.insert_one(copy.deepcopy(post))
