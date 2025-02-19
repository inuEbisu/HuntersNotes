---
title: ZJU C程序设计基础与实验
---

针对浙江大学C程课程备考而准备的一些琐碎事物。

## 格式错误笑话之行末不得有多余空格
```c
for(int i = 0; i < n; i ++) printf(" %d" + !i, a[i]);
```
即可对数组 `a[5] = {2, 4, 6, 7, 8}` 顺利输出首尾无空格的 `2 4 6 7 8`。

如果你觉得这很没品，也可以使用 `printf(i ? " %d" : "%d", a[i])`。

另外有一些情况，这里做一个汇总：
| 所需输出（首尾均无空格）| 代码 |
| --- | --- |
| `2 4 6 7 8` | `printf(" %d" + !i, a[i])` |
| `2,4,6,7,8` | `printf(",%d" + !i, a[i])` |
| `2, 4, 6, 7, 8` | `printf(", %d" + !i * 2, a[i])` |

## 读一行字符串并对其进行处理
我觉得用 `gets()` 最方便。书上没有。~~（别管栈溢出了）~~
```c
char in[1000] = {0};
gets(in);
for(int i = 0; in[i] != 0; i ++) {
    // Business logic
}
puts(in);
```

## switch 小去世
```c
int c = 0, k;
for(k = 1; k < 3; k ++) 
    switch(k) {
        default:
            c += k;
            puts("default");
        case 2:
            c ++;
            puts("case 2");
        case 4:
            c += 2;
            puts("case 4");
    }
printf("%d\n", c);
```
输出
```
default
case 2
case 4
case 2
case 4
7
```

## "%04d" 与 "%.4d" 区别
前者控制宽度，后者控制精度。
```c
int a = -42;
printf("%04d", a);  // 输出：-042
printf("%.4d", a);  // 输出：-0042
```

## dangling else
`else` 与最近的、没有被匹配过的 `if` 匹配。

```c
if(expression_1)
    if(expression_2) func1();
else
    if(expression_3) func2();
    else func3();
```
等价于
```c
if(expression_1) {
    if(expression_2) {
        func1();
    } else {
        if(expression_3) {
            func2();
        } else {
            func3();
        }
    }
}
```

## void swap(int &a, int &b)？
编译错误。

C语言不支持引用，引用是 C++ 的特性。

应 `void swap(int *a, int *b)`。

## 实现 int gcd(int a, int a)
辗转相除法。请背板。

~~想念 C++ 的每一天~~ 

```c
int gcd(int a, int b) {
    while (b != 0) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}
```

## 关于 int* a, b
`b` 是 `int`，并非 `int*`。

## 关于 static 静态局部变量
静态局部变量和全局变量一样：
- 存储在静态存储区中；
- 在程序开始运行时初始化，未赋初值则自动赋零；
- 生命周期是整个程序运行期间。

嘛，约等于作用范围有限的全局变量！

## 强制类型转换 double(i)？
`double(i)` 也是 C++ 的。请 `(double) i`。

~~更别写 `static_cast<double>(i)`~~

## 关于 3 <= x <= 5
等价于 `(3 <= x) <= 5`。

并非 $x \in [3, 5]$。这里不是 Python！

## 运算符优先级
似乎灰常重要【

[外部链接](https://note.isshikih.top/cour_note/D1QD_CXiaoCheng/#%E8%BF%90%E7%AE%97%E7%AC%A6%E4%BC%98%E5%85%88%E7%BA%A7%E5%90%8C%E7%BA%A7%E9%81%B5%E5%BE%AA%E7%BB%93%E5%90%88%E6%96%B9%E5%90%91%E8%A7%84%E5%BE%8B)

## 逻辑运算符短路
```c
int n=2,k=0;
while(k++&&++n>2);
printf("%d %d\n",k,n);
```
输出 `0 2`。并非 `0 3`。

## a << 1 与 a <<= 1
```c
int a = 1;
a << 1;
printf("%d", a);
```

> `warning: statement with no effect [-Wunused-value]`

输出 `1`。

## XOR Swap
`a ^= b ^= a ^= b;`

不过仅限整型，且实际上汇编指令比用 `temp` 要多。

## 逗号表达式
`exp_1, exp_2, ..., exp_n`

先计算 `exp_1`，再计算 `exp_2`，……最后计算 `exp_n`；整个表达式的值为 `exp_n` 的值。

```c
int x, y;
for(x = 30, y = 0; x >= 10, y < 10; x --, y ++)
    x /= 2, y += 2;
printf("x = %d, y = %d", x, y);
return 0;
```

> `warning: left-hand operand of comma expression has no effect [-Wunused-value]`

输出 `x = 0, y = 12`。并非 `x = 6, y = 6`。

## 关于 sizeof
人家不是函数啦，人家是运算符。

单位为 bytes。

`sizeof(void*)` 指针占的⼤小，在 32 位架构中是 4，在 64 位架构中是 8。

## 二维数组
若对全部元素都赋了初值，或分行赋初值时列出了所有行，则行长度可以省略。
```c
int a[][3] = {{1}, {4}, {7}}; // Valid
int a[][3] = {1, 2, 3, 4, 5, 6, 7, 8, 9}; // Valid
```

  [1]: https://inuebisu.cn/usr/uploads/2024/12/test1.png
  [2]: https://inuebisu.cn/usr/uploads/2024/12/test1_asm.png
  [3]: https://inuebisu.cn/usr/uploads/2024/12/test2.png
  [4]: https://inuebisu.cn/usr/uploads/2024/12/test2_asm.png
  [5]: https://inuebisu.cn/usr/uploads/2024/12/test3.png
  [6]: https://inuebisu.cn/usr/uploads/2024/12/test3_asm.png