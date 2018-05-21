import requests
import time
import random
import sys
import copy
from lxml import html
etree =html.etree
from login import Spider
sys.path.append('../')
from log.LogHandler import LogHandler
from threading import Thread

class UserSpider(Spider):

    def __init__(self):
        self.log = LogHandler('book_comment')
        Spider.__init__(self)

    def spider_book_comment(self, book_id):
        s = self.session
        self.init_database()
        # url = 'https://book.douban.com/subject/25862578/comments/hot?p=5'
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Host': 'book.douban.com',
            'Referer': 'https://book.douban.com/subject/25862578/comments/hot?p=1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'
        }
        p = 178
        url = 'https://book.douban.com/subject/{}/comments/hot?p=178'.format(book_id)

        # 开始爬取
        self.log.info('--------Get book_comment user Start--------')
        while(True):
            try:
                rs = s.get(url=url, headers=headers)
            except Exception as e:
                self.log(str(e))
                time.sleep(10)
                continue
            if(rs.status_code==200):
                self.log.info('bookUser_Spider: now spidering {} page data'.format(p))
                html_tree = etree.HTML(rs.text)
                self.analyse_page(html_tree,headers['Referer'])
                p = p + 1
                url = 'https://book.douban.com/subject/{}/comments/hot?p={}'.format(book_id, p)
                headers['Referer'] = url
                time.sleep(random.uniform(5,7))
                if(p%17==0):
                    time.sleep(10)
                if(p==5000):
                    break
            else:
                self.log.info('bookUser_Spider: get {} page data error'.format(p))
                break
        self.log.info('--------Get book_comment user End-----------')

    def analyse_page(self,html_tree, referer):
        user_list = list()
        html = html_tree
        # 从哪部电影爬的
        try:
            from_book = html.xpath('//div[@id="content"]/h1/text()')[0].replace(' 短评', '')
            comment_items = html.xpath('//li[@class="comment-item"]')
            # print(from_book)
            # print(type(comment_items))
            # print(len(comment_items))
            for item in comment_items:
                # item = copy.deepcopy(item)
                user_dic = dict()
                user_name = item.xpath('.//div[@class="avatar"]/a/@title')[0]
                user_page = item.xpath('.//div[@class="avatar"]/a/@href')[0]
                user_avator = item.xpath('.//div[@class="avatar"]/a/img/@src')[0].replace('/u','/ul')
                user_comment = item.xpath('.//div[@class="comment"]/p[@class="comment-content"]/text()')[0]
                comment_vote = item.xpath('.//div[@class="comment"]/h3/span[@class="comment-vote"]/span[@class="vote-count"]/text()')[0]
                comment_vote = int(comment_vote)
                user_dic['user_name'] = user_name
                user_dic['user_page'] = user_page
                user_dic['user_avator'] = user_avator
                user_dic['user_comment'] = user_comment
                user_dic['comment_vote'] = comment_vote
                user_dic['from_book'] = from_book
                user_dic['referer'] = referer
                user_list.append(user_dic)
        except:
            self.log.info('-------spider error Interuput------')
            exit()
        if(len(user_list)):
            self.db.changeTable('douban_user')
            for item in user_list:
                self.db.put(item)

if __name__ == '__main__':
    us = UserSpider()
    if(us.__login__()):
        us.spider_book_comment(25862578)
    # # print(us.name)
    # print(us.headers)
