---
comment: true
---

# Qwen3 架构浅析

!!! abstract

    对应 [Lab 5: TinyLLM](https://hpc101.zjusct.io/lab/Lab5-TinyLLM/)。

!!! quote "WIP"

## Decoder Layer Overview

Qwen3 Decoder Layer 是一个标准的 Transformer 的 Decoder 架构，在此基础上 Layer Norm 部分使用了 RMS Norm。

### RMSNorm

首先需要了解 LayerNorm。LayerNorm 主要对每个 token 的特征向量进行归一化计算，其公式为

$$
  \mathrm{LayerNorm}(\mathbf{x}) = \boldsymbol{\gamma} \odot \frac{\mathbf{x} - \hat{\mu}}{\hat{\sigma}} + \boldsymbol{\beta}.
$$

其中
$$
  \hat{\mu} = \frac{1}{d} \sum_{i=1}^{d} x_i,
$$
$$
  \hat{\sigma}^2 = \frac{1}{d} \sum_{i=1}^{d} (x_i - \mu)^2 + \epsilon,
$$

$\epsilon$ 是防止除零的小常数。$\boldsymbol{\beta}, \boldsymbol{\gamma} \in \mathbb{R}^d$ 是可学习的偏移参数与缩放参数，代表着把第 $i$ 个特征的 batch 分布的均值和方差移动到 $\beta_i, \gamma_i$.

RMSNorm 由论文 Root Mean Square Layer Normalization ([arXiv:1910.07467](https://arxiv.org/abs/1910.07467)) 提出，其提出动机是传统的 LayerNorm 运算量比较大；而相比 LayerNorm，RMSNorm 不需要同时计算均值和方差两个统计量，而只需要计算均方根这一个统计量，性能和 LayerNorm 相当的同时节省了运算。RMSNorm 的公式为

$$
  \mathrm{RMSNorm}(\mathbf{x}) = \boldsymbol{\gamma} \odot \frac{\mathbf{x}}{\mathrm{RMS}(\mathbf{x})},
$$

其中 $\mathrm{RMS}(\mathbf{x})$ 是求均方根操作，公式为

$$
  \mathrm{RMS}(\mathbf{x}) = \sqrt{\frac{1}{d} \sum_{i=1}^{d} x_i^2 + \epsilon},
$$

$\epsilon$ 是防止除零的小常数。$\boldsymbol{\gamma} \in \mathbb{R}^d$ 是可学习的缩放参数。

### Grouped Query Attention

首先需要了解 Multi-head Attention 与其变体 Multi-query Attention。MQA 在 MHA 的基础上，让所有的头之间共享同一份 $K, V$，每个头只单独保留了一份 $Q$，节省了大量 $K, V$。

而 GQA 实则是 MHA 与 MQA 的一个中间态，它选择的是使用 $n$ 份 $Q$ 对应一份 $K, V$。也就是说 GQA-1 即为 MHA，GQA-$n$ 即为 MQA。GQA 在节省 $K, V$ 的同时，且在实践中性能仍与经典的 MHA 相近。

### Feed Forward Network with Gated Linear Unit

Transformer 中经典的 FFN 通常由一个含偏置的线性层、一个激活函数 $\sigma$ 再一个含偏置的线性层组成。FFN 的公式可以写作

$$
  \mathrm{FFN}(x) = W_d \cdot \sigma(W_u \cdot x + b_u) + b_d.
$$

!!! note

    所以也可以见到将 FFN 这一组件叫作 MLP 的称呼，例如实验框架中 FFN 类的类名就叫作 `Qwen3MLP`。不过有一点小出入是，在 Transformer 之外一般所说的经典双层 MLP 每一个神经元都会有一个 $\sigma$，于是最后还会有一个 $\sigma$。

而 Gated Linear Unit 可以理解为第一层线性层的一个替代，其核心思想是使用一个带参数的门控层 $\sigma(W_g \cdot x)$ 代替简单激活函数 $\sigma$，从而更精确地控制信息的流动；另外使用 GLU 的 FFN 实现通常会去掉偏置。

GLU 的公式可以写作

$$
  \mathrm{GLU}(x) = \sigma(W_g \cdot x) \odot (W_u \cdot x).
$$

!!! tip
    对比之下，前面提到的经典 FFN 中的第一层线性层可以写作

    $$
        \mathrm{FFN}_1(x) = \sigma(W_u \cdot x + b_u).
    $$

则 FFN with GLU 可以写作

$$
  \mathrm{FFN}'(x) = W_d \cdot \mathrm{GLU}(x) = W_d \cdot (\sigma(W_g \cdot x) \odot (W_u \cdot x)).
$$


!!! note
    大部分资料认为 GLU 是一种激活函数，但这种说法个人认为有一点奇怪。个人更倾向于将整个 GLU 理解为第一个线性层的替代，而将 GLU 中的 「$\sigma(W_g \cdot x) \odot$」 这一部分理解为 $\sigma$ 的替代。）

SwiGLU 即 $\sigma = \mathrm{SiLU} = x \cdot \mathrm{Sigmoid}(x)$ 的 GLU；于是Qwen-3 中使用了 SwiGLU 的 FFN 实现可以写作

$$
  \mathrm{FFN}(x) = W_d \cdot \mathrm{SwiGLU}(x) = W_d \cdot (\mathrm{SiLU}(W_g \cdot x) \odot (W_u \cdot x)).
$$