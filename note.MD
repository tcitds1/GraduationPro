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

fitler()函数返回值应该用list转化成数组