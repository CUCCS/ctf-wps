# ref: https://www.nssctf.cn/problem/2378 [SDCTF 2022]Case64AR
import base64

base64_str = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
ref_str = "OoDVP4LtFm7lKnHk+JDrJo2jNZDROl/1HH77H5Xv"

for i in range(64):
    ans = ""
    # 遍历ref_str中的每个字符，找到其在base64_str中的位置，加上i后取模64，得到新的字符
    for c in ref_str:
        ans += base64_str[(base64_str.index(c) + i) % 64]

    try:
        print(base64.b64decode(ans).decode())
    except:
        print(end = '')
