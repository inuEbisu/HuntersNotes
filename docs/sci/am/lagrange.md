---
title: 拉格朗日力学粗略
---

## 拉格朗日关系
前置知识是达朗贝尔原理，我不会. 总之我们通过魔法能得到两个基本关系式：
$$
\frac{\partial \dot {\mathbf r} _i}{\partial \dot q_\beta}
= \frac{\partial {\mathbf r} _i}{\partial q_\beta}
$$

$$
\frac{\partial}{\partial q_\beta} \frac{\mathrm{d} \mathbf{r}_i}{\mathrm{d}t}
= \frac{\mathrm{d}}{\mathrm{d}t} \frac{\partial\mathbf{r}_i}{\partial q_\beta}
$$

## 拉格朗日量
对于没有电磁场的非相对论质点系统，其拉格朗日量为
$$ L = T - V $$
其中 $T$ 是系统的总动能，$V$ 是系统的势能. 

## 拉格朗日方程
通过魔法可知，主动力全是保守力情况下的完整系统的拉格朗日方程为
$$
\frac{\mathrm{d}}{\mathrm{d}t}\frac{\partial L}{\partial \dot{q}_\alpha} 
= \frac{\partial L}{\partial q_\alpha}
$$
拉格朗日方程告诉我们：写下 $L$，再写下这个式子，就可以没有什么阻碍地算出系统的运动方程了！
## 广义动量
定义广义动量 $p_\alpha = \frac{\partial L}{\partial \dot{q}_\alpha}$，广义力 $Q_\alpha = \frac{\partial L}{\partial q_\alpha}$，
则拉格朗日方程是在说
$$ \frac{\mathrm{d}p_\alpha}{\mathrm{d}t} = Q_\alpha $$
即拉格朗日方程可读作「广义动量的时间变化率等于广义力」.

广义坐标、广义力与广义动量的内涵很丰富，以下举几例（也是为后文做铺垫）. 

### 整体平移
如果某一广义坐标 $q_\beta$ 反映力学系统的整体平移，其平移方向沿着单位矢量 $\mathbf n$，（此时 $q_\beta$ 具有长度的量纲，）即
$$
\mathbf{r}_i(q, q_\beta + \mathrm{d}q_\beta, t) = \mathbf{r}_i(q, q_\beta, t) + \mathrm{d}q_\beta \mathbf{n}
$$
故
$$
\frac{\partial \mathbf{r}_i}{\partial q_\beta} = \mathbf{n}
$$
相应的广义动量
$$
p_\beta
= \frac{\partial L}{\partial \dot q_\beta}
= \frac{\partial T}{\partial \dot q_\beta}
= \frac{\partial}{\partial \dot q_\beta}  \sum_{i} \frac{1}{2} m_i \dot{\mathbf{r}}_i \cdot \dot{\mathbf{r}}_i
= \sum_{i} m_i \dot{\mathbf{r}}_i \cdot \frac{\partial \dot{\mathbf{r}}_i}{\partial \dot q_\beta}
$$
代入第一条拉格朗日关系，则
$$
p_\beta
= \sum_{i} m_i \dot{\mathbf{r}}_i \cdot \frac{\partial {\mathbf{r}}_i}{\partial q_\beta}
= \mathbf{n} \sum_{i} m_i \dot{\mathbf{r}}_i
$$
即广义动量 $p_\beta$ 是力学系统的动量在 $\mathbf{n}$ 方向的分量.

那么相应的广义力
$$
Q_\beta
= \sum_{i} \mathbf{F}_i \cdot \frac{\partial \mathbf{r}_i}{\partial q_\beta}
= \sum_{i} \mathbf{F}_i \cdot \mathbf{n}
$$
即广义力 $Q_\beta$ 是主动力之和在 $\mathbf n$ 方向的分量.

### 整体转动
如果某一广义坐标 $q_\beta$ 反映力学系统的整体转动，其转动轴沿着单位矢量 $\mathbf n$，（此时 $q_\beta$ 具有角度的量纲，）即
$$
\mathbf{r}_i(q, q_\beta + \mathrm{d} q_\beta, t) = \mathbf{r}_i(q, q_\beta, t) + \mathrm{d}q_\beta \mathbf{n} \times \mathbf{r}_i(q, q_\beta, t)
$$
则
$$
\frac{\partial \mathbf{r}_i}{\partial q_\beta} = \mathbf{n} \times \mathbf{r}_i
$$
那么相应的广义动量 $p_\beta$ 即为力学系统的角动量 $\mathbf{L}$ 在 $\mathbf n$ 方向的分量，相应的广义力 $Q_\beta$ 是主动力对于 $\mathbf n$ 轴的力矩.

我自己推过了，不太想写了同理可得，读者自证不难.jpg（$\LaTeX$的废话怎么跟 Java 一样多！）

## 广义动量积分
$L$ 如果与某个广义坐标 $q_\beta$ 无关，则
$$ \frac{\mathrm{d}p_\beta}{\mathrm{d}t} = Q_\beta=\frac{\partial L}{\partial q_\beta} = 0 $$
于是
$$ p_\beta = C $$
这叫做广义动量积分。

## 广义能量积分

> To-do...

## 诺特定理初步

### 平移对称与动量守恒
如果此时的 $q_\beta$ 反映力学系统的整体平移，其平移方向沿着单位矢量 $\mathbf n$，那么 $L$ 与系统在 $\mathbf n$ 方向上的整体平移无关，此时我们称其平移对称. 

之前我们提到，此时 $q_\beta$ 对应的广义动量 $p_\beta$ 是力学系统的动量在 $\mathbf{n}$ 方向的分量. 

而我们知道 $p_\beta = C$，于是力学系统在 $\mathbf n$ 方向上动量守恒.

整体平移对称下广义动量积分归结于动量守恒定律.

### 旋转对称与角动量守恒
同理.

### 时间平移对称与能量守恒

> To-do...

### 诺特定理
事实上，对于任何一种在坐标连续变换下系统的哈密顿作用量的不变性都有相应的运动积分, 此即**诺特定理**.