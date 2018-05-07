import requests
from bs4 import BeautifulSoup
from os import remove
from PIL import Image
import pickle
#import http.cookiejar as cookielib
url = 'https://www.douban.com/'
login_url='https://www.douban.com/login'
data={'source':None,
      'remember':'on'
    }

headers = {'Host':'www.douban.com',
           'Referer': 'https://www.douban.com/',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
           'Accept-Encoding':'gzip, deflate, br'}

Session=requests.session()
# 读取是否保存有cookie
try:
    with open('cookie','rb') as f:
        Session.cookies=pickle.load(f)
        #这里我将读到的cookie输出
        print(Session.cookies, headers)
        log = True
# 如果没有cookie，就读入用户输入
except:
    data['form_email']='tcitds@163.com'
    data['form_password']='miniyukou'
    log = False

# 获得登陆界面的验证码
def get_captcha():
    req=Session.get(login_url)
    page_bf=BeautifulSoup(req.text,'html.parser')
    # 寻找验证码的图片（有可能不需要验证码 这时返回NULL）
    try:
        img_src=page_bf.find('img',id='captcha_image').get('src')
    except:
        return 'NULL','NULL'
    # 如果需要验证码下载该验证码并打开
    img=requests.get(img_src)
    if img.status_code==200:
        with open('captcha.jpg','wb') as f:
            f.write(img.content)
    image=Image.open('captcha.jpg')
    image.show()
    # 让用户根据验证码图片输入验证码
    captcha=input('please input the captcha:')
    remove('captcha.jpg')
    # 由于post-data里还要求captcha-id所以我从图片网址中截取id
    captcha_id=img_src[img_src.find('=')+1:]
    captcha_id=captcha_id[:captcha_id.find('&')]
    return captcha,captcha_id

def login():
    #获得验证码和验证码id
    if not log:
        captcha,captcha_id=get_captcha()
        if captcha!='NULL':
            data['captcha-solution']=captcha
            data['captcha-id']=captcha_id
        # 进行登陆
        page_login=Session.post(login_url,data=data,headers=headers)
        # 为了验证是否登陆成功我将登陆返回的页面html打印出来发现登陆失败
        #print(page_login.text)
    else:
        page_login=Session.get(url,headers=headers)
    page_login_bf=BeautifulSoup(page_login.text,'html.parser')
    print(page_login_bf.prettify())
    # 如果登陆打印登录账号
    # name=page_login_bf.find_all('a',class_='bn-more')
    # print(name[0].text)
    # 将此时的cookie保存方便下次登陆
    with open('cookie', 'wb') as f:
        pickle.dump(Session.cookies,f)

if __name__=='__main__':
    login()