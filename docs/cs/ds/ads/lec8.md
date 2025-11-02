---
comment: true
---

# Lec 8. Dynamic Programming

> Dynamic programming takes practice to perfect.
>
> <p style="text-align: right">—— *Algorithm Illuminated*, [ 美 ] Tim Roughgarden</p>

## Fibonacci Numbers

[数楼梯](https://www.luogu.com.cn/problem/P1255)问题。

$$
F(n) = F(n - 1) + F(n - 2).
$$

## Ordering Matrix Multiplications

问题：以何种顺序计算 $n$ 个矩阵的乘积，可以使计算时间最小？

假设我们需计算 $n$ 个矩阵 $M_1 \times M_2 \times \cdots \times M_n$ 的乘积，其中 $M_i$ 是一个 $r_{i-1} \times r_i$ 矩阵；计算 $M_i \times M_{i+1}$ 的代价为 $r_{i-1}r_ir_{i+1}$。令 $m_{ij}$ 表示计算 $M_i \times M_{i+1} \times \cdots \times M_j$ 的最优代价，则

$$
m_{ij} = 
\begin{cases} 
0 & \text{if } i = j, \\
\min\limits_{i \leq l < j} \{ m_{il} + m_{(l+1)j} + r_{i-1}r_l r_j \} & \text{if } j > i.
\end{cases}
$$

## Optimal Binary Search Tree

!!! quote "WIP"

## All-Pairs Shortest Path

全源最短路问题：求每对结点之间的最短路。

使用邻接矩阵存图，顶点 $0 \leq i, j < n$。令 $D_{ij}^k$ 表示从 $i$ 到 $j$ 的最短路径长度，且该路径的所有中间顶点（不含端点 $i$ 和 $j$）需来自集合 $\{0, 1, \dots, k\}$；规定 $D_{ij}^{-1} = \text{Cost}_{ij}$。则我们需要的从 $i$ 到 $j$ 的最短路为 $D_{ij}^{N-1}$。其满足状态转移方程

$$
D_{ij}^k = \min\{D_{ij}^{k-1}, D_{ik}^{k-1} + D_{kj}^{k-1}\}.
$$

使用 $k, i, j$ 三层循环实现即可，时间复杂度为 $O(|V|^3)$。

即 Floyd 算法。

!!! info "推荐阅读"

    - OI Wiki: [Floyd 算法](https://oi-wiki.org/graph/shortest-path/#floyd-%E7%AE%97%E6%B3%95)
