> '//'是整除 
>
> '**' 是x的y次方
>
> '<< >>'左移 右移 转化成二进制移位
>
> 'input(str)' 接收键盘输入
>
> global 语句 在函数中声明 给程序顶层赋值
>
> 只有那些位于参数列表末尾的参数才能被赋予默认参数值，意即在函数的参数列表中拥
> 有默认参数值的参数不能位于没有默认参数值的参数之前。
> 这是因为值是按参数所处的位置依次分配的。举例来说， def func(a, b=5) 是有效的，
> 但 def func(a=5, b) 是无效的。（跟js的有一个有点像）
>
> 参数 *number 数组，**字典
>
> 我们可以通过使用函数的 ```__doc__``` （注意其中的双下划綫）属性（属于函数的名称）来获取
> 函数 print_max 的文档字符串属性。
>
> ```python
> ab = {
> 'Swaroop': 'swaroop@swaroopch.com',
> 'Larry': 'larry@wall.org',
> 'Matsumoto': 'matz@ruby-lang.org',
> 'Spammer': 'spammer@hotmail.com'
> }
> print("Swaroop's address is", ab['Swaroop'])
> # 删除一对键值—值配对
> del ab['Spammer']
> ```
>
> 

## 

初始化参数 headers请求头  User-Agent 

from lxml import etree找不到etree的办法，

`from lxml import html`

`etree = html.etree`

****

## [with 工作原理](https://blog.csdn.net/u012609509/article/details/72911564)

（１）紧跟with后面的语句被求值后，返回对象的“–enter–()”方法被调用，这个方法的返回值将被赋值给as后面的变量； 
（２）当with后面的代码块全部被执行完之后，将调用前面返回对象的“–exit–()”方法。 
with工作原理代码示例：

```
class Sample:
    def __enter__(self):
        print "in __enter__"
        return "Foo"
    def __exit__(self, exc_type, exc_val, exc_tb):
        print "in __exit__"
def get_sample():
    return Sample()
with get_sample() as sample:
    print "Sample: ", sample12345678910
```

代码的运行结果如下：

```
in __enter__
Sample:  Foo
in __exit__123
```

可以看到，整个运行过程如下： 
（１）**enter**()方法被执行； 
（２）**enter**()方法的返回值，在这个例子中是”Foo”，赋值给变量sample； 
（３）执行代码块，打印sample变量的值为”Foo”； 
（４）**exit**()方法被调用；

### 用request保存文本文件到本地

在罕见的情况下，你可能想获取来自服务器的原始套接字响应，那么你可以访问 `r.raw`。 如果你确实想这么干，那请你确保在初始请求中设置了 `stream=True`。具体你可以这么做：

```
>>> r = requests.get('https://api.github.com/events', stream=True)
>>> r.raw
<requests.packages.urllib3.response.HTTPResponse object at 0x101194810>
>>> r.raw.read(10)
'\x1f\x8b\x08\x00\x00\x00\x00\x00\x00\x03'

```

但一般情况下，你应该以下面的模式将文本流保存到文件：

```
with open(filename, 'wb') as fd:
    for chunk in r.iter_content(chunk_size):
        fd.write(chunk)
```

request 参数 `cookies`` headers``timeout` 

## 错误与异常

遇到网络问题（如：DNS 查询失败、拒绝连接等）时，Requests 会抛出一个 `ConnectionError` 异常。

如果 HTTP 请求返回了不成功的状态码， [`Response.raise_for_status()`](http://docs.python-requests.org/zh_CN/latest/api.html#requests.Response.raise_for_status) 会抛出一个 `HTTPError`异常。

若请求超时，则抛出一个 `Timeout` 异常。

若请求超过了设定的最大重定向次数，则会抛出一个 `TooManyRedirects` 异常。

**第三方库chardet来检测网页编码**

>pip3 install chardet
>
>chardet.detect(html)

# Beautiful Soup笔记

```python
soup = BeautifulSoup(source_doc)
#解析代码结构
soup.prettify()
#取tagname只能取到当前名字的第一个tag，取多个只能用find_all
soup.tagname
soup.tagname['attr']
#返回数组
soup.find_all('tagname')

soup.find_all('a')[0].get('attr')

tag.get_text() #获取文本
tag.string() # 获取文本


```

## 毕业设计爬虫设计

**爬虫timeout**

**爬虫连接异常**

https://alpha.wallhaven.cc/wallpapers/thumb/small/th-644872.jpg 预览小图片

https://alpha.wallhaven.cc/wallpaper/644872/thumbTags

转变成如下链接

https://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-644872.png

**关键词 python 信号处理 SIGINT**



https://www.douban.com/misc/captcha?id=yG8IYqwATA8QRrjwjrcCK6y6:en&size=s

https://www.douban.com/misc/captcha?id=pm4nTQ834G7PuRFkvPYp1maM:en&size=s

https://www.douban.com/misc/captcha?id=wIRfmKbOnvwyMKEbCE2icBvS:en&size=s

## python 装饰器

```python
def use_logging(func):

    def wrapper(*args, **kwargs):
        logging.warn("%s is running" % func.__name__)
        return func(*args)
    return wrapper

@use_logging
def foo():
    print("i am foo")

@use_logging
def bar():
    print("i am bar")

bar()
```

### set

set和dict类似，也是一组key的集合，但不存储value。由于key不能重复，所以，在set中，没有重复的key。

要创建一个set，需要提供一个list作为输入集合：

```
>>> s = set([1, 2, 3])
>>> s
{1, 2, 3}

```

注意，传入的参数`[1, 2, 3]`是一个list，而显示的`{1, 2, 3}`只是告诉你这个set内部有1，2，3这3个元素，显示的顺序也不表示set是有序的。。

重复元素在set中自动被过滤：

```
>>> s = set([1, 1, 2, 2, 3, 3])
>>> s
{1, 2, 3}

```

通过`add(key)`方法可以添加元素到set中，可以重复添加，但不会有效果：

```
>>> s.add(4)
>>> s
{1, 2, 3, 4}
>>> s.add(4)
>>> s
{1, 2, 3, 4}

```

通过`remove(key)`方法可以删除元素：

```
>>> s.remove(4)
>>> s
{1, 2, 3}

```

set可以看成数学意义上的无序和无重复元素的集合，因此，两个set可以做数学意义上的交集、并集等操作：

```
>>> s1 = set([1, 2, 3])
>>> s2 = set([2, 3, 4])
>>> s1 & s2
{2, 3}
>>> s1 | s2
{1, 2, 3, 4}

```

set和dict的唯一区别仅在于没有存储对应的value，但是，set的原理和dict一样，所以，同样不可以放入可变对象，因为无法判断两个可变对象是否相等，也就无法保证set内部“不会有重复元素”。试试把list放入set，看看是否会报错。

## yield

生成迭代器，必须在函数里面，通过next()，或者for i in Iterator来调用

#### 截取数组

```python
def printarr(arr):
    val = ''
    for i in arr:
            val += str(i) + ' '
    print(val)

l = range(10)

printarr(l)
printarr(l[::2])
printarr(l[::-2])

#从下标0开始，以2为步长

```



在vue项目中使用scsshttps://www.imooc.com/article/28195?block_id=tuijian_wz	

### MongoDb

$nin 不在里面

sort

$ne 不等于