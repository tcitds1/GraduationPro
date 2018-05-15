import random
import requests
from lxml import html
# etree = html.etree
# ua_list = [
#             'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101',
#             'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122',
#             'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71',
#             'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95',
#             'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71',
#             'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
#             'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
#             'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
#         ]
# headers = {'User-Agent': random.choice(ua_list),
#                 'Accept': '*/*',
#                 'Connection': 'keep-alive',
#                 'Accept-Language': 'zh-CN,zh;q=0.8'}
# def getwuyou():
#     rs = requests.get('http://www.data5u.com/free/gngn/index.shtml')
#     print(rs.status_code)
#     ul_list = html.xpath('//ul[@class="l2"]')
#     for ul in ul_list:
#         try:
#             yield ':'.join(ul.xpath('.//li/text()')[0:2])
#         except Exception as e:
#             print(e)
#
#
# cookies = {
#     'JSESSIONID':'0FF288A3BE97652E4E56DBBA56965AA7'
# }
#
# headers = {
# 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
# 'Accept-Encoding': 'gzip, deflate',
# 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
# 'Cache-Control': 'max-age=0',
# 'Host': 'www.data5u.com',
# 'Proxy-Connection': 'keep-alive',
# 'Referer': 'http://www.data5u.com/free/gnpt/index.shtml',
# 'Upgrade-Insecure-Requests': '1',
# 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
# }
# rs = requests.get('http://www.data5u.com/free/gngn/index.shtml', headers=headers)
# # rs = requests.get('http://www.data5u.com/free/gngn/index.shtml')
# html = etree.HTML(rs.text)
# print(rs.status_code)
# ul_list = html.xpath('//ul[@class="l2"]')
# for ul in ul_list:
#  k = ':'.join(ul.xpath('.//li/text()')[0:2])
#  print(k)
# # Accept-Encoding: gzip, deflate
# # Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
# # Cache-Control: max-age=0
# # Cookie: JSESSIONID=0FF288A3BE97652E4E56DBBA56965AA7; Hm_lvt_3406180e5d656c4789c6c08b08bf68c2=1526097070; Hm_lpvt_3406180e5d656c4789c6c08b08bf68c2=1526098841
# #
# #
#
# # Host: www.data5u.com
# # Proxy-Connection: keep-alive
# # Referer: http://www.data5u.com/free/gnpt/index.shtml
# # Upgrade-Insecure-Requests: 1
# # User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36
# k = ['a12312','b123124','c','d']
# print(k[0:3])

if __name__ == '__main__':
    count = 0
    if count:
        print(count)