## 基本信息

* 题目名称： [SWPUCTF 2022 新生赛]ez_ez_unserialize
* 题目链接： https://www.nssctf.cn/problem/3082
* 考点清单： 反序列化，_wakeup绕过
* 工具清单： PHP环境，hackbar
* payloads：反序列化

## 一、看到什么

**题目关键信息列表**：

1. `PHP 源代码`: 该题的`PHP`源码，本题的唯一线索。


## 二、想到什么解题思路

1. 源码审计：

   - 题目意思很明确，按照条件判断的指示，`flag`已经确认在`fllllllag.php`中了，题目还给了`highlight_file()`,这就是我们最后一步，给`flag`所在文件进行输出。
   - 题目只给了一个类，构造`POP`链解题的可能性不大。
   - 题目给了多种魔术方法。

## 三、尝试过程和结果记录

**代码解读：**

- 首先对这些魔术方法有所了解，知道它们触发的条件：

    - `__destruct()` 对象销毁，或者脚本执行完时触发;
    - `__wakeup()`   反序列化中自动执行
    - `__construct()` 创建类的新对象时,，会自动调用该方法。

-  `__FILE__`是一个预定义的魔术常量，用于返回当前文件的完整路径和文件名。这个地方我们无法控制。

- `@unserialize($_REQUEST['x']);` 介绍
    - 我们可以传入`GET`请求、`POST`请求和`COOKIE`任何一个来传递数据x，它们都可以通过`$_REQUEST['x']`进行访问。
    - `unserialize()`是将里面的字符串再转换回原来的数据结构。
    - `@`会忽略该表达式可能产生的任何错误信息。

- `__destruct()`这个方法一定是最后执行的，只有它可以输出`flag`, 所以需要将属性x设置为`fllllllag.php`。

- 但是这里存在一个`__wakeup()`方法，它会在反序列化的时候将值设定为当前的文件。所以我们要绕过这个方法，不让他设置属性`x`的值。



**尝试过程：**

1. 我们新建一个`test.php`,将反序列化相关的的代码`COPY`下来，本地进行序列化，并注释掉部分不影响功能的代码, 使用`basename()`函数输出文件名看起来更简洁。我们输入文件名`fllllllag.php`，在本地进行序列化，得到结果`O:1:"X":1:{s:1:"x";s:13:"fllllllag.php";}`,再使用`unserialize()`进行反序列化，`__destruct()`输出得到的文件名称是`test.php`,而不是我们想要的`fllllllag.php`。

    ```php
    <?php
    class X
    {
        public $x = __FILE__;
        function __construct($x)
        {
            $this->x = $x;
        }
        function __wakeup()
        {
            if ($this->x !== __FILE__) {
                $this->x = __FILE__;
            }
        }
        function __destruct()
        {
            //highlight_file($this->x);
            echo basename($this->x);
            //flag is in fllllllag.php
        }
    } 

    //$a = new X('fllllllag.php');
    //echo serialize($a);//O:1:"X":1:{s:1:"x";s:13:"fllllllag.php";}
    unserialize('O:1:"X":1:{s:1:"x";s:13:"fllllllag.php";}')//test.php
    ?>
    ```
2. 所以我们要绕过`__wakeup()`的赋值。存在有一个漏洞可供利用。[CVE-2016-7124](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-7124)
    - 漏洞环境：`PHP5 < 5.6.25` 或者 `PHP7 < 7.0.10`
    - 利用方法：当序列化字符串中表示对象属性个数的值大于真实的属性个数时，会跳过`__wakeup`的执行。

3. `O:1:"X":1:{s:1:"x";s:13:"fllllllag.php";}`此序列化字符串中的每个字符意义如下。

    ```
    O：对象标识
    1：类名长度
    "X"：类的名称
    1：属性数量
    s：属性名类型（字符串）
    1：属性名长度
    "x"：属性的名称
    s：属性值类型（整数）
    13：属性值长度
    "fllllllag.php"：属性值名称
    ```
4. 因此，我们修改序列化字符串为`O:1:"X":2:{s:1:"x";s:13:"fllllllag.php";}`即可得到结果，本地尝试通过。再通过`GET`参数进行传递，即可得到`flag`。

![payloads](images/[SWPUCTF%202022%20新生赛]ez_ez_unserialize-payloads.png)

## 四、总结与反思

1. `__wakeup()`函数存在绕过漏洞，在其赋的值是我们不需要的时候，可以考虑绕过，需满足序列化字符串中表示对象属性个数的值大于真实的属性个数，但是需要注意`php`版本限制。

