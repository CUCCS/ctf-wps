## 基本信息

- 题目名称： [FSCTF 2023]是兄弟，就来传你の🐎！
- 题目链接： https://www.nssctf.cn/problem/4561
- 考点清单： 文件上传，文件头绕过
- 工具清单： Yakit
- payloads： 一句话木马

## 一、看到什么

1. 一个文件上传界面，可以上传文件

## 二、想到什么解题思路

1. 使用各种方法上传一个包含一句话木马的php文件，包括修改文件后缀名，MIME绕过等

## 三、尝试过程和结果记录

1. 将修改了后缀为jpg的一句话木马`<?php @eval($_POST['cmd']);?>`上传，提示“File is not an image”，在Yakit中查看上传的文件记录，右键发送到Web Fuzzer，以便后面的修改操作
    ![alt text](<images/[FSCTF 2023]是兄弟，就来传你の🐎！-upload_jpg.jpg>)

2. 想要将一个文件伪装成图片文件，使用MIME类型绕过还不够，还需要将文件头伪装成图片文件的文件头，这样才能成功上传，常见的文件头如下：
    - GIF89a：GIF文件头
    - JFIF：JPEG文件头
    - BM：BMP文件头

    这里我们可以使用GIF的文件头，此时木马的内容如下：
    ```php
    GIF89A<?php
    @eval($_POST['cmd']);
    ```
    ![alt text](<images/[FSCTF 2023]是兄弟，就来传你の🐎！-get_out_hacker.jpg>)

    响应信息显示为“get out hacker!!!”，这表明文件内容中可能包含某些敏感关键字，触发了WAF（Web应用防火墙）的防护机制，需要进一步排查和修改。可能触发WAF的关键字包括`<?php`和`eval`。先去除php这个关键词，发现可以成功上传，但是提示文件过长，需要控制在15个长度内
    
    ![alt text](<images/[FSCTF 2023]是兄弟，就来传你の🐎！-without_php.jpg>)
    
    尝试将`<?php`替换为`<?= `，`<?= `的意思是`<?php echo`的短标签，类似的短标签包括：
    - **`<?= ... ?>`**：简写 `<?php echo ...; ?>`，PHP 5.4+ 默认支持。  
    - **`<? ... ?>`**：`<?php ... ?>`短标签，需 `short_open_tag` 启用，不推荐使用。  
    - **`<% ... %>`**：ASP风格标签，需 `asp_tags` 启用，PHP 7.0+ 已移除。  
    - **`<%= ... %>`**：ASP风格简写 `<?php echo ...; ?>`，PHP 7.0+ 已移除。  

    使用短标签可以缩短长度，但是还是不够。首部的文件头`GIF89A`也可以缩短，使用`GIF`即可。现在我们需要解决的问题是如何打印出文件内容。而在php中最短的打印根目录下的文件内容的方式是`nl /*`，`nl`的功能是为文件内容添加行号并输出，`nl /*`的意思是把所有文件都打印出来。

3. 现在上传时jpg后缀名的文件，默认是无法解析执行的。这里可以使用Yakit爆破字典来测试出可以使用的后缀名。最终，我们发现`pht`后缀名可以成功上传

    **为什么可以使用 `.pht` 扩展名？**  
    在 Apache 的默认配置中，`.pht` 扩展名被识别为 PHP 可执行文件。具体配置规则如下：
    ```apache
    #/etc/apache2/mods-enabled/php5.conf
    <FilesMatch ".+\.ph(p[345]?|t|tml)$">
        SetHandler application/x-httpd-php
    </FilesMatch>
    ```
    该正则表达式匹配 `.php3`、`.pht`、`.phtml` 等后缀，并设置对应的 PHP 处理器（详见 [相关讨论](https://github.com/monstra-cms/monstra/issues/429)）。
    
    ![alt text](<images/[FSCTF 2023]是兄弟，就来传你の🐎！-upload_pht.jpg>)

4. 访问上传成功的文件路径，得到flag
    ![alt text](<images/[FSCTF 2023]是兄弟，就来传你の🐎！-flag.jpg>)

## 四、总结与反思

- 文件伪装方法：仅修改后缀为jpg无法绕过图片检测，需进一步伪装文件头和内容。
- Apache 扩展名特性：利用 `.pht` 等冷门后缀绕过限制，需熟悉服务器配置文件规则。
- 使用Yakit的爆破字典功能，可以快速找到可以上传的文件后缀名，还可以使用到其他白名单绕过的场景中。