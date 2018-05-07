import requests
import time
import random
import os
from bs4 import BeautifulSoup
if __name__ == '__main__':
    headers = {'User-Agent': 'User-Agent:Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'}
    proxi = {
        'http': '123.134.185.156'
    }
    http = ['120.194.189.121','112.27.129.54','111.20.250.124','177.21.52.44','183.232.188.32']
    UG = [
        'User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
        'User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
        'User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'User-Agent:Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
        'User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)'
    ]
    # rs = requests.get('https://www.douban.com/people/150495409/',proxies = proxi, headers=headers)
    # print(rs.status_code)
    k = 1
    # https: // www.douban.com / people / 150495409 /

    number = 150495420
    url = 'https://www.douban.com/people/' + str(number) + '/'
    rs = requests.get('https://www.douban.com/people/150495409/',proxies = proxi, headers=headers)
    start = time.time()
    i = 0
    while True:
        if(rs.status_code == 403):
            print('ip baned')
            break
        else:
            print('{} connect success {}'.format(i,number))
            time.sleep(random.uniform(0, 3))
        i=i+1
        number = number + int(random.uniform(100,200))
        if(i%5 == 0):
            proxi['http'] = http[k]
            headers['User-Agent'] = UG[k]
            k = k + 1
        url = 'https://www.douban.com/people/' + str(number) + '/'
        rs = requests.get(url, proxies=proxi, headers=headers)
    stop = time.time()
    print('spent time {} sucess {} count'.format(stop-start,i))
    # https: // www.douban.com / people / 177767948 /