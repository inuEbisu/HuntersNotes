---
comment: true
---

# Qwen3 架构浅析

!!! abstract

    对应 [Lab 5: TinyLLM](https://hpc101.zjusct.io/lab/Lab5-TinyLLM/)。

<!-- !!! quote "WIP" -->

<!-- <object data="./lab5.pdf" type="application/pdf" width="100%" height="800">
    </object> -->

## Decoder Layer Overview

Qwen3 Decoder Layer 是一个标准的 Transformer 的 Decoder 架构，在此基础上 Layer Norm 部分使用了 RMS Norm。

以下是一张简图：

```typst
#import "@preview/cetz:0.4.1"
#import "@preview/note-me:0.5.0": *
#import "@preview/fletcher:0.5.8" as fletcher: diagram, edge, node
#import fletcher.shapes: circle as fletcher_circle, hexagon, house

#set page(width: auto, height: auto, margin: .5cm)

#let body-font = "Source Han Sans SC"

#set text(font: body-font, 12pt)

#figure(
  [
    #let blob(pos, label, tint: white, ..args) = node(
      pos,
      align(center, label),
      width: 28mm,
      fill: tint.lighten(60%),
      stroke: 1pt + tint.darken(20%),
      ..args,
    )

    // #let c(..args) = circle(..args)
    #let circ(pos, tint: white, ..args) = node(
      pos,
      align(center, box(baseline: -0.8em)[$+$]),
      fill: tint,
      stroke: 1pt + black,
      shape: fletcher_circle,
      radius: 2.5mm,
      ..args,
    )

    #diagram(
      spacing: 8pt,
      cell-size: (8mm, 10mm),
      edge-stroke: 1pt,
      edge-corner-radius: 5pt,
      mark-scale: 70%,

      circ((0, 1)),
      edge(),
      blob((0, 2), [Grouped Query\ Attention], tint: orange),
      blob((0, 3.3), [RMS Norm], tint: yellow, shape: hexagon),
      edge(),
      blob((0, 5), [Input], shape: house.with(angle: 30deg), width: auto, tint: red),

      for x in (-.3, -.1, +.1, +.3) {
        edge((0, 2.8), (x, 2.8), (x, 2), "-|>")
      },
      edge((0, 2.8), (0, 4)),
      edge((0, 4), "r,uuu,l", "--|>"),
      edge((0, 1), (0, 0.35), "rr", (2, 4), "r", (3, 3.3), "-|>"),
      edge((3, 4), "r,uuu,l", "--|>"),

      blob((3, 0), [Output], tint: green),
      edge("<|-"),
      circ((3, 1)),
      edge(),
      blob((3, 2), [Feed\ Forward], tint: blue),
      edge(),
      blob((3, 3.3), [RMS Norm], tint: yellow, shape: hexagon),
    )
  ]
)
```

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

以下简单地对比 MHA, MQA 与 GQA：

```typst
#import "@preview/cetz:0.4.1"
#import "@preview/note-me:0.5.0": *
#import "@preview/fletcher:0.5.8" as fletcher: diagram, edge, node
#import fletcher.shapes: circle as fletcher_circle, hexagon, house

#set page(width: auto, height: auto, margin: .5cm)

#let body-font = "Source Han Sans SC"

#set text(font: body-font, 12pt)

#figure(
  [
    #let blob(pos, label, tint: white, ..args) = node(
      pos,
      align(center + horizon, label),
      width: 26pt,
      height: 40pt,
      fill: tint.lighten(60%),
      stroke: 1pt + tint.darken(20%),
      shape: rect,
      corner-radius: 5pt,
      inset: 0pt,
      ..args,
    )

    #let q(pos, label, ..args) = blob(pos, label, tint: color.aqua, ..args)
    #let k(pos, label, ..args) = blob(pos, label, tint: color.red.lighten(35%), ..args)
    #let v(pos, label, ..args) = blob(pos, label, tint: color.orange.lighten(35%), ..args)
    #let t(pos, label) = node(pos, box(label, height: 20pt, width: 100pt), shape: rect, width: 30pt)

    #block(inset: -5pt)

    #diagram(
      spacing: 6pt,
      cell-size: (8mm, 20mm),
      edge-stroke: 1pt,
      edge-corner-radius: 5pt,
      mark-scale: 70%,

      for i in range(4) {
        q((i, 2), [$Q_#(i + 1)$])
        edge("--|>")
        k((i, 1), [$K_#(i + 1)$])
        edge("-")
        v((i, 0.15), [$V_#(i + 1)$])
      },


      for i in range(2) {
        q((5 + 2 * i, 2), [$Q_#(10 * i + 11)$])
        edge("--|>", (5.5 + 2 * i, 1))
        q((6 + 2 * i, 2), [$Q_#(10 * i + 12)$])
        edge("--|>", (5.5 + 2 * i, 1))
        k((5.5 + 2 * i, 1), [$K_#(i + 1)$])
        edge("-")
        v((5.5 + 2 * i, 0.15), [$V_#(i + 1)$])
      },

      for i in range(4) {
        q((10 + i, 2), [$Q_#(i + 1)$])
        edge("--|>", (11.5, 1))
      },
      k((11.5, 1), [$K$]),
      edge("-"),
      v((11.5, 0.15), [$V$]),

      t((1.5, 2.55), [Multi-head]),
      t((6.5, 2.55), [Grouped-query]),
      t((11.5, 2.55), [Multi-query]),
    )
  ],
)
```

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

以下是经典 FFN 与 FFN with GLU 一个简单的对比：

```typst
#import "@preview/cetz:0.4.1"
#import "@preview/note-me:0.5.0": *
#import "@preview/fletcher:0.5.8" as fletcher: diagram, edge, node
#import fletcher.shapes: circle as fletcher_circle, hexagon, house

#set page(width: auto, height: auto, margin: .5cm)

#let body-font = "Source Han Sans SC"

#set text(font: body-font, 12pt)

#figure(
  [
    #let blob(pos, label, tint: white, width: auto, ..args) = node(
      pos,
      align(center, label),
      width: width,
      fill: tint.lighten(60%),
      stroke: 1pt + tint.darken(20%),
      corner-radius: 5pt,
      ..args,
    )

    // #let c(..args) = circle(..args)
    #let circ(pos, tint: white, ..args) = node(
      pos,
      align(center, box(baseline: -0.8em)[$times$]),
      fill: tint,
      stroke: 1pt + black,
      shape: fletcher_circle,
      radius: 2.5mm,
      ..args,
    )

    #let text(pos, label) = node(pos, box(label, height: 20pt, width: 100pt), shape: rect, width: 30pt)

    #let c_i = red
    #let c_o = green
    #let c_u = orange
    #let c_d = blue.lighten(20%)
    #let c_g = yellow
    #let c_s = luma(80%)

    #diagram(
      spacing: 8pt,
      cell-size: (19mm, 8mm),
      edge-stroke: 1pt,
      edge-corner-radius: 5pt,
      mark-scale: 70%,

      blob((0, 6), [Input], shape: house.with(angle: 30deg), tint: c_i),
      edge("-|>"),
      blob((0, 4), [Up projection \ $W_u$ (with bias)], width: 110pt, tint: c_u),
      edge("-"),
      blob((0, 2), [$sigma$], tint: c_s),
      edge("-|>"),
      blob((0, 0.75), [Down projection \ $W_d$ (with bias)], width: 110pt, tint: c_d),
      edge("-|>"),
      blob((0, -0.65), [Output], tint: c_o, corner-radius: 0pt),

      blob((2, 6), [Input], shape: house.with(angle: 30deg), tint: red),
      edge("-|>"),
      edge((2, 6), (2, 4.95), "r,u", "--|>"),
      blob((2, 4), [Up projection \ $W_u$], width: 110pt, tint: c_u),
      edge("-"),
      circ((2, 2)),
      edge("-|>"),
      blob((2, 0.75), [Down projection \ $W_d$], width: 110pt, tint: c_d),
      edge("-|>"),
      blob((2, -0.65), [Output], tint: c_o, corner-radius: 0pt),
      blob((3, 4), [Gate projection \ $W_g$], width: 110pt, tint: c_g),
      edge("--|>"),
      blob((3, 2.8), [$sigma$], tint: c_s),
      edge((3, 2.8), (3, 2), (2, 2), "--|>"),

      text((0, 6.9), [Classic FFN]),
      text((2.4, 6.9), [FFN with GLU]),
    )
  ],
)
```

!!! note
大部分资料认为 GLU 是一种激活函数，但这种说法个人认为有一点奇怪。个人更倾向于将整个 GLU 理解为第一个线性层的替代，而将 GLU 中的 「$\sigma(W_g \cdot x) \odot$」 这一部分理解为 $\sigma$ 的替代。）

SwiGLU 即 $\sigma = \mathrm{SiLU} = x \cdot \mathrm{Sigmoid}(x)$ 的 GLU；于是Qwen-3 中使用了 SwiGLU 的 FFN 实现可以写作

$$
  \mathrm{FFN}(x) = W_d \cdot \mathrm{SwiGLU}(x) = W_d \cdot (\mathrm{SiLU}(W_g \cdot x) \odot (W_u \cdot x)).
$$
