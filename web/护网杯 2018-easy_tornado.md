## 基本信息

- 题目名称：护网杯 2018-easy_tornado
- 题目链接：https://www.nssctf.cn/problem/175
- 考点清单：SSTI、Tornado、md5
- 工具清单：Yakit
- payloads：Tornado环境变量

### 解题思路

题目给了三个可点击的超链接

![](images/%E6%8A%A4%E7%BD%91%E6%9D%AF%202018-easy_tornado-dir.png)

都点击一遍，我们可以得知以下信息：
- flag在`/fllllllllllllag`
- hint为`md5(cookie_secret+md5(filename))`，告诉我们计算hash值的方式
- 随意修改hash值，会跳到`error?msg=Error`页面，更改msg的值，页面也会相应改变

我们知道了flag文件的filename，现在需要获得cookie_secret

### 过程和结果记录

使用`error?msg={{handler.settings}}`获取环境变量的值：
```
36c2c001-c279-4388-9ddf-40e7b9ceffed
```

![](images/%E6%8A%A4%E7%BD%91%E6%9D%AF%202018-easy_tornado-get-env.png)

使用下面的代码计算`welcome.txt`的hash

![](images/%E6%8A%A4%E7%BD%91%E6%9D%AF%202018-easy_tornado-hash.png)

两个hash相同，说明我们的算法是正确的，现在我们可以计算得到/fllllllllllllag的hash

将获得的hash值填入url中，即可得到flag

![](images/%E6%8A%A4%E7%BD%91%E6%9D%AF%202018-easy_tornado-flag.png)

### 总结
- 这道题的重点在于知道如何获得`cookie_secret`，但是题目已经提示了`tornado render`模板，所以我们可以通过模板注入获取环境变量