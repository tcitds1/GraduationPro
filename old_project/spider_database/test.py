# 117.158.146.70:8908
import requests


login_url = 'https://accounts.douban.com/login'
movie_comments_url = 'https://movie.douban.com/subject/4920389/comments?start=0&limit=20&sort=new_score&status=P&percent_type='
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
    'Upgrade-Insecure-Requests': '1',
    'Host': 'accounts.douban.com',
}
proxies = {
    'http': '120.92.118.64:10018'
}
print(requests.get(url=login_url, headers=headers, proxies=proxies).status_code)