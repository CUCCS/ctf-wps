## 基本信息

- 题目名称：BJDCTF 2020-Cookie is so subtle!
- 题目链接：https://www.nssctf.cn/problem/716
- 考点清单：SSTI、Twig
- 工具清单：Yakit
- payloads：Twig SSTI

### 解题思路

题目有两个页面可以访问。一个是flag，有一个输入框，输入的内容会有回显，初步判断为SSTI类型；另一个是hint，查看页面源代码，提示我们要仔细观察cookies
![](images/BJDCTF%202020-Cookie%20is%20so%20subtle!-hint.png)

在`flag.php`页面可以输入username，当我们输入`{{7*'7'}}`，结果返回`49`，证明这是`Twig`的SSTI。
![](images/BJDCTF%202020-Cookie%20is%20so%20subtle!-test.png)

其中，username值通过cookie传递

### 过程和结果记录

Twig 给我们提供了一个 `_self`, 虽然 `_self` 本身没有什么有用的方法，但是却有一个`env`

`env`是指属性 `Twig_Environment` 对象，`Twig_Environment` 对象有一个 `setCache` 方法可用于更改Twig尝试加载和执行编译模板（PHP文件）的位置

不过 `call_user_function()` 函数一般被php禁用了，不过有一个 `getFile()` 可以调用 `call_user_function()` 函数。然后利用`registerUnderfinedFilterCallback()`函数将exec作为回调函数传进去。

payload：
```
{{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("cat /f*")}}
```


这个payloads的第一部分 `{{_self.env.registerUndefinedFilterCallback("exec")}}`设置了一个回调，当遇到未定义的过滤器时，调用 PHP 的 exec 函数执行系统命令。第二部分 `{{_self.env.getFilter("cat /flag")}}` 尝试获取名为 "cat /flag" 的过滤器，由于该过滤器不存在，触发了之前设置的回调，从而执行 `exec("cat /flag")` 命令，显示 "flag" 文件的内容，帮助我们获得 flag。

![](images/BJDCTF%202020-Cookie%20is%20so%20subtle!-flag.png)

### 总结

- 这道题的重点在于知道如何利用`Twig`的SSTI漏洞，通过cookie传递payload。所以平时要多做题，通过积累不同类型模板注入的payload，提高解题效率。