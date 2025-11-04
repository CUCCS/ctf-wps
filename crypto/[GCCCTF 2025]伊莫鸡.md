## 基本信息

- 题目名称： [GCCCTF 2025]伊莫鸡
- 考点清单： HTML实体编码、换表base64

## 一、看到什么

全是表情符号，还有一串64个不重复的字符表

## 二、想到什么解题思路

表情符号可以想到base100，64个不重复的字符表可能是换表base64的对应的表

## 三、尝试过程和结果记录

表情符号在网站上解密可以得到第一个字符串，base100
给出两串字符串：

1. `&#108;&#87;&#69;&#81;...;&#121;&#87;` —— HTML 实体编码。
2. `a6pQqIUurcibPENJSlHxjZkydT3tgY4oFeDXL5mf1V+zR7wv9CnBWh/M2sOAG80K` —— 64 个字符且不重复。
   提示说明第二串为“非标准 Base64”，意味着它是**自定义 Base64 字母表**。

**解题思路**

1. 首先将 HTML 实体转回字符，得到：
   `lWEQShlU4hgBPjP9xxEoEB6oELEQSBYUyBr9PXjeryW`。
2. 观察第二串长度正好 64，推测为自定义 Base64 字母表。
   标准 Base64 表为：`A–Z a–z 0–9 + /`。
3. 将自定义表的每个字符按索引映射回标准 Base64 表。
4. 对第一串中字符逐一替换为对应标准 Base64 字符。
5. 对替换结果做标准 Base64 解码，得到明文。

**关键代码**

```python
import base64, html
html_text = "&#108;&#87;&#69;&#81;&#83;&#104;&#108;&#85;&#52;&#104;&#103;&#66;&#80;&#106;&#80;&#57;&#120;&#120;&#69;&#111;&#69;&#66;&#54;&#111;&#69;&#76;&#69;&#81;&#83;&#66;&#89;&#85;&#121;&#66;&#114;&#57;&#80;&#88;&#106;&#101;&#114;&#121;&#87;"
custom = "a6pQqIUurcibPENJSlHxjZkydT3tgY4oFeDXL5mf1V+zR7wv9CnBWh/M2sOAG80K"
standard = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
mapping = {custom[i]: standard[i] for i in range(64)}
decoded = html.unescape(html_text)
mapped = "".join(mapping.get(ch, ch) for ch in decoded)
print(base64.b64decode(mapped + "=" * ((4 - len(mapped) % 4) % 4)).decode())
```

**flag**

```
GCCCTF{W31C0M3_70_6CCC7F_2025!!}
```

