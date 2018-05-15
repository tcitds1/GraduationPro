import requests
import pickle
import time
import random
from os import remove
from PIL import Image
from lxml import html
import copy
etree = html.etree
from pymongo import MongoClient

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
         'Referer':'https://accounts.douban.com/login',
         'form_email':'tcitds@163.com',
         'form_password':'ywx199722',
         'login':'登录',
         'redir':'https://movie.douban.com/',
         'source': 'None'
        }
        self.session = requests.session()
        self.cookies = ''

    def init_database(self):
        print('初始化数据mongodb数据库啦...')
        client = MongoClient('localhost', 27017)
        db = client.test_database
        self.col = db.user_col

    def login(self):
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
            self.spider_comment('1291561')

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
            with open('cookie', 'wb') as f:
                pickle.dump(session.cookies, f)
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

    def spider_comment(self, movie_id):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
            'Host': 'movie.douban.com',
            'Upgrade-Insecure-Requests': '1',
        }
        s = self.session
        start = 0
        page = 1
        # 'https://movie.douban.com/subject/1291561/comments?start=0&limit=20&sort=new_score&status=P&percent_type='
        url_hot = 'https://movie.douban.com/subject/{}/comments?start={}&limit=20&sort=new_score&status=P&percent_type='.format(movie_id, start)
        url_new = 'https://movie.douban.com/subject/{}/comments?start={}&limit=20&sort=time&status=P&percent_type='.format(movie_id, start)
        while(True):
            response = s.get(url=url_hot, headers=headers)
            if(response.status_code == 200):
                self.analysis_page(response.text, page)
                print('当前已访问第{}页  {}'.format(page, time.asctime(time.localtime(time.time()))))
                time.sleep(random.uniform(5,6))
                start = start + 20
                page = page + 1
                url_hot = 'https://movie.douban.com/subject/{}/comments?start={}&limit=20&sort=new_score&status=P&percent_type='.format(movie_id,start)
                headers['Referer'] = url_hot
                if(start == 500):
                    print('热门评论已爬取完毕')
                    break;
            else:
                print('访问电影第{}页失败'.format(page))
                break

    def analysis_page(self, text, page):
        user_list = []
        html = etree.HTML(text)
        # 从哪部电影爬的
        from_movie = html.xpath('//div[@id="content"]/h1/text()')[0].replace(' 短评', '')
        comment_items = html.xpath('//div[@class="comment-item"]')
        print(type(comment_items))
        print(len(comment_items))
        for item in comment_items:
            user_dic = {}
            item = copy.deepcopy(item)
            user_name = item.xpath('//div[@class="comment-item"]/div[@class="avatar"]/a/@title')[0]
            user_page = item.xpath('//div[@class="comment-item"]/div[@class="avatar"]/a/@href')[0]
            user_avator = item.xpath('//div[@class="comment-item"]/div[@class="avatar"]/a/img/@src')[0].replace('/u','/ul')
            from_movie = from_movie
            user_dic['user_name'] = user_name
            user_dic['user_page'] = user_page
            user_dic['user_avator'] = user_avator
            user_dic['page'] = page
            user_dic['from_movie'] = from_movie
            user_list.append(user_dic)
        col = self.col
        col.insert_many(user_list)


    def add_cookies(self):

        with open('cookie', 'rb') as f:
            self.cookies = pickle.load(f)
            self.session.cookies = self.cookies
        if(self.check_login()):
            self.spider_comment(1291561)

if __name__ == '__main__':
    spider = Spider()

    # spider.login()
    spider.init_database()
    spider.add_cookies()
    # spider.add_cookies()
    # spider.add_cookies()
    # fs_page = s.get('https://movie.douban.com/subject/4920389/comments?start=220&limit=20&sort=new_score&status=P&percent_type=')
    # print(fs_page.text)
# a.bn-more
# captcha-solution: glass
# captcha-id: EVgILOuG3rVaDA30nlujBWoF:en