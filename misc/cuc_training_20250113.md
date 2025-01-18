# 2025-01-13 题解

## [LitCTF 2023]404notfound (初级) 

https://www.nssctf.cn/problem/3881

* 考点：图片隐写, EXIF, 编码分析, 二进制文件分析, 可打印字符串提取
* 工具：Linux, strings, grep
* Linux shell: strings, grep

```bash
strings 1.png | grep -i ctf
# <rdf:RDF xmlns:rdf='LitCTF{Its_404_but_1ts_n0t_a_page}yntax-ns#'>
#     <rdf:li xml:lang='x-default'>LitCTF_Logo - 8</rdf:li>
```

## [LitCTF 2023]What_1s_BASE (初级) 

https://www.nssctf.cn/problem/3879

* 考点：编码分析, base64, base家族编码
* 工具：ciphey, base64, Linux 管道操作, conda, pypi
* Linux shell: |, base64


```bash
# 建议将 pypi 类工具统一使用 conda 管理起来
ciphey -t "TGl0Q1RGe0tGQ19DcjR6eV9UaHVyM2RheV9WX21lXzUwfQ=="
# Possible plaintext: 'LitCTF{KFC_Cr4zy_Thur3day_V_me_50}'

echo -n 'TGl0Q1RGe0tGQ19DcjR6eV9UaHVyM2RheV9WX21lXzUwfQ==' | base64 -d
# LitCTF{KFC_Cr4zy_Thur3day_V_me_50}
```

## [HDCTF 2023]hardMisc 

https://www.nssctf.cn/problem/3796

* 考点：编码分析, base64, base家族编码
* 工具：ciphey, base64, Linux 管道操作, conda, pypi
* Linux shell: file, base64, tail, strings, unzip, 7z, ls

```bash
unzip 0.zip && strings emoji.png | tail -n 1 | base64 -d
# HDCTF{wE1c0w3_10_HDctf_M15c}
```

## [LitCTF 2023]Hex？Hex！(初级)  

https://www.nssctf.cn/problem/3887

* 考点：编码分析, hexdump, unhexlify 
* 工具：ciphey, python, CyberChef

```bash
# 工具-1 ciphey
ciphey 4c69744354467b746169313131636f6f6c6c616161217d
# Possible plaintext: 'LitCTF{tai111coollaaa!}' (y/N): y
# ╭────────────────────────────────────────────────────╮
# │ The plaintext is a Capture The Flag (CTF) Flag     │
# │ Formats used:                                      │
# │    hexadecimalPlaintext: "LitCTF{tai111coollaaa!}" │
# ╰────────────────────────────────────────────────────╯

# 工具-2 CyberChef

# 工具-3 python
import binascii

hex_str = '4c69744354467b746169313131636f6f6c6c616161217d'

print(binascii.unhexlify(hex_str).decode('utf-8'))

```

## [LitCTF 2023]Is this only base?  https://www.nssctf.cn/problem/3968

> macos M系列芯片无法安装 ciphey，会报错 ModuleNotFoundError: No module named 'distutils.msvccompiler'

* 考点：栅栏密码, Rail Fence Cipher, 凯撒密码, Caesar, ROT3, shell 单引号和双引号区别
* 工具：docker, ciphey, python, CyberChef

> 新手提示：学会如何配置 Docker 的镜像加速器以成功下载镜像。

- Caesar Cipher == ROT3
- Caesar Box Cipher 是一种基于表格（方阵）的加密方法。它的加密过程是先将明文按照一定的规则排列成一个方阵（例如，将明文按行写入一个矩形表格中）。注意，这不是 Caesar Cipher 的变种，而是一种独立的加密方法。

题目信息如下：

```
SWZxWl=F=DQef0hlEiSUIVh9ESCcMFS9NF2NXFzM
今年是本世纪的第23年呢
```

观察密文中有等号，猜测可能是 base64 编码，但是位置不对，继续猜测可能是栅栏密码，尝试使用 CyberChef 解密。在 CyberChef 中逐个 key 遍历可以发现 output 不断变化，直到 key 为 23 时，发现输出像是 base64 编码结果了：SWZxWlFDe0liUV9ScF9FNFMzX2NSMCEhISEhfQ==

这里的 23 刚好又符合题目中的提示 23 ，继续使用 `From Base64` 模块进行解码，得到输出 `IfqZQC{IbQ_Rp_E4S3_cR0!!!!!}` 。

这个输出结果从格式上来看非常像是一个 CTF 的 flag，但是 flag 前缀不对，尝试使用 ciphey 进行一把梭自动解密。

```bash
# docker
docker pull remnux/ciphey
docker run -it --rm remnux/ciphey ciphey -t 'IfqZQC{IbQ_Rp_E4S3_cR0!!!!!}'
```

```bash
# 注意在 bash 中 !! 表示上一条命令，所以需要转义或者使用单引号避免代码执行
ciphey -t 'IfqZQC{IbQ_Rp_E4S3_cR0!!!!!}'
# Possible plaintext: 'IfqZQC{IbQ Rp EASE cRO!!!!!}' (y/N): n
# Possible plaintext: 'LitCTF{LeT_Us_H4V3_fU0!!!!!}' (y/N): y
# ╭──────────────────────────────────────────────────────╮
# │ The plaintext is a Capture The Flag (CTF) Flag       │
# │ Formats used:                                        │
# │    caesar:                                           │
# │     Key: 23Plaintext: "LitCTF{LeT_Us_H4V3_fU0!!!!!}" │
# ╰──────────────────────────────────────────────────────╯
```

- CyberChef https://gchq.github.io/CyberChef/#recipe=Rail_Fence_Cipher_Decode(23,0)From_Base64('A-Za-z0-9%2B/%3D',true,false)ROT13(true,true,true,3)&input=U1daeFdsPUY9RFFlZjBobEVpU1VJVmg5RVNDY01GUzlORjJOWEZ6TQ&oeol=CR

## [LitCTF 2023]就当无事发生 https://www.nssctf.cn/problem/3862 

* 考点：github.io 对应仓库路径转换, git 历史记录搜索
* 工具：git
* Linux shell: git grep, git rev-list, shell 子命令

- https://ProbiusOfficial.github.io --> https://github.com/ProbiusOfficial/ProbiusOfficial.github.io 

```bash
git clone https://github.com/ProbiusOfficial/ProbiusOfficial.github.io
cd ProbiusOfficial.github.io
git grep -i "nssCTF{" $(git rev-list --all)

# 根据比赛名称 LitCTF 2023，搜索变更历史记录中是否包含 LitCTF
git grep -i "LitCTF{" $(git rev-list --all) # 试一下所有输出结果即可
# f04fe251bf8811324d4e71cd87b4b15581358490:2023/04/29/什么是flag呢/index.html:<p>Flag LitCTF{g1thub_c0mmit_1s_s0_us3ful}</p>
# f04fe251bf8811324d4e71cd87b4b15581358490:local-search.xml:    <content type="html"><![CDATA[<p>Flag是什么呢LitCTF2023开始了是怎么回事呢？Flag是什么呢相信大家都很熟悉，但是Fla>
# cf96afe7a2adec97b5d64e2acb7d58e70ffec3cb:2023/03/14/Flag-where/index.html:    <meta name="description" content="LitCTF{You_kn0walot_4bout_G1thub}">
# cf96afe7a2adec97b5d64e2acb7d58e70ffec3cb:2023/03/14/Flag-where/index.html:<meta property="og:description" content="LitCTF{You_kn0walot_4bout_G1thub}">
# cf96afe7a2adec97b5d64e2acb7d58e70ffec3cb:2023/03/14/Flag-where/index.html:                <p>LitCTF{You_kn0walot_4bout_G1thub}</p>
# cf96afe7a2adec97b5d64e2acb7d58e70ffec3cb:index.html:          LitCTF{You_kn0walot_4bout_G1thub}
# cf96afe7a2adec97b5d64e2acb7d58e70ffec3cb:local-search.xml:    <content type="html"><![CDATA[<p>LitCTF{You_kn0walot_4bout_G1thub}</p>]]></content>
```


