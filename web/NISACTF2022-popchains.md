## 基本信息

* 题目名称： [NISACTF 2022]popchains
* 题目链接： https://www.nssctf.cn/problem/2099
* 考点清单： 反序列化，伪协议，PHP，POP链构造
* 工具清单： PHP环境,hackbar
* payloads： 反序列化

## 一、看到什么

**题目关键信息列表**：

1. `PHP 源代码`: 该题的`PHP`源码，本题的唯一线索。


## 二、想到什么解题思路

1. 源码审计：

    - 定义了三个类，还有一些魔术方法，可以看出主要考点是`POP`链构造。
    - 题目也提示了结果在 `flag.php`里面。
    - 题目中出现了`include()`函数，可能用到伪协议。

## 三、尝试过程和结果记录

**代码解读：**

- 首先对这里出现的各种魔术方法进行介绍，作为基础知识。
    - `__construct`创建类的新对象时,，会自动调用该方法。
    - `__toString()`将对象转换为字符串时自动触发
    - `__wakeup()` 反序列化中自动执行
    - `__invoke()` 将对象作为函数调用时触发
    - `__get($key)` 访问对象中不存在的属性时触发，并将名字作为参数传入


**尝试过程：**

1. 构造POP链，需要确认好入口或者出口。
    - 入口则是能够开始执行调用的地方，出口则是能够被利用的地方。我们可以选择从头找，或者是从后找。这里的入口不太好找，我们可以想一下出口。
    - 题目最下方提示了`Try to See flag.php`,就是要去访问`flag.php`这个文件，观察发现能有类似功能的只有`include()`，而且是需要传递参数`flag.php`的。所以确认这就是最后一步，标记为`-1`。

2. 倒推倒数第二步
    - 要想能执行倒数第一步，则必须执行`append()`,可以看到在`Try_Work_Hard`这个类中存在方法`__invoke()`，它很明显的会使用到`append()`,并且还带有参数,这是符合我们预期的。所以目前认为这是倒数第二步，标记为`-2`，且var值设置为与`flag.php`相关。

3. 倒推倒数第三步
    - 执行`__invoke()`方法，它的触发条件是对象作为函数调用时触发。所以我们接下来就要找一个方法能执行函数的。我们找到`__construct()`,它会执行`array()`函数，但是这里的函数名已经指定了，不能使得`Try_Work_Hard`的对象当作函数调用。
    - 那这里所以我们就需要找其他的魔术方法。我们可以看到`__get($key)`,它会将对象的属性`effort`赋值给`$function`，并且以函数的形式返回。这也就调用了该函数。
    满足我们的要求，标记为`-3`。

4. 倒推倒数第四步
    - 执行`__get($key)`方法，它的触发条件是访问对象中不存在的属性时触发，并将名字作为参数传入。所以就要找一个`Make_a_Change`这个类中不存在的属性，那再进行观察，如果我们设置`Road_is_Long`类的`string=new Make_a_Change()`，那么`string`的`page`属性，`new Make_a_Change`这个类是没有的。这样就满足了`__get($key)`的触发条件，其中`$key = page`，标记为`-4`
   
5. 倒退倒数第五步
    - 执行`__toString()`方法，它的触发条件是将对象转换为字符串时自动触发，比如`echo`指令或者是`preg_match`这样的输出或者字符串比较指令。所以这里要使用到
   `__wakeup()`函数，且`page = Road_is_Long()`。标记为`-5`

6. 倒退倒数第六步
    - 执行`__wakeup()`方法，它的触发条件是反序列化中自动执行，所以我们需要对其进行反序列化。这个时候就看到代码分隔符`pop your 2022`的上方的`unserialize()`，这个就是入口，是倒数最后一步。标记为`-6`，或者是`+1`。

7. 按照上面的步骤，依次往回写。

    ```php
        <?php  

    class Road_is_Long{
        public $page;
        public $string;
    }

    class Try_Work_Hard{
        protected  $var = "php://filter/convert.base64-encode/resource=/flag";
    }

    class Make_a_Change{
        public $effort;
    
    } 

    $a = new Road_is_Long();
    $a->page = $a;
    $a->string = new Make_a_Change();
    $a->string->effort = new Try_Work_Hard();
    <!-- $a->string->effort->var = "1"; -->

    echo urlencode(serialize($a));
    ```

    ```
    O%3A12%3A%22Road_is_Long%22%3A2%3A%7Bs%3A4%3A%22page%22%3Br%3A1%3Bs%3A6%3A%22string%22%3BO%3A13%3A%22Make_a_Change%22%3A1%3A%7Bs%3A6%3A%22effort%22%3BO%3A13%3A%22Try_Work_Hard%22%3A1%3A%7Bs%3A6%3A%22%00%2A%00var%22%3Bs%3A49%3A%22php%3A%2F%2Ffilter%2Fconvert.base64-encode%2Fresource%3D%2Fflag%22%3B%7D%7D%7D
    ```
8.将得到的payloads用`GET`请求传递，得到了`Base64`编码的结果，进行解码，即可得到`flag`。
  

## 四、总结与反思

1.构造`POP`链时，需要找准出口和入口，从一个方向出发，往另一个方向推。从入口往下找，则是看会触发什么函数。从出口往上找，则是看触发条件是什么。

2. `POP`链出口一般是一些危险函数，如下类似。
    ```
    eval()
    system()
    shell_exec()
    file_get_contents()
    include()
    ```
3. `PHP`反序列化时，若类中的属性修饰符存在`private`和`protected`，在输出`serialize()`结果时,`private`和`protected`属性也会被包含在序列化结果中。但由于`PHP`内部机制的特殊性，这些属性会通过在序列化数据中添加不可见的字符来标识其访问级别。`%00`（`ASCII`码为`0`）字符被用于标记访问权限。这个字符显示和输出可能看不到，甚至导致截断，但是`url`编码后就可以看得清楚。可以将序列化的字符用`urlencode()`编码之后,打印出来查看。同时，若某属性存在上述两种属性修饰符之一时，需要在类内对相应属性赋值才可成功。
