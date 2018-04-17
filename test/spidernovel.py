import requests
from bs4 import BeautifulSoup
import time
import os
# def get_index(url):
#     headers = {}
#     headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
#     res = requests.get(url,headers=headers)
#     if(res.status_code != 200):
#         return
#     soup = BeautifulSoup(res.content)
#     items = soup.find_all('li',class_='item')
#     for item in items:
#         print(type(item))
#
#
# if __name__ == '__main__':
#     headers = {}
#     headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
#     url = 'http://yuedu.163.com/newBookReader.do'
#     # url1 = 'http://yuedu.163.com/book_reader/743bde5ce5b844a8bf838b25ea8eb43d_4/732b64bccc4744c2a8e9d78f2a0cabfc_5'
#     # payload = {
#     #     'operation': 'info',
#     #     'sourceUuid': '743bde5ce5b844a8bf838b25ea8eb43d_4',
#     #     'catalogOnly': 'true'
#     # }
#     # operation = info
#     # & sourceUuid = 743bde5ce5b844a8bf838b25ea8eb43d_4
#     # & catalogOnly = true
#     rs = requests.get(url,headers=headers)
#     print(rs.text)
#     # print('test result {}'.format(rs.status_code))
#     #
#     # html = BeautifulSoup(rs.content)
#     # print(html.prettify())
#     # get_index('http://yuedu.163.com/source/743bde5ce5b844a8bf838b25ea8eb43d_4')
# if __name__ == '__main__':
#     string = '1234bi13'
#     k = filter(str.isdigit, string)
#     numlist = list(k)
#
#     print(k)
#
#     print(numlist)
if __name__ == '__main__':
    headers = {}
    headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    # proxy =
    douban_url = 'https://www.douban.com/people/64250387/'

    # url = 'https://alpha.wallhaven.cc/search?q=girl&categories=111&purity=100&sorting=relevance&order=desc&page=2'
    # proxi = {"http":' 39.137.46.77'}
    # rs = requests.get(douban_url,headers=headers,proxies=proxi)
    # print(rs.status_code)
    # bf = BeautifulSoup(rs.text)
    # print(bf.prettify())
    # # print(rs.text)
    proxi = {"http": '192.155.185.176'}
    url = 'https://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-644668.jpg'
    pic = requests.get(url, headers=headers, proxies=proxi)
    pic_path = ''
    f = open(pic_path, 'wb')
    f.write(pic.content)
    f.close()
