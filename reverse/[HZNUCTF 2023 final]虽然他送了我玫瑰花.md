# [HZNUCTF 2023 final]虽然他送了我玫瑰花

---

## 考点

---

**#花指令**

---

## 思路

---

![[HZNUCTF 2023 final]虽然他送了我玫瑰花_1](./images/%5BHZNUCTF%202023%20final%5D虽然他送了我玫瑰花_1.png)

由可知判断条件只会跳转jz，所以jnz是没用的花指令，把这行指令nop掉再重新编译主函数

![[HZNUCTF 2023 final]虽然他送了我玫瑰花_2](./images/%5BHZNUCTF%202023%20final%5D虽然他送了我玫瑰花_2.png)

然后查看主函数伪代码

![[HZNUCTF 2023 final]虽然他送了我玫瑰花_3](./images/%5BHZNUCTF%202023%20final%5D虽然他送了我玫瑰花_3.png)

这个逻辑是输入29长度的字符串，然后经过函数组funcs_40117E的变换之后再和已有的字符串进行对比来判断flag是否正确，已有的字符串为6CE1CA267159DFE8247A4EFBCE517E7Fh，因为这个程序为小端序，所以是7F7E51CEFB4E7A24E8DF597126CAE16C

函数组的使用是根据字符串索引再模5，再根据顺序来选择函数的使用，下面是函数组中的5个函数

```
int __cdecl sub_401080(int a1)
{
  return a1 ^ 0x19;
}
int __cdecl sub_401090(int a1)
{
  return a1 + 18;
}
int __cdecl sub_4010A0(int a1)
{
  return a1 - 16;
}
int __cdecl sub_4010B0(char a1)
{
  return 2 * (a1 & 0x7F);
}
int __cdecl sub_4010C0(int a1)
{
  return a1 ^ ((unsigned __int8)a1 ^ (unsigned __int8)~(_BYTE)a1) & 0x80;
}
```

由此可以推断出**flag{Wh4t_@_6eaut1fu1_$lower}**