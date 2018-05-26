import json
import re
import requests
import time
import random
import sys
import copy
from datetime import datetime
from lxml import etree
# from login import Spider
from WebRequests import WebRequests
from multiprocessing import Process
sys.path.append('../')
from log.LogHandler import LogHandler
from database.MongoDbUser import MongoDb
from database.MongoDbMovie import MongoDbMovie
import queue

from threading import Thread

class UserSpider():

    def __init__(self):
        self.log = LogHandler('getUerUrl',file=False)
        self.db = MongoDb('localhost', 27017, 'douban')
        self.webRequests = WebRequests()
        # self.webRequests.init_UserRequest()
        self.get = self.webRequests.sendRequest
        self.change_proxy = self.webRequests.change_proxy

    def spider_book_comment(self, book_id):
        # url = 'https://book.douban.com/subject/25862578/comments/hot?p=5'
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Host': 'book.douban.com',
            'Referer': 'https://book.douban.com/subject/25862578/comments/hot?p=1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'
        }
        p = 722
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
                time.sleep(random.uniform(2,5))
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

    # def spider_movie_comment(self, movie_id):
    #     data = {
    #         "_id": ObjectId("5afc634245cc4932b407bbf7"),
    #         "user_name": "失控芭乐",
    #         "user_page": "https://www.douban.com/people/fish6058/",
    #         "user_avator": "https://img1.doubanio.com/icon/ul1389804-18.jpg",
    #         "user_comment": "真的要到很久以后，才会明白，每一个选择只要努力过，都是正确的选择。",
    #         "comment_vote": 12570,
    #         "referer": "https://book.douban.com/subject/25862578/comments/hot?p=1",
    #         "from": "解忧杂货店"
    #     }
    #
    #
    #     headers = {
    #         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    #         'Accept-Encoding': 'gzip, deflate, br',
    #         'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    #         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    #         'Host': 'movie.douban.com',
    #         'Upgrade-Insecure-Requests': '1',
    #     }
    #     s = self.session
    #     start = 0
    #     page = 1
    #     # 'https://movie.douban.com/subject/1291561/comments?start=0&limit=20&sort=new_score&status=P&percent_type='
    #     url_hot = 'https://movie.douban.com/subject/{}/comments?start={}&limit=20&sort=new_score&status=P&percent_type='.format(movie_id, start)
    #     url_new = 'https://movie.douban.com/subject/{}/comments?start={}&limit=20&sort=time&status=P&percent_type='.format(movie_id, start)
    #     while(True):
    #         response = s.get(url=url_hot, headers=headers)
    #         if(response.status_code == 200):
    #             self.analysis_page(response.text, page)
    #             print('当前已访问第{}页  {}'.format(page, time.asctime(time.localtime(time.time()))))
    #             time.sleep(random.uniform(5,6))
    #             start = start + 20
    #             page = page + 1
    #             url_hot = 'https://movie.douban.com/subject/{}/comments?start={}&limit=20&sort=new_score&status=P&percent_type='.format(movie_id,start)
    #             headers['Referer'] = url_hot
    #             if(start == 500):
    #                 print('热门评论已爬取完毕')
    #                 break;
    #         else:
    #             print('访问电影第{}页失败'.format(page))
    #             break
    def spider_movie_comment(self, movie_id):
        self.log.info('UserSpider : {}--电影[{}]-------开始爬取-----------'.format(time.ctime(), movie_id))
        # 从热门评论获取用户的url
        start = 0
        url_hot_raw = 'https://movie.douban.com/subject/{}/comments?start={}&limit=20&sort=new_score&status=P&percent_type='
        url_hot = url_hot_raw.format(movie_id, start)
        while(True):
            while True:
                response = self.get(url_hot)
                if(response):
                    break
                self.change_proxy()

            if response == 'next':
                start = start + 20
                url_hot = url_hot_raw.format(movie_id, start)
                if (start == 220):
                    break
                continue

            self.analyse_movie_page(response, start, url_hot, '热门')
            start = start + 20
            url_hot = url_hot_raw.format(movie_id,start)

            # time.sleep(1)
            # 未登录用户数据 只能访问到220页
            if(start == 220):
                break

        # 从最新评论获取用户的url
        start = 0
        url_new_raw = 'https://movie.douban.com/subject/{}/comments?start={}&limit=20&sort=time&status=P&percent_type='
        url_new = url_new_raw.format(movie_id, start)
        while(True):
            while True:
                response = self.get(url_new)
                if(response):
                    break
                self.change_proxy()

            if response=='next':
                start = start + 20
                if (start == 100):
                    break
                url_new = url_new_raw.format(movie_id, start)
                continue

            self.analyse_movie_page(response, start, url_new, '最新')
            start = start + 20
            url_new = url_new_raw.format(movie_id,start)
            if(start == 100):
                break
            #
            # time.sleep(1)

        self.log.info('UserSpider : {}--电影[{}]-------爬取结束-----------'.format(time.ctime(), movie_id))

    def analyse_movie_page(self, response, start, url, marks):
        user_list = []
        count = 0
        text = response.text
        html = etree.HTML(text)
        try:
        # 从哪部电影爬的
            from_ = html.xpath('//div[@id="content"]/h1/text()')[0].replace(' 短评', '')
            comment_items = html.xpath('//div[@class="comment-item"]')
            for item in comment_items:
                user_dic = {}
                user_page = item.xpath('.//div[@class="avatar"]/a/@href')[0]
                user_name = item.xpath('.//div[@class="avatar"]/a/@title')[0]
                user_avator = item.xpath('.//div[@class="avatar"]/a/img/@src')[0].replace('/u', '/ul')

                user_comment = item.xpath('.//div[@class="comment"]/p/text()')[0].replace(' ','')
                comment_vote = item.xpath('.//div[@class="comment"]/h3/span[@class="comment-vote"]/span[@class="votes"]/text()')[0]
                comment_vote = int(comment_vote)

                user_dic['user_name'] = user_name
                user_dic['user_page'] = user_page
                user_dic['user_avator'] = user_avator
                user_dic['user_comment'] = user_comment
                user_dic['comment_vote'] = comment_vote
                user_dic['referer'] = url
                user_dic['from_'] = from_
                # print(user_dic)
                # exit()
                user_list.append(user_dic)

            for user in user_list:
                result = self.db.put(user)
                if(result):
                    count+=1
            start = int(start/20)
            self.log.info('UserSpider : {}--{}-{}评论-第{}页数据已爬取，存入{}条用户数据----'.format(time.ctime(), from_, marks ,start, count))

        except Exception as e:
            self.log.info('UserSpider : {}--{}--analysis error----'.format(time.ctime(), url))
            print(e)

    def analyse_user_page(self, url):

        while True:
            response = self.get(url)
            if(response):
                break
            self.change_proxy()
        if(response=='next'):
            return

        html_tree = etree.HTML(response.text)

        try:
            user_intro = html_tree.xpath('//div[@id="display"]/text()')[0]
        except:
            user_intro = ''
        # 'https://www.douban.com/people/yinxiang/'
        # 'href="https://movie.douban.com/people/yinxiang/collect"'
        raw_str = url.replace('https://www.douban.com/','')
        try:
            movie_url = 'https://movie.douban.com/' + raw_str + 'collect'
            user_movie = html_tree.xpath('//a[@href="{}"]/text()'.format(movie_url))[0].replace('部看过', '')
            user_movie = int(user_movie)
        except:
            user_movie = 0

        try:
            music_url = 'https://music.douban.com/' + raw_str + 'collect'
            user_music = html_tree.xpath('//a[@href="{}"]/text()'.format(music_url))[0].replace('张听过', '')
            user_music = int(user_music)
        except:
            user_music = 0

        try:
            book_url = 'https://book.douban.com/' + raw_str + 'collect'
            user_book = html_tree.xpath('//a[@href="{}"]/text()'.format(book_url))[0].replace('本读过', '')
            user_book = int(user_book)
        except:
            user_book = 0

        try:
            user_game = html_tree.xpath('//a[@href="games?action=collect"]/text()')[0].replace('玩过','')
            user_game = int(user_game)
        except:
            user_game = 0

        try:
            user_location_detail = html_tree.xpath('//div[@class="user-info"]/a/text()')[0]
            location_arr = user_location_detail.split(',')
            user_location = location_arr[-1::][0]
        except:
            user_location_detail = 'unknow'
            user_location = 'unknow'
        try:
            regex = r"(?<=<br/> ).*?(?=加入)"
            jointime = re.findall(regex, response.text)[0]
            time_arr = jointime.split('-')
            jointime = datetime(int(time_arr[0]), int(time_arr[1]), int(time_arr[2]))
        except:
            jointime = 'unknow'
        # 'https://www.douban.com/people/xingshuiqy/rev_contacts'

        try:
            fans_url = url+'rev_contacts'
            user_fans = html_tree.xpath('//a[@href="{}"]/text()'.format(fans_url))[0]
            user_fans = re.sub('\D', '', user_fans)
            user_fans = int(user_fans)
        except:
            user_fans = 0

        dic = {}

        dic['user_intro'] = user_intro
        dic['user_location_detail'] = user_location_detail
        dic['user_location'] = user_location
        dic['jointime'] = jointime
        dic['user_fans'] = user_fans
        dic['user_movie'] = user_movie
        dic['user_music'] = user_music
        dic['user_book'] = user_book
        dic['user_game'] = user_game

        self.db.changeTable('douban_user')
        self.db.update_one(url, dic)
        #
        print(dic)

def run():
    print('进程已开始')
    db = MongoDbMovie('localhost', 27017)
    db.changeTable('movie_backup')
    data = db.pop()
    us = UserSpider()
    while data:
        us.spider_movie_comment(data['movie_id'])
        data = db.pop()
    print('进程已经结束')



def run1():
    # 爬取用户数据进程
    print('爬取用户数据进程已开始')
    us = UserSpider()
    db = MongoDb('localhost', 27017, 'douban')
    db.changeTable('user_backup')
    data = db.pop()
    while data:
        us.analyse_user_page(data['user_page'])
        data = db.pop()

def main():

    pl = []
    for i in range(20):
        Proc = Process(target=run)
        pl.append(Proc)

    for item in pl:
        item.daemon = True
        item.start()

    for item in pl:
        item.join()
if __name__ == '__main__':
    run1()
    # main()
    # us = UserSpider()
    # url1 = 'https://www.douban.com/people/china30s/'
    # url = 'https://www.douban.com/people/vividtime/'
    # while True:
    #     us.db.changeTable('user_test')
    #     data = us.db.pop()
    #     us.analyse_user_page(url)
    # # print(us.name)
    # print(us.headers)
