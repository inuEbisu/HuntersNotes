---
comment: true
---

# Lec 8. Dynamic Programming

> Dynamic programming takes practice to perfect.
>
> <p style="text-align: right">—— *Algorithm Illuminated*, [ 美 ] Tim Roughgarden</p>

## Dynamic Programming

适合应用动态规划方法求解的最优化问题应该具备的两个要素：

- 最优子结构

- 子问题重叠

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

## 0-1 Knapsack Problem

0-1 背包问题：已知第 $i$ 个物品的重量 $w_{i}$，价值 $v_{i}$，与背包的总容量 $W$，求所能达到的最大总价值。

设 $f_{i, j}$ 为在只能放前 $i$ 个物品的条件下容量为 $j$ 的背包所能达到的最大总价值，则

$$
f_{i, j} = \max\{f_{i - 1, j}, f_{i - 1, j - w_i} + v_i\}.
$$

可做滚动数组优化，去掉第一维：

$$
f_{j} = \max\{f_j, f_{j - w_i} + v_i\}.
$$

此时注意 $j$ 需要从 $W$ 枚举到 $w_i$，以保证 $f_{i,j}$ 总在 $f_{i, j - w_i}$ 之前被更新。

???+ example

    ```c
    for (int i = 1; i <= n; i++) {
        for (int j = W; j >= w[i]; j--) {
            f[j] = max(f[j], f[j - w[i]] + v[i]);
        }
    }
    ```

!!! info "推荐阅读"

    - [背包 DP - OI Wiki](https://oi-wiki.org/dp/knapsack/)
