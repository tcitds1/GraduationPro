from urllib import request
if __name__ == '__main__':
    req = request.Request("http://www.baidu.com")
    response = request.urlopen(req)
    print('geturl打印信息 {0} \n'.format(response.geturl()))
    print('getinfo打印信息 {}'.format(response.info()))
    print('getcode打印信息 {}'.format(response.getcode()))