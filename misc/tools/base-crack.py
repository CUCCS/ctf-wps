import re
from base64 import b64decode


# problem: [FSCTF 2023]base套 https://www.nssctf.cn/problem/4587
def process_data(data):
    try:
        # cat flag.txt| base64 -d | grep -P '[\p{Han}]' -o
        # 删除包含'flag'或汉字字符的部分
        data = re.sub(r'flag|[\u4e00-\u9fa5]', '', data)
        decoded_data = b64decode(data)
        return decoded_data.decode(), True
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return data, False


with open('flag.txt', 'r', encoding='utf-8') as file:
    data = file.read()

iterations = 0

while True:
    data, can_decode = process_data(data)
    iterations += 1
    # 如果无法继续解码，输出结果并结束循环
    if not can_decode:
        print('最终结果:', data)
        print('循环次数:', iterations)
        break
