# 2025-01-15 题解

## [MoeCTF 2022]寻找黑客的家

https://www.nssctf.cn/problem/3314

* 考点：osint, 信息收集, 地图应用
* 工具：百度地图

1. 放大附件1：看到大招牌“汉明宫”，百度地图搜索“汉明宫”，电话后4位 3085 和图上匹配。
2. 点击位置后，搜索附近，根据附件2，输入关键词：茶百道，得到地址 龙华街道三联社区清泉路星光城A107
3. 对照题目 Flag 规则描述，得到 Flag：`NSSCTF{shenzhen_longhua_qingquan}`

## [MoeCTF 2022]zip套娃 

https://www.nssctf.cn/problem/3313


* 考点：zip 爆破，压缩包密码爆破
* 工具：cargo, zip-password-finder, crunch, python, python itertools
* Linux Shell：sudo, apt update, apt install

### 安装 cargo 和 zip-password-finder

```bash
# install cargo and use tuna as mirror
# ref: https://mirrors.tuna.tsinghua.edu.cn/help/crates.io-index/
sudo apt update && sudo apt install cargo

mkdir -vp ${CARGO_HOME:-$HOME/.cargo}

cat << EOF | tee -a ${CARGO_HOME:-$HOME/.cargo}/config.toml
[source.crates-io]
replace-with = 'mirror'

[source.mirror]
registry = "sparse+https://mirrors.tuna.tsinghua.edu.cn/crates.io-index/"
EOF

# ref: https://github.com/agourlay/zip-password-finder
cargo install zip-password-finder
```

### 解题

```bash
# 默认爆破，找到密码 1235
zip-password-finder -i f.zip
# Targeting file 'fl.zip' within the archive
# Archive encrypted with ZipCrypto - expect a much faster throughput
# Starting 12 workers to test passwords
# Generating passwords with length from 1 to 10 for charset with length 62
# 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz
# Starting search space for password length 1 (62 possibilities)
# Starting search space for password length 2 (3844 possibilities) (62 passwords generated so far)
# Starting search space for password length 3 (238328 possibilities) (3906 passwords generated so far)
# Starting search space for password length 4 (14776336 possibilities) (242234 passwords generated so far)
# Time elapsed: 49ms 992us 292ns
# Password found:1235

# 熟悉常用的爆破参数组合使用
zip-password-finder --minPasswordLen 1 --maxPasswordLen 6 -i f.zip
# Targeting file 'fl.zip' within the archive
# Archive encrypted with ZipCrypto - expect a much faster throughput
# Starting 12 workers to test passwords
# Generating passwords with length from 1 to 6 for charset with length 62
# 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz
# Starting search space for password length 1 (62 possibilities)
# Starting search space for password length 2 (3844 possibilities) (62 passwords generated so far)
# Starting search space for password length 3 (238328 possibilities) (3906 passwords generated so far)
# Starting search space for password length 4 (14776336 possibilities) (242234 passwords generated so far)
# Time elapsed: 50ms 158us 583ns
# Password found:1235

# 解压缩，得到新压缩包文件 fl.zip 和 密码.txt
7z x f.zip -p1235

# 其中 密码.txt 内容如下
# 密码的前七位貌似是1234567
# 后三位被wuliao吃了

zip-password-finder -p dict_of_3chars.txt -i fl.zip
# Targeting file 'fla.zip' within the archive
# Archive encrypted with ZipCrypto - expect a much faster throughput
# Using passwords dictionary "dict_of_3chars.txt" with 238328 candidates.
# Starting 12 workers to test passwords
# Time elapsed: 23ms 296us
# Password found:1234567qwq
```

上面命令参数中的 `dict_of_3chars.txt` 是通过 python 生成的，代码如下：

```python
import itertools
seed = ''

for i in range(ord('a'), ord('z') + 1):
    seed += chr(i)

for i in range(ord('A'), ord('Z') + 1):
    seed += chr(i)

for i in range(0, 10):
    seed += str(i)

res = itertools.product(seed, repeat=3)
for i in res:
    print('1234567' + ''.join(i))
```

也可以通过 `crunch` 生成

```bash
crunch 3 3 -f tools/charset.lst mixalpha-numeric -o crunch_dict.txt
# 然后将 1234567 作为前缀加入到 crunch_dict.txt 中
while read line; do
    echo "1234567$line" >> crunch_dict_new.txt
done < crunch_dict.txt
```

## [FSCTF 2023]最终试炼hhh 

https://www.nssctf.cn/problem/4601

* 考点：PDF隐写, 二进制文件逆序输出, 16进制编辑器, zip伪加密, 压缩包分析
* 工具：wbStego4, wbStego4Open, 大模型 Chat, 豆包
* Linux Shell: file, strings

```bash
file flag
# flag: data
strings flag
# 发现逆序输出的 flag 如下在末尾
# fdp.galf
```

- Ask Doubao: 现在需要你编写一个 python 程序，实现读取二进制文件后，从文件尾开始按照逆序另存写入一个新文件，命名为 flag.data
- Ask Doubao: 使用 python 编程自动将使用伪加密方式加密的 zip 文件设置为不加密模式
	- [remove_fake_encryption.py](tools/remove_fake_encryption.py)
    - 输入 flag.data ，解压后得到无加密设置的 flag.data.temp

```bash
unzip flag.data.temp 
# 直接解压只会得到一个 flag.pdf ，但这个文件打开查看啥也没有看到，推测用到了 PDF 文件隐写
```

Google 一番可知，PDF 隐写提取信息基本只有 wbStego4，但是 wbStego4 只能在 Windows 上运行，macOS 不友好。

https://www.bailer.at/wbstego/

通过 wbStego4Open 解题，实际提取出来的 flag.txt 内容如下，第一个字符并不是 F ，推测是命题人懒得解决或无法解决的信息嵌入 BUG 了，只能依赖于选手根据比赛名称和 Flag 格式规则，自行补全。

```bash
xxd flag.txt
# 00000000: 0253 4354 467b 636d 6467 795f 7979 6473  .SCTF{cmdgy_yyds
# 00000010: 7d                                       }
```

实际提交通过的 Flag: FSCTF{cmdgy_yyds} ，命题描述里也没有提到更改 flag 前缀。题目上写的比赛名称是 FSCTF 。

## [网鼎杯 2022 玄武组]misc999 

https://www.nssctf.cn/problem/2572

* 考点：base62, base换表

题目描述非常简单，一个 txt 文件，内容如下：

```
表 9876543210qwertyuiopasdfghjklzxcvbnmMNBVCXZLKJHGFDSAPOIUYTREWQ
密文 7dFRjPItGFkeXAALp6GMKE9Y4R4BuNtIUK1RECFlU4f3PomCzGnfemFvO
```

观察 `表` ，相比 `base64` 用到的码表，缺了 `+` 和 `/` 。

```bash
# 数字符个数
echo -n '9876543210qwertyuiopasdfghjklzxcvbnmMNBVCXZLKJHGFDSAPOIUYTREWQ' | wc
      0       1      62
```

- [misc999.py](tools/misc999.py)
    - [base62.py](tools/base62.py) Google 搜索得到的 



## [SDCTF 2022]Case64AR 

https://www.nssctf.cn/problem/2378

- 考点：base64, base64换表, base64自定义表, 移位密码, base64变形

```
Someone script kiddie just invented a new encryption scheme. It is described as a blend of modern and ancient cryptographic techniques. Can you prove that the encryption scheme is insecure by decoding the ciphertext below?

Ciphertext: OoDVP4LtFm7lKnHk+JDrJo2jNZDROl/1HH77H5Xv
得到的flag使用NSSCTF{}格式提交。
```

已知比赛 flag 格式为 sdctf{ ，经过 base64 编码之后得到 

c2RjdGZ7

- [case64ar.py](tools/case64ar.py)


