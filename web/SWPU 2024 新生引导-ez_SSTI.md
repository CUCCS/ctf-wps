## 基本信息  

- 题目名称：SWPU 2024 新生引导-ez_SSTI  
- 题目链接：https://www.nssctf.cn/problem/5808
- 考点清单：SSTI、Flask  
- 工具清单：Fenjing  
- Payloads：Fenjing  

### 解题思路  

从题目提示可以看出，这是一道与 SSTI（服务器端模板注入）相关的题目。  

![](images/SWPU%202024%20%E6%96%B0%E7%94%9F%E5%BC%95%E5%AF%BC-ez_SSTI-test.png)  

此外，题目中特别提到了 `fenjing` 这个工具，这表明我们可以借助 `fenjing` 来分析和利用 SSTI 漏洞。  

### 过程和结果记录  

首先，使用 `fenjing` 进行检测，我们需要进行适当的配置。  

![](images/SWPU%202024%20%E6%96%B0%E7%94%9F%E5%BC%95%E5%AF%BC-ez_SSTI-fenjing.png)  

通过 `fenjing` 的自动化分析，我们成功识别了 SSTI 漏洞，并利用该工具执行了相应的 payload，最终成功获取 flag。  

### 总结  

- `fenjing` 作为专门针对 Flask SSTI 的工具，可以高效识别和利用漏洞，极大地简化了测试流程。  
- 在 CTF 实战中，适当使用自动化工具可以事半功倍，但同时理解其底层原理至关重要，否则容易成为“脚本小子”，无法灵活应对不同场景的题目。