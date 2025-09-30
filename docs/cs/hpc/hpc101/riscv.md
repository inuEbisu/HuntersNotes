---
comment: true
---

# RISC-V 向量化

!!! abstract

    对应 [Lab 2.5: 向量化进阶 (RISC-V) - HPC101](https://hpc101.zjusct.io/lab/Lab2.5-RISC-V/)。

## RISC-V 与其 Vector 向量化扩展学习

<!--
!!! note

    这里或许起到了一个备忘录的作用，主要目的是记一下核心概念与参数方便我挑选指令。 -->

### 硬件参数：ELEN 与 VLEN

对于每个支持向量扩展的硬件线程 (hart / hardware thread) 都有如下的两个硬件参数：

- ELEN: 单个数据的最大位宽;
- VLEN: 一个向量寄存器的位宽.

本次实验所使用的 Muse Pi Pro 拥有 32 个 256 位向量寄存器 (`v0`-`v31`)，单个数据的最大位宽是 64-bit (也就是说没有 `int128_t` 这种东西)，所以：

- ELEN = 64;
- VLEN = 256.

### 运行参数：SEW 与 LMUL

- SEW: 指定单个向量元素的位宽 (Selected Element Width)
- LMUL: 向量寄存器个数 (Length Multiplier)

假如我们在 Muse Pi Pro 中希望使用一条指令对 128 个 8-bit 整数进行操作，那么就需要在程序中设置 SEW = 8, LMUL $= 128 \times 8 \div 256 = 4$.

### 动手

考虑一种常见的对连续数组进行操作的情形，也即形如这样的一个循环：

```cpp
size_t vl = __riscv_vsetvlmax_e32m1(); // SEW = 32, LMUL = 1
for (size_t i = 0; i < N; i += vl) {
    vl = __riscv_vsetvl_e32m1(N - i);
    // process vl elements
}
```

查阅 Intrinsic Viewer 可以知道，`vsetvl` 是这样的一个逻辑：

```cpp
vlmax = vlmax(e32, m1);
if (avl <= vlmax) {
  return avl;
} else if (vlmax < avl < vlmax*2) {
  return /* implementation-defined number in [ceil(avl/2), vlmax] */;
} else {
  return vlmax;
}
```

这里使用 `vsetvl` 系列指令动态设置 `vl` 的值，这是运行时的；所以即使机器的 VLEN 不同，数组总长度不同，都可以完美地处理数组尾部的元素。

!!! info

    这里这个 Implementation-defined feature 的原因是给尾部处理一个负载均衡。例如我们考虑 `vlmax = 8` 且剩下 9 个元素的情况，这里就允许了 5 + 4 的操作，会比 8 + 1 效率略高一点；当然，不实现这个 feature，直接返回一个 `vlmax`，也没有问题。

## 使用 RVV Intrinsic 实现整数矩阵乘法

!!! note

    在 RVV 的设计中，「数据类型」和「操作」是解耦的。

### 基础实现

这里提供的 `naive_gemm` 和 Lab2 中的是一样的。算一个 $A B^T = C$，数据类型为 `uint8_t * int8_t -> int32_t`。

前面提到的 `for` 循环是 RVV Intrinsic 向量化的惯常写法。查阅 Intrinsics Viewer，选用一些 Intrinsics，使用类似的思路进行向量化即可。

### 性能优化

使用循环展开等常见优化手段。

## SpaceMiT IME 矩阵扩展学习

参考资料：

- [SpaceMiT IME Extension Spec](https://github.com/space-mit/riscv-ime-extension-spec/releases/download/v0429/spacemit-ime-asciidoc.pdf)

VLEN = 256；根据文档，$copy = 1$，于是 $M = 4, N = 4, K = 8$。

事实上该指令就是做了一个 $A_{4 \times 8} B_{4 \times 8}^T = C_{4 \times 4}$。

??? example

    通过如下测试代码的执行结果可以观察得很清楚。
    ```cpp
    #include <algorithm>
    #include <iomanip>
    #include <iostream>
    #include <riscv_vector.h>
    #include <stdint.h>
    #include <type_traits>
    #include <vector>

    // Simple pretty printers
    template <typename T> void print_matrix(const T *matrix, int rows, int cols, const std::string &name, int width = 4) {
        std::cout << name << " (" << rows << "x" << cols << "):\n";
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                if constexpr (std::is_same<T, int32_t>::value) {
                    std::cout << std::setw(std::max(width, 8)) << static_cast<int64_t>(matrix[i * cols + j]);
                } else {
                    std::cout << std::setw(width) << static_cast<int>(matrix[i * cols + j]);
                }
            }
            std::cout << '\n';
        }
        std::cout << '\n';
    }

    // Wrap a single vmadotus call that interprets:
    // - vs1: 4x8 uint8
    // - vs2: 4x8 int8 (vmadotus uses vs2^T internally)
    // Produces a 4x4 int32 block accumulated into vd (zero-initialized here).
    static inline void vmadotus_4x8_4x8(const uint8_t *A4x8, const int8_t *B4x8, int32_t *C4x4) {
        // Destination: 16 int32 elements => e32, LMUL=2 (occupies 2 vector registers,
        // 512 bits total)
        size_t vl32 = __riscv_vsetvl_e32m2(16);
        vint32m2_t vd = __riscv_vmv_v_x_i32m2(0, vl32); // zero accumulators

        // Sources: 32 int8/uint8 elements => e8, LMUL=1
        size_t vl8 = __riscv_vsetvl_e8m1(32);
        vuint8m1_t va = __riscv_vle8_v_u8m1(A4x8, vl8);
        vint8m1_t vb = __riscv_vle8_v_i8m1(B4x8, vl8);

        // Ensure e8,m1 is active when issuing vmadotus (operands are 8-bit)
        (void)__riscv_vsetvl_e8m1(32);

        // Call SpaceMiT IME vmadotus: vd += va(4x8) * vb(8x4), interpreting the 32B
        // vectors as those tiles
        asm volatile("vmadotus %[VC], %[VA], %[VB]\n" : [VC] "+vr"(vd) : [VA] "vr"(va), [VB] "vr"(vb) : "memory");

        // Store result back as 16 int32 values in row-major 4x4
        vl32 = __riscv_vsetvl_e32m2(16);
        __riscv_vse32_v_i32m2(C4x4, vd, vl32);
    }

    // Scalar reference: C = A(4x8) * B(4x8)^T => C[i,j] = dot(A[i,:], B[j,:])
    static inline void ref_gemm_4x4_from_tiles_ATxBT(const uint8_t *A4x8, const int8_t *B4x8, int32_t *C4x4) {
        for (int i = 0; i < 4; ++i) {
            for (int j = 0; j < 4; ++j) {
                int32_t sum = 0;
                for (int k = 0; k < 8; ++k) {
                    sum += static_cast<int32_t>(A4x8[i * 8 + k]) * static_cast<int32_t>(B4x8[j * 8 + k]);
                }
                C4x4[i * 4 + j] = sum;
            }
        }
    }

    int main() {
        // Prepare a 4x8 (row-major) uint8 A tile and an 8x4 (row-major) int8 B tile
        // Note: vmadotus expects vs2 to be the transposed view; an 8x4 row-major
        // buffer matches that requirement here.
        alignas(32) uint8_t A[4 * 8] = {
            1, 2, 3, 4, 5, 6, 7, 8,
            9, 10, 11, 12, 13, 14, 15, 16,
            17, 18, 19, 20, 21, 22, 23, 24,
            25, 26, 27, 28, 29, 30, 31, 32,
        };

        // B as a 4x8 tile (row-major). This matches what vmadotus expects for vs2
        // (it will use B^T internally).
        alignas(32) int8_t B[4 * 8] = {
            1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, -1, 0, -1, 2, 1, 0,
            2, -1, 0, 1, 0, 1, 1, -1,
            1, 0, 2, 1, -1, 1, 0, 2,
        };

        alignas(32) int32_t C_ref[4 * 4] = {0};
        alignas(32) int32_t C_vmadot[4 * 4] = {0};

        // Print inputs
        print_matrix<uint8_t>(A, 4, 8, "A (uint8, 4x8)");
        print_matrix<int8_t>(B, 4, 8, "B (int8, 4x8)");

        // Compute scalar reference and vmadotus result
        ref_gemm_4x4_from_tiles_ATxBT(A, B, C_ref);
        vmadotus_4x8_4x8(A, B, C_vmadot);

        // Show results
        print_matrix<int32_t>(C_vmadot, 4, 4, "C_vmadotus (int32, 4x4)", 8);
        print_matrix<int32_t>(C_ref, 4, 4, "C_ref   (int32, 4x4)", 8);

        // Quick check
        bool ok = true;
        for (int i = 0; i < 16; ++i)
            ok &= (C_ref[i] == C_vmadot[i]);
        std::cout << "Match: " << (ok ? "YES" : "NO") << "\n\n";

        // Explain what vmadotus did for one element
        std::cout << "Explanation (one cell): C[0,0] = dot(A[0,:], B[0,:])\n";
        std::cout << "                               = ";
        for (int k = 0; k < 8; ++k) {
            std::cout << (int)A[0 * 8 + k] << "*" << (int)B[0 * 8 + k];
            if (k != 7)
                std::cout << " + ";
        }
        std::cout << " = " << C_vmadot[0] << "\n";

        return ok ? 0 : 1;
    }
    ```

## 使用 SpaceMiT IME 指令扩展实现整数矩阵乘法

### 基本实现

我们可以看到 `vmadot` 指令可以帮助我们完成形如 $A_{4 \times 8} B_{4 \times 8}^T = C_{4 \times 4}$ 的乘法，所以在计算原理上直接使用分块矩阵乘法就好了。

访存上，我们应当如何从 $A$ 中读取这样一块 $4 \times 8$ 的矩阵到寄存器呢？如图，其中每一个格子为一个 `uint8_t`，$A$ 的形状为 $12 \times 32$。

```typst
#import "@preview/cetz:0.4.1"

#set page(width: auto, height: auto, margin: .5cm)

#figure(
  cetz.canvas(
    {
      import cetz.draw: *
      let stress = green.lighten(80%)

      rect((0, 12), (8, 8), fill: stress)
      grid(
        (0, 0),
        (32, 12),
      )
    },
    length: 8pt,
  ),
)
```

用 Strided Load 的想法来看，我们需要每 256 位读入连续的 64 位。那么可以设置 SEW = 64, Stride = 256。可以选用 `__riscv_vlse64_v_u64m1` 这个 Intrinsic 来进行访存。

### 性能优化

使用循环展开等常见优化手段。
