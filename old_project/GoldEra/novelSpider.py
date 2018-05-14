import requests
def index_spider():
    rs = requests.get('http://www.kanunu8.com/book3/7065/index.html')
    print(rs.encoding)
    rs.encoding = 'gb2312'
    print(rs.text)
index_spider()