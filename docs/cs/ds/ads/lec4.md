---
comment: true
---

# Lec 4: Leftist Heaps and Skew Heaps

## Skew Heaps

### Merge

课程中给出的 merge 操作定义：Always swap the left and right children **except** the largest of all the nodes on the right paths doesn’t have its children swapped. No Npl.

课程之外的大部分实现没有这个 except 的要求，这可能导致混乱，勿混淆。

!!! note

    一种快速 merge 的旁门左道：

    1. 先提出两个 heap 的 right path。
    2. 合并这两条 right path，作为新 heap 的 left path。
    3. 写出剩余的部分（原样挂上剩余的子树）。

    注意合并后 path 的最后一个节点，有且只有以下两种情况：

    - 最后一个节点有左孩子，此时左孩子不要动。这是由于陈越姥姥的 Slides 中定义里的 except。
    - 最后一个节点没有孩子。

    最后一个节点不可能有右孩子，因为一旦有右孩子它就不会是最后一个节点。

    看以下这张图感受：

    <figure class="md-figure">
        <img src="lec4/merge_skew_heaps.png" alt="lec4/merge_skew_heaps.png" />
        <figcaption>两种例子分别对应两种情况。第一个例子中合并后 35 仍然在 18 的左边，没有去到 18 的右边。</figcaption>
    </figure>
