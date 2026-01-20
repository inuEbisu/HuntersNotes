---
comment: true
---

# 应试痕迹

备考时留下的一些痕迹。

## 格式错误之行末不得有多余空格

```c
for(int i = 0; i < n; i ++) printf(" %d" + !i, a[i]);
```

即可对数组 `a[5] = {2, 4, 6, 7, 8}` 顺利输出首尾无空格的 `2 4 6 7 8`。

如果你觉得这实在太没品了，也可以使用 `printf(i ? " %d" : "%d", a[i])`。

我们还可以灵活变通：

| 所需输出（首尾均无空格） | 代码                            |
| ------------------------ | ------------------------------- |
| `2 4 6 7 8`              | `printf(" %d" + !i, a[i])`      |
| `2,4,6,7,8`              | `printf(",%d" + !i, a[i])`      |
| `2, 4, 6, 7, 8`          | `printf(", %d" + !i * 2, a[i])` |

## 读一行字符串并对其进行处理

无需考虑安全问题时，最方便的方法是 `gets()`。

```c
char in[1000] = {0};
gets(in);
for(int i = 0; in[i] != 0; i ++) {
    // Business logic
}
puts(in);
```

!!! danger

    `gets()` 不安全，不要在生产代码中使用 `gets()`！

## `switch` Fallthrough

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

```txt
default
case 2
case 4
case 2
case 4
7
```

## `"%04d"` 与 `"%.4d"` 的区别

前者控制宽度，后者控制精度。

```c
int a = -42;
printf("%04d", a);  // -042
printf("%.4d", a);  // -0042
```

## Dangling `else`

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

## `void swap(int &a, int &b)`？

编译错误。

C语言不支持引用，引用是 C++ 的特性。

应 `void swap(int *a, int *b)`。

## 实现 `int gcd(int a, int a)`

辗转相除法。

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

## `int* a, b`

`b` 是 `int`，并非 `int*`。

## `static`

静态局部变量和全局变量一样：

- 存储在静态存储区中；
- 在程序开始运行时初始化，未赋初值则自动赋零；
- 生命周期是整个程序运行期间。

## `double(i)`？

`double(i)` 也是 C++ 的。请 `(double) i`。

## `3 <= x <= 5`

其等价于 `(3 <= x) <= 5`，不是 $x \in [3, 5]$ 的意思。

## 运算符优先级

[IsshikiHugh 的笔记](https://note.isshikih.top/cour_note/D1QD_CXiaoCheng/#%E8%BF%90%E7%AE%97%E7%AC%A6%E4%BC%98%E5%85%88%E7%BA%A7%E5%90%8C%E7%BA%A7%E9%81%B5%E5%BE%AA%E7%BB%93%E5%90%88%E6%96%B9%E5%90%91%E8%A7%84%E5%BE%8B)。应试需要背板。

## 逻辑运算符短路

```c
int n=2,k=0;
while(k++&&++n>2);
printf("%d %d\n",k,n);
```

??? info "Answer"

    ```
    0 2
    ```

    Not `0 3`.

## `a << 1` 与 `a <<= 1`

```c
int a = 1;
a << 1;
printf("%d", a);
```

??? info "Answer"

    > `warning: statement with no effect [-Wunused-value]`

    ```
    1
    ```

## XOR Swap

```c
a ^= b ^= a ^= b;
```

!!! warning

    虽然看起来非常巧妙，但有其局限性：

    - 只有整型可以使用，无法用于浮点数等其他数据类型；
    - 使用 [Compile Explorer](https://godbolt.org/) 可以看到，其汇编指令反而比用 `temp` 中间变量更多。

## 逗号表达式

`exp_1, exp_2, ..., exp_n`

先计算 `exp_1`，再计算 `exp_2`，……最后计算 `exp_n`；整个表达式的值为最后一个表达式 `exp_n` 的值。

```c
int x, y;
for(x = 30, y = 0; x >= 10, y < 10; x --, y ++)
    x /= 2, y += 2;
printf("x = %d, y = %d", x, y);
return 0;
```

??? info "Answer"

    > `warning: left-hand operand of comma expression has no effect [-Wunused-value]`

    ```
    x = 0, y = 12
    ```

    Not `x = 6, y = 6`.

## `sizeof`

`sizeof` 是一个运算符，不是函数；且它是编译时的，不是运行时的。其单位为 bytes。

`sizeof(void*)` 指针占的⼤小，在 32 位架构中是 4，在 64 位架构中是 8。

!!! tip

    可以想一想「X 位架构」的意思是什么。

## 二维数组

若对全部元素都赋了初值，或分行赋初值时列出了所有行，则行长度可以省略。

```c
int a[][3] = {{1}, {4}, {7}}; // Valid
int a[][3] = {1, 2, 3, 4, 5, 6, 7, 8, 9}; // Valid
```
