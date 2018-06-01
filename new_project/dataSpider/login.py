import requests
import pickle
import time
import random
import sys
from os import remove
from PIL import Image
from lxml import html
import copy
etree = html.etree
from pymongo import MongoClient
sys.path.append('../')
from database.MongoDbUser import MongoDb
class Spider():
    def __init__(self):
        self.login_url = 'https://accounts.douban.com/login'
        self.movie_comments_url = 'https://movie.douban.com/subject/4920389/comments?start=0&limit=20&sort=new_score&status=P&percent_type='
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
            'Upgrade-Insecure-Requests': '1',
            'Host': 'accounts.douban.com',
        }
        self.login_data = {
         'Referer':'https://accounts.douban.com/dataSpider',
         'form_email':'tcitds@163.com',
         'form_password':'miniyukou',
         'dataSpider':'登录',
         'redir':'https://movie.douban.com/',
         'source': 'None'
        }
        self.session = requests.session()
        self.cookies = ''

    def init_database(self):
        print('初始化数据mongodb数据库啦...')
        self.db = MongoDb('localhost', 27017, 'douban')

    def login(self):
        print('---正在使用账号密码登录---')
        s = self.session
        rsponse = s.get(url=self.login_url, headers=self.headers)
        if(rsponse.status_code != 200):
            print('访问登录页面受限')
            exit(0)
        login_html = etree.HTML(rsponse.text)
        captcha_img = login_html.xpath('//img[@class="captcha_image"]')
        #判断是否需要验证码
        if (len(captcha_img) == 0):
            s.post(url=self.login_url, headers=self.headers, data=self.login_data)
        else:
            captcha_id, captcha_solution = self.get_captcha(login_html)
            login_data = self.login_data.copy()
            login_data['captcha-solution'] = captcha_solution
            login_data['captcha-id'] = captcha_id
            rs = s.post(url=self.login_url, headers=self.headers, data=login_data)
        if(self.check_login()):
            with open('cookie', 'wb') as f:
                pickle.dump(s.cookies, f)
            return True
        else:
            return False

    def check_login(self):
        print('判断登录是否成功')
        session = self.session
        test_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
            'Upgrade-Insecure-Requests': '1',
            'Host': 'movie.douban.com'
        }
        test_url = 'https://movie.douban.com/subject/4920389/comments?start=220&limit=20&sort=new_score&status=P&percent_type='
        rs = session.get(url=test_url, headers=test_headers, allow_redirects=False)
        if rs.status_code == 200:
            print('登录成功')
            # print(rs.text)
            return True
        else:
            print('登录失败')
            return False

    def get_captcha(self, html):
        #获取验证码地址
        captcha_url = html.xpath('//img[@class="captcha_image"]/@src')[0]
        img = requests.get(captcha_url)
        if img.status_code == 200:
            with open('captcha.jpg', 'wb') as f:
                f.write(img.content)
        image = Image.open('captcha.jpg')
        image.show()
        # 让用户根据验证码图片输入验证码
        captcha_solution = input('please input the captcha:')
        captcha_id = html.xpath('//input[@name="captcha-id"]/@value')[0]
        remove('captcha.jpg')
        return captcha_id, captcha_solution

    def add_cookies(self):
        print('---正在使用添加cookie方式登录---')
        try:
            with open('cookie', 'rb') as f:
                self.cookies = pickle.load(f)
                self.session.cookies = self.cookies
            if(self.check_login()):
                return True
            else:
                return False
        except:
            return False

    def __login__(self):
        # self.init_database()
        if (self.add_cookies()):
            print('添加cookie登录成功')
            return True
        else:
            print('添加cookie失败，用账号密码重新登录')
            if (self.login()):
                return True
            else:
                print('登录失败啦，请检查设置')
                return False

if __name__ == '__main__':
    spider = Spider()
    spider.login()
    # spider.__login__()
    # spider.add_cookies()
    # spider.add_cookies()
    # fs_page = s.get('https://movie.douban.com/subject/4920389/comments?start=220&limit=20&sort=new_score&status=P&percent_type=')
    # print(fs_page.text)
# a.bn-more
# captcha-solution: glass
# captcha-id: EVgILOuG3rVaDA30nlujBWoF:en