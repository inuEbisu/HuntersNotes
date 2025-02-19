---
title: Ch.1 复杂度
---

```py
def fib(n: int):
    if n == 0: return 1
    elif n == 1: return 1
    else return fib(n - 1) + fib(n - 2) 
```
递归求斐波那契数列的时间复杂度为 $O\left(\left(\dfrac{\sqrt{5} + 1}{2}\right)^n\right)$。