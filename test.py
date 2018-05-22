import random
import requests
import time
from lxml import html
etree = html.etree
ua_list = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
            'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
        ]
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
'''
<li class="comment-item" data-cid="844365694">
    <div class="avatar">
        <a title="失控芭乐" href="https://www.douban.com/people/fish6058/">
            <img src="https://img1.doubanio.com/icon/u1389804-18.jpg">
        </a>
    </div>
    <div class="comment">
        <h3>
            <span class="comment-vote">
                <span id="c-844365694" class="vote-count">12570</span>
                    <a href="javascript:;" id="btn-844365694" class="j vote-comment" data-cid="844365694">有用</a>
            </span>
            <span class="comment-info">
                <a href="https://www.douban.com/people/fish6058/">失控芭乐</a>
                    <span class="user-stars allstar50 rating" title="力荐"></span>
                <span>2014-09-12</span>
            </span>
        </h3>
        <p class="comment-content">真的要到很久以后，才会明白，每一个选择只要努力过，都是正确的选择。</p>
    </div>
</li>
'''
def testpy(str):
    print(str.format("333"))

def test(k):
    if(k==5):
        return
    print(k)

if __name__ == '__main__':
    for i in range(8):
        test(i)
    # proxies = {
    #     'http': 'http://192.155.185.239:80'
    # }
    # # '192.155.185.239:80'
    # headers = {
    #     'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101'
    # }
    # url = 'https://movie.douban.com/subject/26793157/'
    # count = 1
    # while True:
    #     rs = requests.get(url=url, headers=headers, proxies=proxies)
    #     if(rs.status_code==200):
    #         print('已成功访问 {} 次'.format(count))
    #         count = count + 1
    #     else:
    #         break

    # url = 'http://piping.mogumiao.com/proxy/api/get_ip_bs?appKey=fbfc504c469c4c669cbe57a8b220e64c&count=5&expiryDate=0&format=1&newLine=2'
    # data = requests.get(url=url).json()['msg']
    # for item in data:
    #     proxy = item['ip'] + ':' + item['port']
    #     print(proxy)

    # tag_list = ['剧情', '喜剧', '动作', '爱情', '科幻', '悬疑', '惊悚', '恐怖', '犯罪', '同性', '音乐', '歌舞', '传记',
    #             '历史', '战争', '西部', '奇幻', '冒险', '灾难', '武侠', '情色']
    # tag_url_list = list()
    # # 'https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=&start=10000&genres=爱情'
    # tag_url = 'https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=&start={}&genres={}'
    # for i in tag_list:
    #     total_url = tag_url.format('{}', i)
    #     tag_url_list.append(total_url)
    # for i in tag_url_list:
    #     test = 'Movie Spider : {}----{} tag start----'.format(time.ctime(), i[-2::])
    #     print(test)



