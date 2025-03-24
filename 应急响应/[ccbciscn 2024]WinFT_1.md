## [ccbciscn 2024]WinFT_1 https://github.com/CTF-Archives/2024-ccbciscn/tree/main 

* 考点：电子取证，网络连接
* 工具：netstat

题目信息如下：
    
```
某单位网管日常巡检中发现某员工电脑（IP：192.168.116.123）存在异常外连及数据传输行为，随后立即对该电脑进行断网处理，并启动网络安全应急预案进行排查。

1、受控机木马的回连域名及ip及端口是（示例：flag{xxx.com:127.0.0.1:2333}）

```

使用netstat -n命令查找外联地址，得到ip地址
![alt text](<images/[ccbciscn 2024]WinFT_1-netstat.png>)
查找host文件
```
tpye C:\Windows\System32\drivers\etc\hosts
```
得到域名
![alt text](<images/[ccbciscn 2024]WinFT_1-hosts.png>)

flag为
```
flag{miscsecure.com:192.168.116.130:443}
```