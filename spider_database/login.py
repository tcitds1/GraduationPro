import requests
from bs4 import BeautifulSoup
from os import remove
from PIL import Image
from lxml import html
etree = html.etree
from pymongo import MongoClient

class Spider():
    def __init__(self):
        self.login_url = 'https://accounts.douban.com/login'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        }
        self.login_data = {
            'source': 'movie',
            'redir': 'https://movie.douban.com/',
            'form_email': 'tcitds@163.com',
            'form_password': 'miniyukou1997',
            'login': '登录'
        }
        self.session = requests.session()
    def login(self):
        s = self.session
        rsponse = s.get(url=self.login_url, headers=self.headers)
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
            s.post(url=self.login_url, headers=self.headers, data=self.login_data)
        #判断是否登录成功
        rs = s.get('https://movie.douban.com/',headers = self.headers)
        check_html = etree.HTML(rs.text)
        check_tag = check_html.xpath('//a[@class="bn-more"]')
        if(len(check_tag)) == 0:
            print('登录失败 请检查代码')

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

if __name__ == '__main__':
    spider = Spider()
    spider.login()
    # fs_page = s.get('https://movie.douban.com/subject/4920389/comments?start=220&limit=20&sort=new_score&status=P&percent_type=')
    # print(fs_page.text)
# a.bn-more
# captcha-solution: glass
# captcha-id: EVgILOuG3rVaDA30nlujBWoF:en