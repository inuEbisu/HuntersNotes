---
comment: true
---

# Lec 8. Dynamic Programming

> Dynamic programming takes practice to perfect.
>
> <p style="text-align: right">—— *Algorithm Illuminated*, [ 美 ] Tim Roughgarden</p>

## Ordering Matrix Multiplications

!!! quote "WIP"

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
