---
comment: true
---

# Lec 7. Divide and Conquer

## Divide and Conquer

1. Divide;
2. Conquer;
3. Combine.

故其通常满足形如下式的式子：

$$
T(n) = a T(\frac{n}{b}) + f(n).
$$

## The Closest Points Problem

!!! quote "WIP"

## The Master Theorem

!!! quote "WIP"

## K-way Merge Sort

在 2-way Merge 操作中我们使用了双指针法；同理，在 K-way Merge 操作中我们可使用 $k$ 指针法，每次从 $k$ 个指针中取出最小值。

朴素实现下每次取出最小值的操作是 $O(k)$。我们可以考虑维护一个堆（或锦标赛树），则每次取出最小值的时间复杂度为 $O(\log{k})$。设 $k$ 个数组共有 $n$ 个元素，则 K-way Merge 操作的总时间复杂度为 $O(n \log{k})$。

若 $k$ 为常数，设整个 K-way Merge Sort 过程的时间为 $T(n)$，则

$$
\begin{align*}
  T(n) &= k T(\frac{n}{k}) + O(n \log{k}) \\
       &= k T(\frac{n}{k}) + O(n), \\
\end{align*}
$$

由主定理，$T(n) = O(n \log{n})$。

若我们关心 $k$ 的影响，设整个 K-way Merge Sort 过程的时间为 $T(n, k)$，则

$$
T(n, k) = k T(\frac{n}{k}, k) + O(n \log{k}).
$$

此时主定理不适用，我们需要画递归树进行求解。

递归树的高度 $h = \log_{k}{n}$，第 $i$ 层（根节点为第 0 层）有 $k^i$ 个子问题，每个子问题的工作量为 $O(\frac{n}{k^i} \log{k})$。

故总时间

$$
\begin{align*}
  T(n, k) &= \sum_{i = 0}^{h} k^i \cdot O(\frac{n}{k^i} \log{k}) \\
          &= \sum_{i = 0}^{h} O(n \log{k}) \\
          &= \log_{k}{n} \cdot O(n \log{k}) \\
          &= \frac{\log{n}}{\log{k}} \cdot O(n \log{k}) \\
          &= O(n \log{n}).
\end{align*}
$$

相较于二路，使用 $k$ 路的好处在于递归树变矮，坏处在于每一层的合并工作变重。这里我们看到二者恰好抵消，最终总时间 $T(n, k) = O(n \log{n})$，与 $k$ 无关。

!!! tip

    在 In-Memory Sort 中，K-way Merge Sort 的常数很大，因为其需要维护一个最小堆。

    K-way Merge Sort 通常用于 External Sort：当数据在硬盘上时，算法的瓶颈在于硬盘 I/O（相比之下在内存中维护一个最小堆的成本可忽略不计），而树高 $h$ 决定了算法需要完整读写数据多少遍；此时我们希望减小树高 $h$，为此我们应使用大 $k$。
