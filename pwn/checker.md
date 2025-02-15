## 基本信息

- 题目名称： [HNCTF 2022 WEEK4]checker
- 题目链接： https://www.nssctf.cn/problem/3106
- 考点清单： html
- 工具清单： 无
- payloads： 无

## 一、看到什么

### 第一轮

1. 一个html文件和两个被引用的图片文件

## 二、想到什么解题思路

### 第一轮

1. flag可能直接藏在源码里
1. 通过源码算法编写反算法

## 三、尝试过程和结果记录

### 第一轮

1. 直接双击进网站看看，是一个登录界面

![](./images/\[HNCTF 2022 WEEK4\]checker-html.png)

1. 打开源代码搜集信息，未发现直接存储的flag，但发现关键信息

![\[HNCTF 2022 WEEK4\]checker-code_info](./images/\[HNCTF 2022 WEEK4\]checker-code_info.png)

核心算法就是将b64形式的密码解码后与密钥流逐位异或（二元加法流密码）

3. 尝试直接修改源码使其通过校验

![](./images/\[HNCTF 2022 WEEK4\]checker-encode.png)

4. 运行网页，输入用户名为`Admin`，密码为`goldenticket`，成功得到flag

![](./images/\[HNCTF 2022 WEEK4\]checker-flag.png)

## 四、总结与反思

- 解题收获：积累前端代码逆向经验
- 不足之处：任何时候，*不要直接* **双击打开来自于不可信源的文件** ，即使是参加 CTF 比赛或做题，实在要开就用虚拟机开；
- 改进措施：优先审查源代码

## 五、本地工具环境配置

无
