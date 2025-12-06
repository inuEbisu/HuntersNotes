---
comment: true
---

# ZJUCTF 2024

!!! abstract

    浙江大学 2024 年信息安全校赛。

    - 比赛链接：[ZJUCTF 2024 - ZJU::CTF](https://ctf.zjusec.com/games/4)
    - 比赛时间：2024 年 10 月 15 日 20:00 - 2024 年 10 月 22 日 20:00
    - 成绩：总分数 1435，总排名 33 / 377，浙江大学组内排名 20 / 185

## Crypto

### FIB 1

斐波那契数列矩阵性质应用。题目定义 $\mathit{fib}(n, p) = (f_n, f_{n+1}) \pmod p$。

利用斐波那契数列的矩阵形式：

$$
\begin{pmatrix} f_{n-1} & f_n \\ f_n & f_{n+1} \end{pmatrix} = \begin{pmatrix} 0 & 1 \\ 1 & 1 \end{pmatrix}^n
$$

#### Case 1

已知 $\mathit{fib}(a, p)$ 和 $\mathit{fib}(b, p)$，求 $\mathit{fib}(a+b, p)$。

利用矩阵乘法：

$$
\begin{pmatrix} f_{a+b} \\ f_{a+b+1} \end{pmatrix} = \begin{pmatrix} f_{b-1} & f_b \\ f_b & f_{b+1} \end{pmatrix} \begin{pmatrix} f_a \\ f_{a+1} \end{pmatrix}
$$

#### Case 2

已知 $\mathit{fib}(a, p)$ 和 $k$，求 $\mathit{fib}(ka, p)$。

利用矩阵快速幂：

$$
\begin{pmatrix} f_{ka} \\ f_{ka+1} \end{pmatrix} = \begin{pmatrix} f_{a-1} & f_a \\ f_a & f_{a+1} \end{pmatrix}^{k-1} \begin{pmatrix} f_a \\ f_{a+1} \end{pmatrix}
$$

#### Case 3

已知 $\mathit{fib}(a, p)$ 且 $\mathit{fib}(a+c, p) = (0, 1)$，求 $\mathit{fib}(c, p)$。

$$
\begin{pmatrix} 0 \\ 1 \end{pmatrix} = \begin{pmatrix} f_{a-1} & f_a \\ f_a & f_{a+1} \end{pmatrix} \begin{pmatrix} f_c \\ f_{c+1} \end{pmatrix}
$$

左乘逆矩阵求解。行列式 $\det = f_{a-1}f_{a+1} - f_a^2 = (-1)^a$。由于 $a$ 未知，需分类讨论行列式为 $1$ 或 $-1$，爆破即可。
