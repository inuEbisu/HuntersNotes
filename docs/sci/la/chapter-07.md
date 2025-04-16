---
title: Ch.7 线性空间
---

## 7.2 线性空间
设数域 $P$，集合 $V$，在 $V$ 上定义了封闭的加法与数乘。即：

- $\forall \alpha, \beta \in V,$ 均有 $\alpha + \beta \in V$
- $\forall k \in P,\ \alpha \in V,$ 均有 $k\alpha \in V$

若其满足以下 8 条运算规则，则称 $V$ 为 $P$ 上的**线性空间**。

1. $\alpha + \beta = \beta + \alpha$
2. $(\alpha + \beta) + \gamma = \alpha + (\beta + \gamma)$
3. $\exists \theta \in V,\ \forall \alpha \in V,\ \alpha + \theta = \alpha$
4. $\forall \alpha \in V,\ \exists \beta \in V,\ \alpha + \beta = \theta$
5. $(kl)\alpha = k(l\alpha)$
6. $1 \cdot \alpha = \alpha$
7. $k(\alpha + \beta) = k\alpha + k\beta$
8. $(k + l)\alpha = k\alpha + l\alpha$

如何记忆？其中 1, 2, 3, 4 条关于加法，5, 6 条关于数乘，7, 8 条是数乘对加法的分配律。

## 7.3 线性关系

### 定义
对于 $\beta \in V,$ 若 $\exists k_1, k_2, \cdots, k_s \in P,$ s.t. $\beta = k_1\alpha_1 + k_2\alpha_2 + \cdots + k_s\alpha_s,$ 则称 $\beta$ 可由向量组 $\alpha_1, \cdots, \alpha_n$ **线性表示**。

可见：
1. $\beta$ 可由向量组 $\alpha_1, \cdots, \alpha_n$ 线性表示 $\Leftrightarrow Ax = \beta$ 有解；

2. $\theta$ 可由任意向量组线性表示。

若 $\exists$ 不全为零的 $k_1, \cdots, k_s$ s.t. $k_1\alpha_1 + k_2\alpha_2 + \cdots + k_s\alpha_s = \theta$，则称 $\alpha_1, \alpha_2, \cdots, \alpha_s$ **线性相关**。

可见：
1. $\alpha_1, \alpha_2, \cdots, \alpha_s$ 线性相关 $\Leftrightarrow Ax = \theta$ 有非零解。

### 定理1
$\alpha_1, \alpha_2, \cdots, \alpha_s$ 线性相关 $\Leftrightarrow$ 至少有一个量可以被其他量线性表示。

### 定理2
$\alpha_1, \cdots, \alpha_s$ 线性无关，$\alpha_1, \cdots, \alpha_s, \beta$ 线性相关 $\Leftrightarrow$ $\beta$ 可由 $\alpha_1 \cdots \alpha_s$ 表示，且线性组合唯一。

<!--
$$[\alpha_1, \alpha_2, \cdots, \alpha_s] = [\beta_1, \beta_2, \cdots, \beta_s] \begin{bmatrix} m_{11} & m_{12} & \cdots & m_{1j} \\ m_{21} & m_{22} & \cdots & m_{2j} \\ \vdots & \vdots & \ddots & \vdots \\ m_{s1} & m_{s2} & \cdots & m_{sj} \end{bmatrix}$$
-->

### 定理3

对于两个向量组：(I) $\alpha_1, \cdots, \alpha_r$，(II) $\beta_1, \cdots, \beta_s$，

若 I 可由 II 线性表示，且 $r > s$，则 I 线性相关。

若 I 可由 II 线性表示，且 I 线性无关，则 $r < s$。

### 定理4

I 和 II 可互相线性表示 $\Leftrightarrow$ I 与 II 等价。

## 7.5 极大线性无关组，向量组的秩

### 定义

对于一个向量组 (I) $\alpha_1, \cdots, \alpha_m$，从中挑几个向量出来构成新的向量组：(II) $\alpha_{i_1}, \cdots, \alpha_{i_r} (r \leq m)$，则称 (II) 为 (I) 的部分组。

若 (II)：

1. 线性无关

2. $\forall \alpha_k \in$ (I)，均可由 (II) 线性表示

则称 (II) 为 (I) 的一个极大线性无关组。

一个向量组的极大线性无关组所含向量的个数称为**向量组的秩**。

秩相等 $\Leftrightarrow$ 矩阵等价 $\Leftarrow$ $(\nRightarrow)$ 向量组等价。

## 7.6 基、维数、坐标

### 定义

$V$ 中 $\xi_1, \cdots, \xi_n$ 称为 $V$ 的一组**基**，当且仅当：

1. $\xi_1, \cdots, \xi_n$ 线性无关；
2. $\forall \alpha \in V$，$\alpha$ 可由 $\xi_1, \cdots, \xi_n$ 线性表示。

其中向量个数则称为 $V$ 的**维数**，记作 $\mathrm{dim} V.$

此时有
$$\alpha = x_1\xi_1 + x_2\xi_2 + \cdots + x_n\xi_n = [\xi_1, \cdots, \xi_n] \begin{bmatrix} x_1 \\ \vdots \\ x_n \end{bmatrix} = [\xi_1, \cdots, \xi_n]\boldsymbol{x}$$

其中向量 $\boldsymbol{x}$ 称为 $\alpha$ 在基 $\xi_1, \cdots, \xi_n$ 下的**坐标**。

常用基有：
1. $e_1, e_2, \cdots, e_n$
2. $\mathbb{R}^n$ 的常用基：$e_i$
3. $\mathbb{R}^{m \times n}$ 的常用基：$E_{ij}$（矩阵单位）

可见基是一组有序的极大线性无关组。

### 定理
$\alpha_1, \cdots, \alpha_s$ 线性相关 $\Leftrightarrow R(A_{n \times s}) < s \Leftrightarrow (n=s)~|A| = 0$；

$\alpha_1, \cdots, \alpha_s$ 线性无关 $\Leftrightarrow R(A_{n \times s}) = s \Leftrightarrow (n=s)~|A| \neq 0$。

### 定理1
$r(\alpha_1, \cdots, \alpha_s) = r(X_1, \cdots, X_s)$.

### 如何求线性关系

要求 $\alpha_1, \cdots, \alpha_m$ 的线性关系：
1. 定义 $k_1\alpha_1 + k_2\alpha_2 + \cdots + k_m\alpha_m = \theta.$
2. $A = (\alpha_1, \cdots, \alpha_m)$，求出 $r(A)$ 并与 $m$ 比较。
3. 化为 $(x_1, \cdots, x_m).$ （可选择常用基。）

## 7.7 过渡矩阵、坐标变换公式

### 定义

设 $\dim V = n$, 两组基：

(1) $[\xi_1, \ldots, \xi_n] = A$；

(2) $[\eta_1, \ldots, \eta_n] = B$；

且 $AM = B$；则称 $M$ 为从基 (1) 到基 (2) 的**过渡矩阵**。

### 定理1：坐标变换公式

$\forall \alpha \in V$，$\alpha$ 在 (1) 下坐标为 $X$，
在 (2) 下坐标为 $Y$，
则
$$ X = MY,~ Y = M^{-1}X $$

## 一些总结

### 其一
$A_{n \times n}$ 可逆

$\Leftrightarrow |A| \neq 0$

$\Leftrightarrow \exists B, AB = E \Leftrightarrow \exists B, BA = E$

$\Leftrightarrow A^*$ 可逆

$\Leftrightarrow A$ 可表示为一系列初等变换的乘积

$\Leftrightarrow AX = \theta$ 只有零解

$\Leftrightarrow A$ 的等价标准形为 $E$

$\Leftrightarrow A$ 的行向量组线性无关 $\Leftrightarrow A$ 行满秩

$\Leftrightarrow A$ 的列向量组线性无关 $\Leftrightarrow A$ 列满秩

### 其二

$$\begin{cases}
a_{11}x_1 + a_{12}x_2 + \cdots + a_{1n}x_n = b_1 \\
a_{21}x_1 + a_{22}x_2 + \cdots + a_{2n}x_n = b_2 \\
\vdots \\
a_{m1}x_1 + a_{m2}x_2 + \cdots + a_{mn}x_n = b_m
\end{cases} \Leftrightarrow A_{m \times n}X = \beta$$

$$
\Leftrightarrow [\alpha_1, \alpha_2, \ldots, \alpha_n]\begin{bmatrix} x_1 \\ \vdots \\ x_n \end{bmatrix} = \beta \Leftrightarrow \beta = x_1\alpha_1 + \cdots + x_n\alpha_n
$$

### 其三
$AX = \beta$ 有解

$\Leftrightarrow R(A) = R(\bar{A})$

$\Leftrightarrow \beta$ 可由 $A$ 的列向量组线性表示

$\Leftrightarrow \alpha_1, \ldots, \alpha_n$ 与 $\alpha_1, \ldots, \alpha_n, \beta$ 等价

$\Leftrightarrow R(\alpha_1, \ldots, \alpha_n) = R(\alpha_1, \ldots, \alpha_n, \beta)$

$\Leftrightarrow L(\alpha_1, \ldots, \alpha_n) = L(\alpha_1, \ldots, \alpha_n, \beta)$