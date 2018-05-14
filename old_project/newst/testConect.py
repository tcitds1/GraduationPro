import os
import time
import requests
if __name__ == '__main__':
    url = 'https://wikiwiki.jp/'
    headers = {}
    headers = {
        'User-Agent': ''
    }
    rs = requests.get(url=url, headers=headers)
    print(rs.status_code)