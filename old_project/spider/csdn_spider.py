from urllib import request

if __name__ == '__main__':
    url = 'http://csdn.net'
    header = {}
    header['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
    req = request.Request(url, headers=header)
    response = request.urlopen(req)
    html = response.read().decode('utf-8')
    print(html)
