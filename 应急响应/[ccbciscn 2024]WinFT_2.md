## [ccbciscn 2024]WinFT_2 https://github.com/CTF-Archives/2024-ccbciscn/tree/main 

* 考点：电子取证，应急响应，base64
* 工具：无

题目信息如下：

```
2、受控机启动项中隐藏flag是
```
先查看msconfig启动项，并未发现可疑的地方

再查看任务计划taskschd.msc
![alt text](<images/[ccbciscn 2024]WinFT_2-taskschdMsc.png>)
得到base64编码，用cyperchef解码后得到flag

![alt text](<images/[ccbciscn 2024]WinFT_2-base64解码.png>)
```
{AES_encryption_algorithm_is_an_excellent_encryption_algorithm}
```第二周题目wp（MISC WEB）\WinFT_2\images\[ccbciscn 2024]WinFT_2-taskschdMsc.png