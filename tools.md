
## MISC

### 编解码

- [自己 Fork 的 CyberChef](https://github.com/c4pr1c3/CyberChef) 
    - [X] 增加了 `Base91` 编解码支持
    - [X] 已本地容器化 `ghcr.io/gchq/cyberchef:c4pr1c3` ，源代码在在 `$HOME/workspace/ctf/CyberChef/`
- [basecrack](https://github.com/mufeedvh/basecrack) Base编码套娃自动遍历尝试求解
    - [X] 本地部署在 `Conda` 环境中：`Ciphey`
- [Ciphey/Ciphey](https://github.com/Ciphey/Ciphey)
    - [X] 本地部署在 `Conda` 环境中：`Ciphey`
    - [X] 本地 `Docker` 镜像：`docker.io/remnux/ciphey`
- base换表： 
    - [misc/tools/case64ar.py](misc/tools/case64ar.py)
    - [misc/tools/misc999.py](misc/tools/misc999.py)
        - [misc/tools/base62.py](misc/tools/base62.py) Base62 编解码（支持自定义换表）
- 带混淆的 Base 编码
    - [misc/tools/justBase.py](misc/tools/justBase.py) Base64 换表，穷举编码表排列组合，自定义正常解码的停止条件
    - [misc/tools/base-crack.py](misc/tools/base-crack.py) 无关字符过滤，套娃解码，迭代解码

### 压缩包

- [misc/tools/remove_fake_encryption.py](misc/tools/remove_fake_encryption.py) ZIP 伪加密自动解密
- [zip-password-finder](https://github.com/agourlay/zip-password-finder)
    - [X] 本地通过 `cargo` 安装，命令行全局可用

## Web

- [sqlmap](https://sqlmap.org/)
    - [X] 本地部署在 `Conda` 环境中：`pentest`
- [SSTImap](https://github.com/vladko312/SSTImap)
    - [X] 本地部署在 `Conda` 环境中：`pentest` ，进入目录 `$HOME/workspace/ctf/SSTImap/`
- [Yakit](https://yaklang.com/products/download_and_install)
    - [X] 本地图形化界面已安装

## debug

- [mysql + adminer]($HOME/workspace/c4pr1c3/ctf-games/dvwa)
- [pgsql + adminer](stats/docker-compose.yml)


