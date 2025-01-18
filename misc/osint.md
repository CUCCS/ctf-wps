
## [KPCTF 2024 初赛]小明的旅游日记

- 题目链接: https://www.nssctf.cn/problem/5777
- 考点清单：以图搜图, 文字推理, uuid-v5, AI 辅助代码生成

### 技巧总结

- 尝试了直接将 `题目 PDF` 上传到豆包、通义千问、Kimi、智谱清言和 ChatGPT ，但均未能直接给出正确答案。
- 百度搜索在搜索国内城市卫星图时的效果好于 Google。利用百度以图搜索功能确认每一个火车站信息，结合文字描述进一步确认火车站信息
- 根据火车站信息和每一段文字描述中提到的“约束条件信息”查询火车时刻表，找到满足条件的唯一车次信息
- 使用大模型生成 python 代码满足 flag 生成要求：`使用 DNS 命名空间的 uuid v5 算法` 

```python
import uuid

input_str = "福州站_G1672_杭州东站_G7364_上海虹桥站_G18_南京南站_G28_北京南站"
namespace = uuid.NAMESPACE_DNS
result_uuid = uuid.uuid5(namespace, input_str)

# 字符串拼接格式化输出 NSSCTF{result_uuid}
print("NSSCTF{%s}" % result_uuid)

```

