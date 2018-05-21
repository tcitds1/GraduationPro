# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 14:47:09 2018

"""

from requests_html import HTMLSession
from pymongo import MongoClient
from PIL import Image
import time

session = HTMLSession()


def createDB():
    # 创建mongo数据库，并建立集合
    client = MongoClient('localhost', 27017)
    db = client.douban
    col_hldwm = db.hldwm
    return col_hldwm


def login(email, password):
    # 登录豆瓣网
    url = 'https://accounts.douban.com/dataSpider'
    headers = {
        # 在network获取
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    }
    login_data = {
        # 在network获取
        "source": 'index_nav',
        'redir': 'https://www.douban.com',
        "form_email": email,
        "form_password": password,
        "dataSpider": "登录",
    }
    captcha_html = session.get(url).html
    # 每次get(url)都会刷新验证码，所以只能get一次并同时获取验证码地址和验证码id !!!!!!!!!!!!!!!!
    captcha_img = captcha_html.find('img.captcha_image', first=True)
    if captcha_img:
        # 如果获取了验证码图片则填写验证码并添加进login_data
        login_data = identify_captcha(login_data, captcha_html, captcha_img)
    html = session.post(url, headers=headers, data=login_data)
    html = session.get(
        'https://movie.douban.com/subject/26683723/comments?start=0&limit=20&sort=new_score&status=P&percent_type=').html
    if html.find('a.bn-more', first=True) is None:
        print('登录失败')
        return False
    else:
        print('登录成功，当前为：%s' % html.find('a.bn-more', first=True).text)
        return True


def identify_captcha(login_data, captcha_html, captcha_img):
    # 识别验证码并将其添加进login_data
    captcha_id = captcha_html.find('div.captcha_block', first=True).find('input')[1].attrs['value']
    img_src = captcha_img.attrs['src']
    ir = session.get(img_src, stream=True)
    f = open('d:\\captcha.jpg', 'wb')
    f.write(ir.content)
    f.close()
    Image.open('d:\\captcha.jpg').show()
    captcha_solution = input('请输入验证码:')
    login_data['captcha-solution'] = captcha_solution
    login_data['captcha-id'] = captcha_id
    return login_data


def get_current_comments(html, col_hldwm):
    # 获取当前页的评论并存入mongodb
    comments = html.find('div.comment')
    for comment in comments:
        _id = comment.find('input', first=True).attrs['value']
        comment_info = comment.find('p', first=True).text
        if len(comment.find('span')[4].attrs['title']) == 2:
            class_ = comment.find('span')[4].attrs['title']
        else:
            class_ = ''
        votes = comment.find('span.votes', first=True).text
        col_hldwm.save({'_id': _id, 'comment_info': comment_info, 'class': class_, 'votes': votes})


def get_all_comments(col_hldwm):
    # 获取所有页面的评论
    first = 'https://movie.douban.com/subject/26683723/comments'
    end = '?start=0&limit=20&sort=new_score&status=P&percent_type='
    while 1:
        url = first + end
        html = session.get(url).html
        get_current_comments(html, col_hldwm)
        try:
            end = html.find('a.next', first=True).attrs['href']
        except AttributeError:
            break
        time.sleep(0.5)


if __name__ == '__main__':
    email = input('帐号:')
    password = input('密码:')
    col_hldwm = createDB()
    if login(email, password):
        print('正在收集数据，请等待...')
        get_all_comments(col_hldwm)
        print('共收集%s条数据' % str(col_hldwm.count()))
        print('完成！')
    else:
        pass  