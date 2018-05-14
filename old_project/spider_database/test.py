from pymongo import MongoClient
client = MongoClient()
db = client.test_database
col = db.user_col
one = list(col.aggregate([{'$sample': {'size': 1}}]))
print(one)