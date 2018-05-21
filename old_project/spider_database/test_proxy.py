import requests
import copy
import time
import random
import pickle
from os import remove
from PIL import Image
from lxml import html
etree = html.etree
from pymongo import MongoClient
proxies = {
    'http':'111.13.135.153'
}
url = "https://accounts.douban.com/dataSpider"
headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'user-agent': 'Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50',
    'Host': 'movie.douban.com',
    # 'X-Requested-With': 'XMLHttpRequest'
}
post_data = {
 'Referer':'https://accounts.douban.com/dataSpider',
 'form_email':'tcitds@163.com',
 'form_password':'miniyukou1997',
 'dataSpider':'登录',
 'redir':'https://movie.douban.com/',
 'source': 'None'
}
session = requests.session()

test_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
    'Upgrade-Insecure-Requests': '1',
    'Host': 'movie.douban.com'
}
test_url = 'https://movie.douban.com/subject/1291561/comments?start=0&limit=20&sort=new_score&status=P&percent_type='
rs = requests.get(url=test_url, headers=test_headers, proxies=proxies,allow_redirects=False)
if(rs.status_code!=200):
    print('访问失败')
    exit()
html = etree.HTML(rs.text)

from_movie = html.xpath('//div[@id="content"]/h1/text()')[0].replace(' 短评','')

comment_items = html.xpath('//div[@class="comment-item"]')
print(type(comment_items))
print(len(comment_items))

for item in comment_items:
    # print(etree.tostring(i))
    item = copy.deepcopy(item)
    user_name = item.xpath('//div[@class="comment-item"]/div[@class="avatar"]/a/@title')[0]
    user_page = item.xpath('//div[@class="comment-item"]/div[@class="avatar"]/a/@href')[0]
    user_avator = item.xpath('//div[@class="comment-item"]/div[@class="avatar"]/a/img/@src')[0].replace('/u','/ul')
    from_movie  = from_movie
    print(user_name, user_avator, user_page, from_movie)