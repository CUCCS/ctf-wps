## [ccbciscn 2024]WinFT_5 https://github.com/CTF-Archives/2024-ccbciscn/tree/main 

* 考点：文件分离，流量分析
* 工具：dd，binwalk，wireshark

题目信息如下：
```
5、分析流量，获得压缩包中得到答案
```

wireshark分析流量包后，并没有什么结果，扔去kali里binwalk一下，出来了一大串东西，能看到其中有一个zip压缩包
![alt text](<images/[ccbciscn 2024]WinFT_5-binwalk分析文件.png>)

用dd提取出来
```
dd if=恶意流量包.cap  of=1.zip skip=22258409 bs=1 count=318
```
提取出来后，尝试打开，发现需要密码并且不是伪加密，利用010editor查看恶意流量包
![alt text](<images/[ccbciscn 2024]WinFT_5-010editor2.png>)
base64解码后，得到一串中文
![alt text](<images/[ccbciscn 2024]WinFT_5-base64中文解码.png>)
解压后得到flag
```
flag{a1b2c3d4e5f67890abcdef1234567890-2f4d90a1b7c8e2349d3f56e0a9b01b8a-CBC}
```