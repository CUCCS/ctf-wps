##  [MoeCTF 2022] Base

### 基本信息

* 题目名称： [MoeCTF 2022] Base
* 题目链接：https://www.nssctf.cn/problem/3319
* 考点清单：换表base64，逆向技术
* 工具清单：IDA Pro，DIE

### 1.1 看到什么

***题目关键信息列表：***

下载附件后发现是一个名为base的exe运行文件

### 1.2 解题思路

显然，我们需要对这个文件进行反汇编逆向分析，猜测需要分析反汇编后的代码，然后编写脚本得出flag，同时，结合题目名字和文件名，猜测会用到base系列的编码。

### 1.3 ✅ 尝试过程和结果记录

1. 首先先查壳，发现64位无壳。

![image-20250527183248528](./images/%5BMoeCTF%202022%5D%20Base_1.png)

2. 那么直接丢到64位的IDA中进行反汇编

   ![image-20250527184719337](./images/%5BMoeCTF%202022%5D%20Base_2.png)

   显然，发现当前main函数有flag的提示，所有这就是我们需要分析的，对汇编代码不熟悉可以使用F5快捷键生成C语言伪代码进行分析。

3. 分析C语言伪代码

   ![image-20250527185003882](./images/%5BMoeCTF%202022%5D%20Base_3.png) 

   此时就清晰很多了，代码流程就是先将常量字符串 `"1wX/yRrA4RfR2wj72Qv52x3L5qa="` 复制到 `base64` 数组，然后读取用户输入存入数组`inp`，然后调用函数`base64_decode`（根据函数名字，显然可以知道是base64解密函数）,数组`base64`作为参数传进去，并且将返回结果存入数组`de64`，然后比较`de64`和`inp`，相等就输出 `"great!"`，那么到这了，就十分明了了。

   flag就是输入存到inp的字符串，并且需要和串`"1wX/yRrA4RfR2wj72Qv52x3L5qa="` 经过函数`base64_decode`后返回值相同。

   此时，聪明的人已经想到直接将字符串进行base64解码就可以得到flag。==但是==，这里有个**坑**，初学者很容易犯，就是函数`base64_decode`，我们并没有查看里面的代码具体是什么，就直接判断了，出题人是可以随意更改里面的内容的。

4. 所以，我们点进去分析函数`base64_decode`

   ![image-20250527190939681](./images/%5BMoeCTF%202022%5D%20Base_4.png)

   发现这里是正常base64的解码流程，但是注意使用的是否是标准的base64表（不清楚这个的先去了解base64编码解码原理）。

   发现这里的base64表换成了`abcdefghijklmnopqrstuvwxyz0123456789+/ABCDEFGHIJKLMNOPQRSTUVWXYZ`

   ![image-20250527191230273](./images/%5BMoeCTF%202022%5D%20Base_5.png)

5. 所以，我们通过base64新表编写base64解码脚本即可得到flag！

   具体脚本如下（编写过程略,脚本编写可以自己手写一份base64解码过程，或者调用第三方库，也可以用在线网站解码，记得换表就行）：

   ```
   import base64
   
   s1 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
   
   # 换表
   s2 = 'abcdefghijklmnopqrstuvwxyz0123456789+/ABCDEFGHIJKLMNOPQRSTUVWXYZ'
   
   en_text = '1wX/yRrA4RfR2wj72Qv52x3L5qa='
   
   # 将换表字符映射回标准表
   map_text = ''
   for ch in en_text:
       if ch != '=':
           idx = s2.index(ch)
           map_text += s1[idx]
       else:
           map_text += ch
   
   print(map_text)    #原来的
   print(base64.b64decode(map_text))  # 解码后的 bytes
   
   ```

   运行结果如下：

   ![image-20250527193001816](./images/%5BMoeCTF%202022%5D%20Base_6.png)

   所以flag是`moectf{qwqbase_qwq}`