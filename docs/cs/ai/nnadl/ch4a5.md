---
comment: true
---

# Ch 4 & 5. Theoretical Universality & Practical Instability

## Universality Theorem

A neural network with even a single hidden layer can approximate any continuous function to any desired accuracy.

It proves that a solution exists for almost any problem (translation, vision, etc.), though it doesn't guarantee that gradient descent will easily find it.

## The Unstable Gradient

<div align="center"><img alt="ch4a5/deep_network.png" src="ch4a5/deep_network.png"/></div>

The gradient in early layers is calculated via the Chain Rule, resulting in a product of terms from all subsequent layers:

$$\delta^l = \Sigma'(z^l)(w^{l+1})^T \Sigma'(z^{l+1})(w^{l+2})^T \dots \Sigma'(z^L) \nabla_a C.$$

As a result, if we use standard gradient-based learning techniques, different layers in the network will tend to learn at wildly different speeds.

### Vanishing Gradient

$$\delta^l = \underbrace{\Sigma'(z^l)(w^{l+1})^T}_{<1} \cdot \underbrace{\Sigma'(z^{l+1})(w^{l+2})^T}_{<1} \dots \Sigma'(z^L) \nabla_a C.$$

### Exploding Gradient

$$\delta^l = \underbrace{\Sigma'(z^l)(w^{l+1})^T}_{>1} \cdot \underbrace{\Sigma'(z^{l+1})(w^{l+2})^T}_{>1} \dots \Sigma'(z^L) \nabla_a C.$$
